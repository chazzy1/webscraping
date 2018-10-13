import pandas as pd
from matplotlib import pyplot as plt
from utils import get_pr_news_data

"""
removed weekends from dataframe to get rid of spikes
and checked time series plot again.
"""

df = get_pr_news_data()

time_df = df.groupby(['release_date', 'level3']).size().unstack().fillna(0)

time_df = time_df.resample('D').sum()

time_df = time_df[time_df.index.dayofweek < 5]
#time_df = time_df[~time_df.index.weekday_name.isin(['Saturday', 'Sunday'])]


plt.plot(time_df['Blockchain'])
plt.show()
