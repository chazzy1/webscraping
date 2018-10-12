import pandas as pd
import json

from matplotlib import pyplot as plt

"""
trying to remov first, last week
"""

df = pd.read_csv('./data/titles_20181008.txt', header=None, nrows=None)

df.columns = ['nav_level', 'link', 'release_date', 'title']

df["release_date"] = pd.to_datetime(df["release_date"])

df["week"] = df["release_date"].dt.week

print(min(df["week"]), max(df["week"]))

"""
15 41
"""

