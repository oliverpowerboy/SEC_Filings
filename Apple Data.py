import pandas as pd

data = pd.read_csv("APPL.csv")

print(data["tag"].unique())