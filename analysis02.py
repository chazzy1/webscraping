import pandas as pd
from matplotlib import pyplot as plt
from utils import get_pr_news_data

"""
Trying to see the trend
by ploting time series data
"""

df = get_pr_news_data()

time_df = df.groupby(['release_date', 'level3']).size().unstack().fillna(0)

time_df = time_df.sort_values('release_date')

time_df = time_df.resample('D').sum()

plt.plot(time_df['Blockchain'])
plt.show()

"""
plot shows periodic spikes
"""







