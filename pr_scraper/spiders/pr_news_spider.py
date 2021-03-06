# -*- coding: utf-8 -*-
from scrapy import Spider
from pr_scraper.items import IndustryItem
import json

class PRNewsSpider(Spider):
    name = 'pr_news_spider'
    allowed_urls = ['http://http://www.prnewswire.co.uk']
    start_urls = ['http://www.prnewswire.co.uk/news-releases/news-releases-list/']

    def parse(self, response):
        # rows = response.xpath('//*[@class="tier-two"]/div/table/tbody/tr')
        # //*[@id="mm-0"]/div[1]/header/div/div/nav[1]/ul/li[2]/ul/div/div/li[1]/ul
        rows = response.xpath('//*[contains(@class, "tier-two")]//*[contains(@class, "tier-four")]/a[contains(@class,"omniture-subnav")]')

        for row in rows:
            item = IndustryItem()

            item['link'] = row.xpath('./@href').extract_efirst()
            item['nav_levels'] = json.loads(row.xpath('./@data-omniture').extract_first())
            #["SubNavigationLink"]
            yield item

