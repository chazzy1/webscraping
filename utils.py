import pandas as pd
import json
import numpy as np

def trend_line(data, order=1):
    """
    returns numpy polypit coefficient
    :param data:
    :param order:
    :return:
    """
    coeffs = np.polyfit(range(len(data.index)), data, order)
    slope = coeffs[0]
    return float(slope)


def get_nav_level(nav_level_str, level):
    """
    :param nav_level_str:
    :param level:
    :return nav_level_str for specified level:
    """
    return json.loads(nav_level_str.replace("'", "\""))["SubNavigationLink"].split("|")[level].strip()



def get_pr_news_data(file_path='./data/titles_20181008.txt', nrows=None):
    """
    returns pr_news_title dataframe.
    columns are ['nav_level', 'link', 'release_date', 'title']
    timezone warning is neglectable for analysis.
    :param file_path:
    :param nrows:
    :return pr_news_titles dataframe:
    """
    df = pd.read_csv(file_path, header=None, nrows=nrows)
    df.columns = ['nav_level', 'link', 'release_date', 'title']
    df["level1"] = df["nav_level"].map(lambda x: get_nav_level(x, 1))
    df["level2"] = df["nav_level"].map(lambda x: get_nav_level(x, 2))
    df["level3"] = df["nav_level"].map(lambda x: get_nav_level(x, 3))
    df["release_date"] = pd.to_datetime(df["release_date"])
    df = df.sort_values('release_date')

    return df[~df["level3"].isin(['UK Regulatory News', 'All Public Company News', 'Computer & Electronics'])]


