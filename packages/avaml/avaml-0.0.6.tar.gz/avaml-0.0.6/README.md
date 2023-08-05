# avaml - helper functions for Avalanche machine learning

This package contains functions used to prepare data from
the Norwegian Avalanche Forecasting Service to facilitate
machine learning.

## Installation

To install using `pip`:
```
pip install avaml
```

## Example program

### Searching for data

Here is a short example program using the package to prepare data
for training a RandomForestClassifier:

```python
import sys

from regobslib import SnowRegion
import avaml
import datetime as dt
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

DAYS_IN_TIMELINE = 4
START_DATE = dt.date(2017, 11, 1)
STOP_DATE = dt.date(2021, 7, 1)
TRAINING_REGIONS = [
    SnowRegion.VEST_FINNMARK,
    SnowRegion.NORD_TROMS,
    SnowRegion.LYNGEN,
    SnowRegion.SOR_TROMS,
    SnowRegion.INDRE_TROMS,
    SnowRegion.LOFOTEN_OG_VESTERALEN,
    SnowRegion.SVARTISEN,
    SnowRegion.HELGELAND,
    SnowRegion.TROLLHEIMEN,
    SnowRegion.ROMSDAL,
    SnowRegion.SUNNMORE,
    SnowRegion.INDRE_FJORDANE,
    SnowRegion.JOTUNHEIMEN,
    SnowRegion.HALLINGDAL,
    SnowRegion.INDRE_SOGN,
    SnowRegion.VOSS,
    SnowRegion.HEIANE,
]
VALIDATION_REGIONS = [
    SnowRegion.TROMSO,
    SnowRegion.SALTEN,
    SnowRegion.VEST_TELEMARK,
]
TEST_REGIONS = [
    SnowRegion.FINNMARKSKYSTEN,
    SnowRegion.OFOTEN,
    SnowRegion.HARDANGER,
]
REGIONS = sorted(TRAINING_REGIONS + VALIDATION_REGIONS + TEST_REGIONS)

# fetch_and_prepare_aps_varsom() does a number of things:
# * See if a call with the same parameters have been called earlier.
#   If so, load prepared csv's from disk.
# * If there is no prepared data on disk, see if there are raw
#   data instead.
# * If no previously downloaded data is found, download data from
#   APS and Varsom.
# * Save the data as csv's to the 'cache_dir'
# * Prepare the data:
#   * It transforms the Varsom DataFrame to contain the same index
#     as the APS DataFrame, replicating the forecast for every
#     elevation level. It then removes avalanche problems that
#     does not exist at the row's elevation level and remove the
#     elevation data from the avalanche problems. All rows that
#     does not contain complete APS data is removed.
#   * Creates a timeline out of the APS DataFrame. This means that
#     the APS data is concatenated onto a shifted version of itself,
#     making each APS row contain several days worth of data.
#     This will make some rows incomplete. They will be removed.
aps, varsom = avaml.prepare.fetch_and_prepare_aps_varsom(START_DATE,
                                                         STOP_DATE,
                                                         DAYS_IN_TIMELINE,
                                                         REGIONS,
                                                         print_to=sys.stdout,  # Print progression to terminal
                                                         cache_dir=".",  # Use current dir for csv-files
                                                         read_cache=True,
                                                         write_cache=True)

print("Training and predicting problems")
# split_avalanche_problems() takes the Varsom Dataframe and splits it into
# several DataFrames, containing information about one avalanche problem each.
# If a problem row contains some values, but also some NaNs, it is invalid and
# is removed from both Varsom and APS.
#
# A 3-tuple is returned, (problems_X: Dict, problems_Y: Dict, problems: List).
# * problems_X is a dict with the problem as key and a DataFrame with indata as value
# * problems_Y is a dict with the problem as key and a DataFrame with labels as value
# * problems is a list of avalanche problem names
problems_X, problems_Y, problems = avaml.prepare.split_avalanche_problems(aps, varsom)
f1_dict = {}
for problem in problems:
    X = problems_X[problem]
    Y = problems_Y[problem]

    # Splitting data into TRAINING and VALIDATION sets
    training_index = Y.index.isin(TRAINING_REGIONS, level="region")
    validation_index = Y.index.isin(VALIDATION_REGIONS, level="region")
    training_X = X.loc[training_index]
    training_Y = Y.loc[training_index].any(axis=1)
    validation_X = X.loc[validation_index]
    validation_Y = Y.loc[validation_index].any(axis=1)

    # Training and validating
    classifier = RandomForestClassifier(n_estimators=10)
    classifier.fit(training_X.values, training_Y)
    prediction = pd.Series(classifier.predict(validation_X.values), index=validation_X.index)

    # Calculating and storing scores to dict
    elevation_prediction = prediction
    elevation_ground_truth = validation_Y
    problem_prediction = elevation_prediction.unstack().any(axis=1)
    problem_ground_truth = elevation_ground_truth.unstack().any(axis=1)
    training_elevation_ground_truth = training_Y
    training_problem_ground_truth = training_elevation_ground_truth.unstack().any(axis=1)
    elevation_f1 = metrics.f1_score(elevation_ground_truth, elevation_prediction)
    problem_f1 = metrics.f1_score(problem_ground_truth, problem_prediction)
    f1_dict[problem] = {
        ("f1", "per_elevation"): elevation_f1,
        ("f1", "per_forecast"): problem_f1,
        ("training_n_true", "per_elevation"):
            f"{training_elevation_ground_truth.sum()}/{len(training_elevation_ground_truth)}",
        ("training_n_true", "per_forecast"):
            f"{training_problem_ground_truth.sum()}/{len(training_problem_ground_truth)}",
        ("validation_n_true", "per_elevation"):
            f"{elevation_ground_truth.sum()}/{len(elevation_ground_truth)}",
        ("validation_n_true", "per_forecast"):
            f"{problem_ground_truth.sum()}/{len(problem_ground_truth)}",
    }

with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.expand_frame_repr', False):
    print(pd.DataFrame(f1_dict).T)
```
