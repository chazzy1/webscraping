# -*- coding: utf-8 -*-
from scrapy import Item, Field

class IndustryItem(Item):
	link = Field()
	nav_levels = Field()