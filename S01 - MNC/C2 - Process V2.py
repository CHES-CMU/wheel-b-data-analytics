import pandas as pd
import numpy as np
from datetime import datetime
import pickle, sys, os, pickle, pathlib


def convertToDateTime(row, field):
    # print(len(str(row[field])))
    if len(str(row[field])) == 26:
        timestamp = datetime.strptime(
            str(row[field])[:-7], "%Y-%m-%d %H:%M:%S"
        ).timestamp()
    # if len(str(row[field]))
    elif len(str(row[field])) == 19:
        timestamp = datetime.strptime(str(row[field]), "%Y-%m-%d %H:%M:%S").timestamp()
    else:
        timestamp = 0
    if row[field] != None:
        seconds = timestamp
    else:
        seconds = 0
    timestamp = datetime.now().timestamp()
    if seconds > timestamp:
        seconds = 0
    return pd.to_datetime(seconds, unit="s")


# Calculate time difference
def timeDifference(row, startTimeField, stopTimeField):
    if row[startTimeField] > row[stopTimeField]:
        return -(row[startTimeField] - row[stopTimeField]).total_seconds() / 60
    else:
        return (row[stopTimeField] - row[startTimeField]).total_seconds() / 60


###############################################################################
USE_SAMPLE = False
prefixInput = "C1"
prefixOutput = "C2"

###############################################################################
inputFolder = f"{prefixInput}_out"
outputFolder = f"{prefixOutput}_out"

cwd = sys.path[0]
if not USE_SAMPLE:
    inputFilePath = os.path.join(cwd, inputFolder, f"{prefixInput}_V2_df_full.pickle")
    outputFilePath = os.path.join(
        cwd, outputFolder, f"{prefixOutput}_V2_df_full.pickle"
    )
else:
    inputFilePath = os.path.join(
        cwd, inputFolder, f"{prefixInput}_V2_df_sampled.pickle"
    )
    outputFilePath = os.path.join(
        cwd, outputFolder, f"{prefixOutput}_V2_df_sampled.pickle"
    )

with open(inputFilePath, "rb") as handle:
    data = pickle.load(handle)
    df1 = data["df"]


timeFields = ["order_at", "arrival_at"]
timeFieldsCV = [f"{i}CV" for i in timeFields]

for timeField, timeFieldCV in zip(timeFields, timeFieldsCV):
    df1[timeFieldCV] = df1.apply(lambda row: convertToDateTime(row, timeField), axis=1)

df1["wardWaitingMin"] = df1.apply(
    lambda row: timeDifference(row, "assigned_at", "arrival_at"), axis=1
)

# Store data (serialize)
data = dict(df=df1)
with open(outputFilePath, "wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
pass
