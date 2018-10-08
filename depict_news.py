import pandas as pd
import json
titles = pd.read_csv('titles_20181008.txt', header=None)

titles.columns = ['nav_level', 'link', 'release_date', 'title']



def get_nav_level(nav_level_str, level):
    nav_level3 = json.loads(nav_level_str.replace("'", "\""))["SubNavigationLink"].split("|")[3].strip()
    return nav_level3


#title_with_level = pd.concat([titles, titles.apply(lambda x: get_nav_level(x, 3)), "nav_level"], axis=1)



#print(title_with_level)
titles["level1"] = titles["nav_level"].map(lambda x: get_nav_level(x, 1))
titles["level2"] = titles["nav_level"].map(lambda x: get_nav_level(x, 2))
titles["level3"] = titles["nav_level"].map(lambda x: get_nav_level(x, 3))

group = titles.groupby('level3')
print(group.size())