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

"""

                                        industry  pr_count
0                              Computer Software      5610
1                           Computer Electronics      5149
2                         Computer & Electronics      5149
3                    Surveys, Polls and Research      3988
4                        New Products & Services      2666
5                        Health Care & Hospitals      2561
6                                       Networks      2495
7                            Aerospace & Defence      2242
8                        Medical Pharmaceuticals      2154
9                   Banking & Financial Services      2097
10                          Financial Technology      1602
11                                Data Analytics      1452
12                                    Blockchain      1298
13                                      Chemical      1236
14                               Trade Show News      1149
15                           Internet Technology      1117
16                           Electronic Commerce      1104
17                               Pharmaceuticals       988
18             Publishing & Information Services       979
19                          Mobile Entertainment       972
20                         Multimedia & Internet       964
21                                     Contracts       923
22                               Mining & Metals       800
23                             Medical Equipment       793
24                             Computer Hardware       779
25           Transportation, Trucking & Railroad       753
26                                        Retail       694
27                                        Awards       691
28                                    Automotive       642
29                   Telecommunications Industry       617
..                                           ...       ...
147                                  Air Freight        31
148                         Environmental Policy        28
149                                      Tobacco        28
150                Overseas Real Estate (non-US)        24
151                     Real Estate Transactions        23
152                                         Toys        23
153                                        Radio        22
154                         Shareholder Activism        21
155                             Health Insurance        20
156             Restructuring & Recapitalization        18
157                                     Religion        17
158                              Senior Citizens        14
159          VoIP (Voice over Internet Protocol)        14
160                      Oil and Gas Discoveries        14
161                                     Hispanic        13
162                            Leisure & Tourism        10
163                      Lesbian, Gay & Bisexual         9
164                                 Mutual Funds         9
165                              Bridal Services         5
166                                     Disabled         5
167                             African American         3
168  Aboriginal, First Nations & Native American         3
169                                  Stock Split         3
170               Socially Responsible Investing         3
171                                   Bankruptcy         3
172                                   Obituaries         3
173                         Bond & Stock Ratings         2
174                                     Veterans         1
175                                Labor & Union         1
176                              Product Recalls         1


"""

