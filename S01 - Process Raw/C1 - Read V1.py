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
USE_SAMPLE = True

cwd = sys.path[0]

if not USE_SAMPLE:
    parentPath = pathlib.Path(cwd).parent.absolute()
    baseFolder = "S00 - Data MNC"
    filename = "wheel-b-suandok_orders_2023-5-19_4-50-pm.json"
    filePath = os.path.join(parentPath, baseFolder, filename)
    df1 = pd.read_json(filePath)
else:
    filePath = os.path.join(cwd, "V1_df_sampled.pickle")
    with open(filePath, "rb") as handle:
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
outputFilePath = os.path.join(cwd, "V1_df.pickle")
with open(outputFilePath, "wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

pass
