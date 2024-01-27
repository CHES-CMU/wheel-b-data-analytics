import os, sys

cwd = sys.path[0]

ns = [1, 2, 3, 4, 5]

for n in ns:
    folderPath = os.path.join(cwd, f"C{n}_out")
    if not (os.path.exists(folderPath)):
        os.mkdir(folderPath)
