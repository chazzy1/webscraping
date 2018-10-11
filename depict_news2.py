import pandas as pd
import json
df = pd.read_csv('./data/titles_20181008.txt', header=None, nrows=500)

df.columns = ['nav_level', 'link', 'release_date', 'title']



def get_nav_level(nav_level_str, level):
    nav_level3 = json.loads(nav_level_str.replace("'", "\""))["SubNavigationLink"].split("|")[3].strip()
    return nav_level3


#title_with_level = pd.concat([df, df.apply(lambda x: get_nav_level(x, 3)), "nav_level"], axis=1)



#print(title_with_level)
df["level1"] = df["nav_level"].map(lambda x: get_nav_level(x, 1))
df["level2"] = df["nav_level"].map(lambda x: get_nav_level(x, 2))
df["level3"] = df["nav_level"].map(lambda x: get_nav_level(x, 3))

df = df[~df["level3"].isin(['UK Regulatory News', 'All Public Company News'])]


#group = df.groupby('level3')
#print(group.size().sort_values(ascending=False))

df["release_date"] = pd.to_datetime(df["release_date"])

#df['release_date'] = df['timestamp'].apply(lambda x: "%d-%d-%d" % (x.year,x.month,x.day))

#df['release_date'] = df['timestamp'].apply(lambda x: "%d-%d" % (x.year, x.week))



time_df = df.groupby(['release_date', 'level3']).size().unstack().fillna(0)
#time_df = time_df.reset_index()

#time_df['release_date'] = pd.to_datetime(time_df["release_date"], format='%Y-%W')

#df['count'].resample('D', how='sum')

time_df = time_df.sort_values('release_date')
#time_df = time_df.set_index('release_date')


time_df = time_df.resample('M', how='sum')

print(time_df.columns)

from matplotlib import pyplot as plt

plt.plot(time_df)
plt.legend(loc='upper left')
plt.show()



