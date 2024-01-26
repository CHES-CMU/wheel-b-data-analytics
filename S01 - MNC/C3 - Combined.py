import pandas as pd
import pickle, sys, os, pickle

###############################################################################
USE_SAMPLE = False
prefixInput = "C2"
prefixOutput = "C3"

###############################################################################
inputFolder = f"{prefixInput}_out"
outputFolder = f"{prefixOutput}_out"

# Load data
cwd = sys.path[0]
if not USE_SAMPLE:
    inputFilePathV1 = os.path.join(cwd, inputFolder, f"{prefixInput}_V1_df_full.pickle")
    inputFilePathV2 = os.path.join(cwd, inputFolder, f"{prefixInput}_V2_df_full.pickle")
    outputFilePath = os.path.join(cwd, outputFolder, f"{prefixOutput}_df_full.pickle")
else:
    inputFilePathV1 = os.path.join(
        cwd, inputFolder, f"{prefixInput}_V1_df_sampled.pickle"
    )
    inputFilePathV2 = os.path.join(
        cwd, inputFolder, f"{prefixInput}_V2_df_sampled.pickle"
    )
    outputFilePath = os.path.join(
        cwd, outputFolder, f"{prefixOutput}_df_sampled.pickle"
    )

with open(inputFilePathV1, "rb") as handle:
    dataV1 = pickle.load(handle)
with open(inputFilePathV2, "rb") as handle:
    dataV2 = pickle.load(handle)
df1 = dataV1["df"]
df2 = dataV2["df"]

# Combine data
df1 = df1.loc[
    :, ["orderId", "appointTimeCV", "arrivalTimeCV", "emergencyDegree", "serviceType"]
]
df2 = df2.loc[:, ["id", "order_atCV", "arrival_atCV", "priorityId", "transportation"]]

# Change transportation value
mappingTransportation = {"รถเข็น": "wheel", "พนักงาน": "staff", "เปล": "bed"}
df2["transportation"] = df2["transportation"].map(mappingTransportation)

mapping = {}
for i, j in zip(
    ["id", "order_atCV", "arrival_atCV", "priorityId", "transportation"],
    ["orderId", "appointTimeCV", "arrivalTimeCV", "emergencyDegree", "serviceType"],
):
    mapping[i] = j
df2.rename(columns=mapping, inplace=True)
df1 = pd.concat([df1, df2], axis=0)


# Store data (serialize)
data = dict(df=df1)
with open(outputFilePath, "wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
pass
