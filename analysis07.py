import pandas as pd
import json
import numpy as np

from matplotlib import pyplot as plt

"""
get the slope
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




time_df = df.groupby(['release_date', 'level3']).size().unstack().fillna(0)
time_df = time_df.resample('D').sum()

time_df = time_df[time_df.index.dayofweek < 5].stack()
time_df = pd.DataFrame(time_df).reset_index()
#time_df = time_df.reset_index('release_date')
time_df.columns = ['release_date', 'level3', 'pr_count']


def trend_line(data, order=1):
    coeffs = np.polyfit(range(len(data.index)), data, order)
    slope = coeffs[0]
    return float(slope)

slope_df = pd.DataFrame(time_df.groupby('level3').apply(lambda x: trend_line(x.pr_count)))

slope_df.columns = ['slope']
slope_df = slope_df.sort_values('slope', ascending=False)
print(slope_df)


slope_df.plot(y='slope', kind="bar")
plt.show()




"""

                                            slope
level3                                           
Data Analytics                           0.023742
Mobile Entertainment                     0.021813
Peripherals                              0.015871
Cannabis                                 0.014796
Financial Technology                     0.014587
STEM (Science, Tech, Engineering, Math)  0.012750
Household, Consumer & Cosmetics          0.010083
Supplementary Medicine                   0.007023
Beverages                                0.006968
Agriculture                              0.006132
High Tech Security                       0.005469
Electronic Design Automation             0.005296
Transportation, Trucking & Railroad      0.004891
Magazines                                0.004006
Outdoors, Camping & Hiking               0.004006
Trucking and Road Transportation         0.004000
Food & Beverages                         0.004000
Contracts                                0.003994
Green Technology                         0.003963
Non-Alcoholic Beverages                  0.003926
Cosmetics and Personal Care              0.002986
Tobacco                                  0.002888
Organic Food                             0.002513
Environmental                            0.002409
Environmental Products & Services        0.002237
Insurance                                0.002101
Natural Disasters                        0.002065
Amusement Parks and Tourist Attractions  0.001806
Corporate Expansion                      0.001555
Corporate Social Responsibility          0.001481
...                                           ...
Investments Opinions                    -0.006138
Outsourcing Businesses                  -0.006138
Art                                     -0.006556
Medical Pharmaceuticals                 -0.006802
Multimedia & Internet                   -0.008301
Travel Industry                         -0.008522
Travel                                  -0.008522
Airlines & Aviation                     -0.008596
Entertainment                           -0.009057
Acquisitions, Mergers and Takeovers     -0.009616
Pharmaceuticals                         -0.010151
Sporting Events                         -0.010747
Banking & Financial Services            -0.010777
Automotive                              -0.011029
General Sports                          -0.011601
Accounting News & Issues                -0.011717
Aerospace & Defence                     -0.012676
Conference Call Announcements           -0.013026
New Products & Services                 -0.017892
Electronic Commerce                     -0.020190
France Regulatory News                  -0.020682
Computer Software                       -0.021186
Blockchain                              -0.023275
Mining                                  -0.025413
Internet Technology                     -0.026949
Mining & Metals                         -0.029886
Earnings                                -0.031914
Computer Electronics                    -0.032614
Networks                                -0.032627
Computer & Electronics                  -0.032879


"""