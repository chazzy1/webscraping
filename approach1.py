from bs4 import BeautifulSoup
import requests


# http://www.prnewswire.co.uk/news-releases/automotive-transportation-latest-news/aerospace-defense-list/?c=n&page=2&pagesize=25
# http://www.prnewswire.co.uk/news-releases/news-releases-list/

"""
text = requests.get('http://www.prnewswire.co.uk/news-releases/automotive-transportation-latest-news/aerospace-defense-list/?c=n&page=2&pagesize=25').text
text = BeautifulSoup(text, 'html.parser')


date_texts = text.find_all('small')

print (date_texts)
"""


def get_industry_list():
    url_industry_list = "http://www.prnewswire.co.uk/news-releases/news-releases-list/"
    html_text = requests.get(url_industry_list).text
    html_bs4 = BeautifulSoup(html_text, 'html.parser')

    sub_navigation_link = html_bs4.find_all('a',{"class":"omniture-subnav"})

    print(sub_navigation_link)


get_industry_list()
