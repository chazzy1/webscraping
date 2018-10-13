import pandas as pd
from matplotlib import pyplot as plt
from utils import get_pr_news_data

"""
have to remove first, last week to do Weekly resampling. 
for these weeks, scraped data is not complete (not full week)
"""
df = get_pr_news_data()

df["week"] = df["release_date"].dt.week

print(min(df["week"]), max(df["week"]))

"""
15 41
"""

