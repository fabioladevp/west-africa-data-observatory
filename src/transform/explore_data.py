import pandas as pd


df = pd.read_csv(
    "data/raw/worldbank_indicators.csv"
)


print("\nFIRST 10 ROWS")
print(df.head(10))


print("\nDATASET SIZE")
print(df.shape)


print("\nCOUNTRIES")
print(df["country"].unique())


print("\nINDICATORS")
print(df["indicator"].unique())


print("\nMISSING VALUES")
print(df.isnull().sum())