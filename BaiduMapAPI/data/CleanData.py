import pandas as pd

df = pd.read_csv("ChAdminUnit2016.csv", encoding="utf-8")

df = df[["省", "城市", "区镇", "街道"]]

df.drop_duplicates(inplace=True)

df.to_csv("ChUnit2016.csv", encoding="utf-8", index=False)