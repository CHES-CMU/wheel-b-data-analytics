import pandas as pd
import pickle, sys, os, pickle


###############################################################################
USE_SAMPLE = False
prefixInput = "C4"
prefixOutput = "C5"

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

filt = (df1.index < "2023-02-01") & (df1.index > "2022-12-31")
df2 = df1[filt]

rNumAll = df2.shape[0]
rNumE1 = df2[df2["emergencyDegree"] == "E1"].shape[0]
rNumE2 = df2[df2["emergencyDegree"] == "E2"].shape[0]
rNumE3 = df2[df2["emergencyDegree"] == "E3"].shape[0]

filt = (df2["emergencyDegree"] == "E1") & (df2["inTime"] == False)
rNumE1Late = df2[filt].shape[0]
filt = (df2["emergencyDegree"] == "E2") & (df2["inTime"] == False)
rNumE2Late = df2[filt].shape[0]
filt = (df2["emergencyDegree"] == "E3") & (df2["inTime"] == False)
rNumE3Late = df2[filt].shape[0]

rPercentLateE1 = rNumE1Late / rNumE1 * 100
rPercentLateE2 = rNumE2Late / rNumE2 * 100
rPercentLateE3 = rNumE3Late / rNumE3 * 100

rNumBed = df2[df2["serviceType"] == "bed"].shape[0]
rNumStaff = df2[df2["serviceType"] == "staff"].shape[0]
rNumWheel = df2[df2["serviceType"] == "wheel"].shape[0]

pass
