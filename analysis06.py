import pandas as pd
from matplotlib import pyplot as plt
from utils import get_pr_news_data

"""
removed first week, last week and weekends.
could see trend.
"""

df = get_pr_news_data()
df["week"] = df["release_date"].dt.week
df = df[~df["week"].isin([15, 41])]

time_df = df.groupby(['release_date', 'level3']).size().unstack().fillna(0)
time_df = time_df.resample('D').sum()
time_df = time_df[time_df.index.dayofweek < 5]

plt.plot(time_df['Blockchain'])
plt.show()
