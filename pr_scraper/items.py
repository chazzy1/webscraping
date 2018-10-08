# -*- coding: utf-8 -*-
from scrapy import Item, Field


class IndustryItem(Item):
    link = Field()
    nav_levels = Field()


class NewsItem(Item):
    link = Field()
    title = Field()
    release_date = Field()
    levels = Field()
    content = Field()
