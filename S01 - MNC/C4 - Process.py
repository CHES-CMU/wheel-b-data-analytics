import pandas as pd
import pickle, sys, os, pickle


def timeDifference(row, startTimeField, stopTimeField):
    # print(row[startTimeField] - row[stopTimeField] )
    if row[startTimeField] > row[stopTimeField]:
        return -(row[startTimeField] - row[stopTimeField]).total_seconds() / 60
    else:
        return (row[stopTimeField] - row[startTimeField]).total_seconds() / 60


def late_not(row):
    if row["waiting_time"] <= 0:
        return "In-Time"
    if (
        row["waiting_time"] > 0
        and row["emergencyDegree"] == "E1"
        and row["waiting_time"] <= 5
    ):
        return "In-Time"
    if (
        row["waiting_time"] > 0
        and row["emergencyDegree"] == "E2"
        and row["waiting_time"] <= 15
    ):
        return "In-Time"
    if (
        row["waiting_time"] > 0
        and row["emergencyDegree"] == "E3"
        and row["waiting_time"] <= 30
    ):
        return "In-Time"
    else:
        return "Late"


###############################################################################
USE_SAMPLE = False
prefixInput = "C3"
prefixOutput = "C4"

###############################################################################
inputFolder = f"{prefixInput}_out"
outputFolder = f"{prefixOutput}_out"

# Load data
cwd = sys.path[0]
if not USE_SAMPLE:
    inputFilePath = os.path.join(cwd, inputFolder, f"{prefixInput}_df_full.pickle")
    outputFilePath = os.path.join(cwd, outputFolder, f"{prefixOutput}_df_full.pickle")
else:
    inputFilePath = os.path.join(cwd, inputFolder, f"{prefixInput}_df_sampled.pickle")
    outputFilePath = os.path.join(
        cwd, outputFolder, f"{prefixOutput}_df_sampled.pickle"
    )

with open(inputFilePath, "rb") as handle:
    dataV1 = pickle.load(handle)
df1 = dataV1["df"]


# Preprocess data
df1["waiting_time"] = df1.apply(
    lambda row: timeDifference(row, "appointTimeCV", "arrivalTimeCV"), axis=1
)
df1["Late_or_not"] = df1.apply(late_not, axis=1)
df1["inTime"] = df1["Late_or_not"].apply(lambda el: el == "In-Time")
df1 = df1.rename(columns={"waiting_time": "waitingTime"})
df1 = df1.drop(columns=["Late_or_not", "arrivalTimeCV"])
df1 = df1.set_index("appointTimeCV")


# Store data (serialize)
data = dict(df=df1)
with open(outputFilePath, "wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
pass
