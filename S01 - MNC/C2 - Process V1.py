import pandas as pd
from datetime import datetime
import pickle, sys, os, pickle, pathlib


def rowToDrop(row):
    toDrop = False
    seconds = row["appointTime"]["_seconds"]
    cancelApprove = row["cancelApprove"]
    arrivalTime = row["arrivalTime"]
    if seconds < 0:
        # print(f"Loc:{row.name} - Invalid appointTime")
        toDrop = True
    elif (type(cancelApprove) == bool) and (cancelApprove == True):
        # print(f"Loc:{row.name} - Cancelled order")
        toDrop = True
    elif arrivalTime == "":
        # print(f"Loc:{row.name} - No arrival time")
        toDrop = True
    return toDrop


def convertToDateTime(row, field):
    # print(field, row[field])
    if row[field] == None:
        row[field] = {"_seconds": 0}
    if "_seconds" in row[field]:
        seconds = row[field]["_seconds"]
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
    inputFilePath = os.path.join(cwd, inputFolder, f"{prefixInput}_V1_df_full.pickle")
    outputFilePath = os.path.join(
        cwd, outputFolder, f"{prefixOutput}_V1_df_full.pickle"
    )
else:
    inputFilePath = os.path.join(
        cwd, inputFolder, f"{prefixInput}_V1_df_sampled.pickle"
    )
    outputFilePath = os.path.join(
        cwd, outputFolder, f"{prefixOutput}_V1_df_sampled.pickle"
    )

with open(inputFilePath, "rb") as handle:
    data = pickle.load(handle)
    df1 = data["df"]

df1["idx"] = df1.reset_index().index

# Check for problematic data
df1["toDrop"] = df1.apply(rowToDrop, axis=1)
idxDrop = df1[df1["toDrop"] == True].index
print(idxDrop)
df1[df1["toDrop"] == True][
    ["orderId", "pickUp", "appointTime", "cancelApprove", "arrivalTime"]
]
df2 = df1.drop(idxDrop)

# Time
timeFields = [
    "acceptTime",
    "appointTime",
    "arrivalTime",
    "assignmentTime",
    "confirmStaffTime",
    "createdAt",
    "dropOffTime",
    "finishTime",
    "pickUpTime",
]
timeFieldsCV = [f"{i}CV" for i in timeFields]

for timeField, timeFieldCV in zip(timeFields, timeFieldsCV):
    df2[timeFieldCV] = df2.apply(lambda row: convertToDateTime(row, timeField), axis=1)

df2["wardWaitingMin"] = df2.apply(
    lambda row: timeDifference(row, "assignmentTimeCV", "arrivalTimeCV"), axis=1
)

# Store data (serialize)
data = dict(df=df2)
with open(outputFilePath, "wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
pass
