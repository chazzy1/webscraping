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

df = df[~df["level3"].isin(['UK Regulatory News', 'All Public Company News', 'Computer & Electronics'])]
df["release_date"] = pd.to_datetime(df["release_date"])
df["week"] = df["release_date"].dt.week
df = df[~df["week"].isin([15, 41])]
df = df.sort_values('release_date')


group = df.groupby('level3')
df_pr_count = df.groupby('level3').size().sort_values(ascending=True)

df_pr_count = df_pr_count.reset_index()
df_pr_count.columns = ['industry', 'pr_count']


df_time = df.groupby(['release_date', 'level3']).size().unstack().fillna(0)
df_time = df_time.resample('D').sum()

df_time = df_time[df_time.index.dayofweek < 5].stack()
df_time = pd.DataFrame(df_time).reset_index()

df_time.columns = ['release_date', 'level3', 'pr_count']


def trendline(data, order=1):
    coeffs = np.polyfit(range(len(data.index)), data, order)
    slope = coeffs[0]
    return float(slope)


df_slope = pd.DataFrame(df_time.groupby('level3').apply(lambda v: trendline(v.pr_count)))
df_slope.columns = ['slope']
df_slope = df_slope.sort_values('slope', ascending=False).reset_index()
df_slope.columns = ['industry', 'slope']

df_3d = pd.merge(left=df_pr_count, right=df_slope, on='industry')

df_3d['color'] = df_3d.apply(lambda x: 'R' if x['slope'] > 0 else 'B', axis=1)


print(df_3d[ (df_3d['slope'] > 0) & (df_3d['pr_count'] > 1000) ])
print(df_3d[ (df_3d['slope'] < -0.022) & (df_3d['pr_count'] > 1000) ])


pr_count = df_3d['pr_count'].tolist()
slope = df_3d['slope'].tolist()
level3 = df_3d.index
color = df_3d['color'].tolist()


fig = plt.figure()
ax = Axes3D(fig)


ax.scatter(xs=level3, ys=pr_count, zs=slope, color=color, marker='o')
plt.show()


