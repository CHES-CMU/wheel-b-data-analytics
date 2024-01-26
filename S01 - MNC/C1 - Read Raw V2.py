import pandas as pd
import pickle, sys, os, pickle, pathlib

USE_SAMPLE = False
prefixOutput = "C1"
###############################################################################
cwd = sys.path[0]
outputFolder = f"{prefixOutput}_out"
parentPath = pathlib.Path(cwd).parent.absolute()
baseFolder = "S00 - Data MNC"
filename = "V2-wheel-b-suandok_order_2023-5-19.json"
filePath = os.path.join(parentPath, baseFolder, filename)

df1 = pd.read_json(filePath)
if USE_SAMPLE:
    df1 = df1.sample(frac=0.01)
    outputFilePath = os.path.join(
        cwd, outputFolder, f"{prefixOutput}_V2_df_sampled.pickle"
    )
else:
    outputFilePath = os.path.join(
        cwd, outputFolder, f"{prefixOutput}_V2_df_full.pickle"
    )

data = dict(df=df1)
with open(outputFilePath, "wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
