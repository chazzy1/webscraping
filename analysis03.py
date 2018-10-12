import pandas as pd
import json

"""
reason for sparks
"""


df = pd.read_csv('./data/titles_20181008.txt', header=None, nrows=None)

df.columns = ['nav_level', 'link', 'release_date', 'title']


def get_nav_level(nav_level_str, level):
    nav_level3 = json.loads(nav_level_str.replace("'", "\""))["SubNavigationLink"].split("|")[3].strip()
    return nav_level3


df["level1"] = df["nav_level"].map(lambda x: get_nav_level(x, 1))
df["level2"] = df["nav_level"].map(lambda x: get_nav_level(x, 2))
df["level3"] = df["nav_level"].map(lambda x: get_nav_level(x, 3))


df = df[~df["level3"].isin(['UK Regulatory News', 'All Public Company News'])]

df["release_date"] = pd.to_datetime(df["release_date"])

df['day_of_week'] = df['release_date'].dt.weekday_name

group = df.groupby('day_of_week')


print(group.size())


"""
day_of_week
Friday        9370
Monday       14824
Saturday       590
Sunday         711
Thursday     17890
Tuesday      18448
Wednesday    17126
"""


