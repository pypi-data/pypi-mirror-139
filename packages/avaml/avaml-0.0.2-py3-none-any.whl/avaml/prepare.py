import os
from importlib import metadata
from typing import Dict, List, TextIO

import pandas as pd
import numpy as np
import datetime as dt
from regobslib import Aps, SnowRegion, SnowVarsom, Connection


def _drop_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Removes all rows from DataFrame which does contain a NaN-value
    """
    return df.loc[~(df.isna()).any(axis=1)]


def _drop_invalid_problems(df: pd.DataFrame) -> pd.DataFrame:
    """Removes all rows from a Varsom DataFrame which contains NaN-values
    but is not only NaN-values. The remaining rows is either all NaN or
    all values.
    """
    return df.loc[~(df.isna().any(axis=1) & ~(df.isna()).all(axis=1))]


def _join_aps_varsom(aps: pd.DataFrame, varsom: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """Takes APS and Varsom problem DataFrames and splits the Varsom problems
    up into the elevation levels of the APS DataFrame.

    Only rows which exists in both DataFrames are kept.
    """
    def remove_irrelevant_problems(forecast: pd.Series) -> pd.Series:
        def check_and_remove_problem(problem: pd.Series) -> pd.Series:
            if problem[p_min] is None and problem[p_max] is None:
                return problem
            if not (problem[p_min] < aps_max and problem[p_max] > aps_min):
                problem[:] = None
            return problem

        aps_min, aps_max = Aps.parse_level(forecast.name[2])
        p_min, p_max = "elevation_min", "elevation_max"
        forecast_index = forecast.index
        forecast = forecast.unstack(level=0)
        forecast = forecast.apply(check_and_remove_problem)
        return forecast.unstack().reindex(forecast_index)

    def drop_elevations(forecast: pd.Series) -> pd.Series:
        return forecast.drop(["elevation_min", "elevation_max"], level=1)

    joined = aps.join(varsom, on=["region", "date"], how="inner")
    index = joined.index
    joined.index = index.set_levels([index.levels[0], pd.to_datetime(index.levels[1]), index.levels[2]])
    varsom = joined.reindex(varsom.columns, axis=1)
    aps = joined.reindex(aps.columns, axis=1)
    varsom = varsom.apply(remove_irrelevant_problems, axis=1)
    varsom = varsom.apply(drop_elevations, axis=1)
    aps = _drop_nan_rows(aps)
    intersected_index = varsom.index.intersection(aps.index)
    return aps.reindex(intersected_index), varsom.reindex(intersected_index)


def _make_timeline(aps: pd.DataFrame, varsom: pd.DataFrame, days: int) -> (pd.DataFrame, pd.DataFrame):
    """Concatenates shifted versions of an APS DataFrame on axis 1, so that
    every row has 'days' numbers of days concatenadet into it, making each row
    a time series.

    The first and last rows will be incomplete. These are removed from both aps and varsom.
    """

    def sub_date(date: dt.date, days_: int):
        if isinstance(date, str):
            date = dt.date.fromisoformat(date)
        return date - dt.timedelta(days=days_)

    if days < 1:
        raise ValueError("days parameter must be larger or equal to 1")
    days = range(0, -days, -1)
    apses = []
    for day in days:
        shifted_index = aps.index.map(lambda i: (i[0], sub_date(i[1], day), i[2]))
        shifted_aps = aps.copy()
        shifted_aps.index = shifted_index
        apses.append(shifted_aps)

    concat_aps = pd.concat(apses,
                           keys=days,
                           axis=1,
                           names=["day_offset", "data_type", "attr"])
    concat_aps = _drop_nan_rows(concat_aps)
    varsom = varsom.reindex(concat_aps.index)
    return concat_aps, varsom


def split_avalanche_problems(X: pd.DataFrame, Y: pd.DataFrame) -> [Dict, Dict, List]:
    """Splits a Varsom DataFrame into a number of dataframes containing only
    information about one avalanche problem each.
    """
    split_X = {}
    split_Y = {}
    problems = Y.columns.unique(level="problem")
    for problem in problems:
        problem_Y = _drop_invalid_problems(Y[[problem]]).replace(np.nan, 0)
        index_intersection = X.index.intersection(problem_Y.index)
        split_X[problem] = X.reindex(index_intersection)
        split_Y[problem] = problem_Y.reindex(index_intersection)
    return split_X, split_Y, problems.to_list()


def prepare_aps_varsom(aps: pd.DataFrame, varsom: pd.DataFrame, days: int) -> (pd.DataFrame, pd.DataFrame):
    """
    :param aps: An APS Dataframe as given by regobslib.Aps.to_frame()
    :param varsom: An Varsom DataFrame as given by regobslib.SnowVarsom.to_frame()
    :param days: The number of days included in the APS timeline
    :return: New APS and Varsom DataFrames, with combined indexes, invalid data removed and
             timelines on the APS Dataframe.
    """
    aps, varsom = _join_aps_varsom(aps, varsom)
    return _make_timeline(aps, varsom, days)


def read_prepared_aps_csv(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, sep=";", header=[0, 1, 2], index_col=[0, 1, 2])
    df.index = df.index.set_levels([
        df.index.levels[0],
        pd.to_datetime(df.index.levels[1]),
        df.index.levels[2],
    ])
    return df


def read_prepared_varsom_csv(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename, sep=";", header=[0, 1], index_col=[0, 1, 2])
    df.index = df.index.set_levels([
        df.index.levels[0],
        pd.to_datetime(df.index.levels[1]),
        df.index.levels[2],
    ])
    return df


def fetch_and_prepare_aps_varsom(start_date: dt.date,
                                 stop_date: dt.date,
                                 days: int,
                                 regions: List[SnowRegion] = None,
                                 print_to: TextIO = None,
                                 cache_dir: str = ".",
                                 read_cache: bool = True,
                                 write_cache: bool = True) -> (pd.DataFrame, pd.DataFrame):
    def if_print(msg: str):
        if print_to is not None:
            print(msg, file=print_to)

    date_range = f"{start_date.isoformat()}--{stop_date.isoformat()}"
    region_range = "-".join([str(r.value) for r in regions])
    version = metadata.version("regobslib")
    file_suffix = f"{date_range}_{region_range}_{version}"

    prepared_varsom_filename = os.path.join(cache_dir, f"prepared_varsom_{file_suffix}.csv")
    prepared_aps_filename = os.path.join(cache_dir, f"prepared_aps_{file_suffix}.csv")
    try:
        if not read_cache:
            raise FileNotFoundError()
        if_print("Looking for prepared APS and Varsom data on disk")
        aps = read_prepared_aps_csv(prepared_aps_filename)
        varsom = read_prepared_varsom_csv(prepared_varsom_filename)
        if_print("Loaded prepared APS and Varsom data from disk")
    except FileNotFoundError:
        if read_cache:
            if_print("No prepared data found, looking for downloaded raw data.")

        varsom_filename = os.path.join(cache_dir, f"varsom_{file_suffix}.csv")
        try:
            if not read_cache:
                raise FileNotFoundError()
            varsom = SnowVarsom.read_csv(varsom_filename)
            if_print("Found downloaded raw Varsom data")
        except FileNotFoundError:
            if_print("Fetching Varsom data from online resources (ETA 7 minutes)")
            varsom = Connection(prod=True).get_varsom(start_date, stop_date).to_problem_frame()
            if write_cache:
                varsom.to_csv(varsom_filename, sep=";")

        aps_filename = os.path.join(cache_dir, f"aps_{file_suffix}.csv")
        try:
            if not read_cache:
                raise FileNotFoundError()
            aps = Aps.read_csv(aps_filename)
            if_print("Found downloaded raw APS data")
        except FileNotFoundError:
            if_print("Fetching APS data from online resources (ETA 10 minutes)")
            aps = Connection(prod=True).get_aps(start_date, stop_date).to_frame()
            if write_cache:
                aps.to_csv(aps_filename, sep=";")

    if_print("Preparing data (ETA 9 minutes)")
    aps, varsom = prepare_aps_varsom(aps, varsom, days)
    if write_cache:
        aps.to_csv(prepared_aps_filename, sep=";")
        varsom.to_csv(prepared_varsom_filename, sep=";")
