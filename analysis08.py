import pandas as pd
from matplotlib import pyplot as plt
from utils import get_pr_news_data, trend_line
from mpl_toolkits.mplot3d import Axes3D

"""
get the 3d scatter
"""

df = get_pr_news_data()
df["week"] = df["release_date"].dt.week
df = df[~df["week"].isin([15, 41])]
df = df.sort_values('release_date')

# get industry against pr_count dataframe
df_pr_count = df.groupby('level3').size().sort_values(ascending=True)
df_pr_count = df_pr_count.reset_index()
df_pr_count.columns = ['industry', 'pr_count']

# get daily pr count per industry dataframe to create industry-trend dataframe
df_time = df.groupby(['release_date', 'level3']).size().unstack().fillna(0)
df_time = df_time.resample('D').sum()
df_time = df_time[df_time.index.dayofweek < 5].stack()
df_time = pd.DataFrame(df_time).reset_index()
df_time.columns = ['release_date', 'level3', 'pr_count']

# get industry against trend dataframe
df_slope = pd.DataFrame(df_time.groupby('level3').apply(lambda v: trend_line(v.pr_count)))
df_slope.columns = ['slope']
df_slope = df_slope.sort_values('slope', ascending=False).reset_index()
df_slope.columns = ['industry', 'slope']


# merge 2 dataframes
df_3d = pd.merge(left=df_pr_count, right=df_slope, on='industry')
df_3d['color'] = df_3d.apply(lambda x: 'R' if x['slope'] > 0 else 'B', axis=1)


# plot 3d scatter
pr_count = df_3d['pr_count'].tolist()
slope = df_3d['slope'].tolist()
level3 = df_3d.index
color = df_3d['color'].tolist()

fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(xs=level3, ys=pr_count, zs=slope, color=color, marker='o')
plt.show()

print(df_3d[ (df_3d['slope'] > 0) & (df_3d['pr_count'] > 1000) ])
print(df_3d[ (df_3d['slope'] < -0.022) & (df_3d['pr_count'] > 1000) ])

"""
                 industry  pr_count     slope color
165        Data Analytics      1432  0.023742     R
166  Financial Technology      1574  0.014587     R
                 industry  pr_count     slope color
161   Internet Technology      1099 -0.026949     B
164            Blockchain      1284 -0.023275     B
170              Networks      2468 -0.032627     B
174  Computer Electronics      5036 -0.032614     B

"""
