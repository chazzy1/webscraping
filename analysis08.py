import pandas as pd
import json
import numpy as np

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
get the 3d scatter
"""

df = pd.read_csv('./data/titles_20181008.txt', header=None, nrows=None)



# Prepare Data
df.columns = ['nav_level', 'link', 'release_date', 'title']

def get_nav_level(nav_level_str, level):
    nav_level3 = json.loads(nav_level_str.replace("'", "\""))["SubNavigationLink"].split("|")[3].strip()
    return nav_level3

df["level1"] = df["nav_level"].map(lambda x: get_nav_level(x, 1))
df["level2"] = df["nav_level"].map(lambda x: get_nav_level(x, 2))
df["level3"] = df["nav_level"].map(lambda x: get_nav_level(x, 3))

df = df[~df["level3"].isin(['UK Regulatory News', 'All Public Company News'])]
df["release_date"] = pd.to_datetime(df["release_date"])
df["week"] = df["release_date"].dt.week
df = df[~df["week"].isin([15, 41])]
df = df.sort_values('release_date')




pr_count_df = df.groupby(['release_date', 'level3']).size().unstack().fillna(0)
pr_count_df = pr_count_df.resample('D').sum()

pr_count_df = pr_count_df[pr_count_df.index.dayofweek < 5].stack()
pr_count_df = pd.DataFrame(pr_count_df).reset_index()

pr_count_df.columns = ['release_date', 'level3', 'pr_count']


def trendline(data, order=1):
    coeffs = np.polyfit(range(len(data.index)), data, order)
    slope = coeffs[0]
    return float(slope)


slope_df = pd.DataFrame(pr_count_df.groupby('level3').apply(lambda v: trendline(v.pr_count)))
slope_df.columns = ['slope']
slope_df = slope_df.sort_values('slope', ascending=False).reset_index()
#print(slope_df)



df_3d = pd.merge(left=pr_count_df, right=slope_df, on='level3')


pr_count = df_3d['pr_count'].tolist()
slope = df_3d['slope'].tolist()
level3 = df_3d.index



fig = plt.figure()
ax = Axes3D(fig)
import random
sequence_containing_x_vals = list(range(0, 100))
sequence_containing_y_vals = list(range(0, 100))
sequence_containing_z_vals = list(range(0, 100))

random.shuffle(sequence_containing_x_vals)
random.shuffle(sequence_containing_y_vals)
random.shuffle(sequence_containing_z_vals)

ax.scatter(level3, pr_count, slope)
plt.show()