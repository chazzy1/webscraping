import pandas as pd
import json
titles = pd.read_csv('./data/titles_20181008.txt', header=None, nrows=None)

titles.columns = ['nav_level', 'link', 'release_date', 'title']



def get_nav_level(nav_level_str, level):
    nav_level3 = json.loads(nav_level_str.replace("'", "\""))["SubNavigationLink"].split("|")[3].strip()
    return nav_level3


#title_with_level = pd.concat([titles, titles.apply(lambda x: get_nav_level(x, 3)), "nav_level"], axis=1)



#print(title_with_level)
titles["level1"] = titles["nav_level"].map(lambda x: get_nav_level(x, 1))
titles["level2"] = titles["nav_level"].map(lambda x: get_nav_level(x, 2))
titles["level3"] = titles["nav_level"].map(lambda x: get_nav_level(x, 3))

#group = titles.groupby('level3')
#print(group.size())

titles["timestamp"] = pd.to_datetime(titles["release_date"])

titles['release_date'] = titles['timestamp'].apply(lambda x: "%d-%d-%d" % (x.year,x.month,x.day))




time_df = titles.groupby(['release_date', 'level3']).size().unstack().fillna(0)
time_df = time_df.reset_index()

time_df['release_date'] = pd.to_datetime(time_df["release_date"])
time_df = time_df.sort_values('release_date')
#print(time_df)
time_df = time_df.set_index('release_date')

print(time_df)

from matplotlib import pyplot as plt

plt.plot(time_df)
plt.show()
"""
sample_data = pd.DataFrame(titles, columns=['release_date', 'level3']).head(100)
sample_data = sample_data[sample_data['level3'] == 'Travel']
"""




#time_df.plot(x='release_date')


#print(group.agg(['count']))

