import pandas as pd
import numpy as np
from datetime import datetime
import pickle, sys, os, pickle, pathlib


def rowToDrop(row):
    toDrop = False
    seconds = row["assigned_at"]
    cancelApprove = row["cancled_at"]
    arrivalTime = row["arrival_at"]
    if seconds < 0:
        # print(f"Loc:{row.name} - Invalid appointTime")
        toDrop = True
    elif (type(cancelApprove) == bool) and (cancelApprove == True):
        # print(f"Loc:{row.name} - Cancelled order")
        toDrop = True
    # elif pickUpTime == "":
    #     print(f"Loc:{row.name} - No pickup time")
    #     toDrop = True
    elif arrivalTime == "":
        # print(f"Loc:{row.name} - No arrival time")
        toDrop = True
    return toDrop


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


df = pd.read_json("../Data/V2-wheel-b-suandok_order_2023-5-19.json")
df["idx"] = df.reset_index().index

# Check for problematic data

df2 = df
timeFields = ["order_at", "arrival_at"]
timeFieldsCV = [f"{i}CV" for i in timeFields]

for timeField, timeFieldCV in zip(timeFields, timeFieldsCV):
    df2[timeFieldCV] = df2.apply(lambda row: convertToDateTime(row, timeField), axis=1)

df2["wardWaitingMin"] = df2.apply(
    lambda row: timeDifference(row, "assigned_at", "arrival_at"), axis=1
)


data = dict(df=df2)
# Store data (serialize)
with open("df2.pickle", "wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
