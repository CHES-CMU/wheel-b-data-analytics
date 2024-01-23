import pandas as pd
import pickle, sys, os, pickle, pathlib


###############################################################################
cwd = sys.path[0]
parentPath = pathlib.Path(cwd).parent.absolute()
baseFolder = "S00 - Data MNC"
filename = "wheel-b-suandok_orders_2023-5-19_4-50-pm.json"
filePath = os.path.join(parentPath, baseFolder, filename)

df1 = pd.read_json(filePath)
df1 = df1.sample(frac=0.01)
data = dict(df=df1)
outputFilePath = os.path.join(cwd, "V1_df_sampled.pickle")
with open(outputFilePath, "wb") as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
