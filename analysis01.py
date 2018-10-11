import pandas as pd
import json

from matplotlib import pyplot as plt

#import seaborn as sns
#sns.set()

df = pd.read_csv('./data/titles_20181008.txt', header=None, nrows=None)

df.columns = ['nav_level', 'link', 'release_date', 'title']



def get_nav_level(nav_level_str, level):
    nav_level3 = json.loads(nav_level_str.replace("'", "\""))["SubNavigationLink"].split("|")[3].strip()
    return nav_level3


df["level1"] = df["nav_level"].map(lambda x: get_nav_level(x, 1))
df["level2"] = df["nav_level"].map(lambda x: get_nav_level(x, 2))
df["level3"] = df["nav_level"].map(lambda x: get_nav_level(x, 3))

df = df[~df["level3"].isin(['UK Regulatory News', 'All Public Company News'])]

group = df.groupby('level3')
df_group = group.size().sort_values(ascending=False)


df_group = df_group.reset_index()
df_group.columns = ['industry', 'pr_count']


print(df_group)

df_group.plot(x='industry', y='pr_count', kind="bar")
plt.show()

#plt.plot(x=df_group['industry'], y='pr_count')
#plt.legend(loc='upper left')
#plt.show()



