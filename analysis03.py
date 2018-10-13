import pandas as pd
from utils import get_pr_news_data

"""
found a reason for spikes
"""

df = get_pr_news_data()

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


