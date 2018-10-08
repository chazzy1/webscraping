# -*- coding: utf-8 -*-
from scrapy import Spider
from pr_scraper.items import IndustryItem
from pr_scraper.items import NewsItem
import scrapy
import json
import urllib.parse

class NewsSpider(Spider):
    name = 'news_spider'
    allowed_urls = ['http://http://www.prnewswire.co.uk']
    #start_urls = ['http://www.prnewswire.co.uk/news-releases/consumer-technology-latest-news/science-tech-engineering-math-list/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'pr_scraper.pipelines.WriteNewsItemPipeline': 400
        }
    }

    start_urls = ['http://www.prnewswire.co.uk/news-releases/news-releases-list/']


    def join_page_number(self, response, url, page_number):
        page_get_param = "?c=n&page={}&pagesize=25".format(page_number)
        rel_url = urllib.parse.urljoin(url, page_get_param)
        absolute_page_url = response.urljoin(rel_url)

        return absolute_page_url


    def parse(self, response):
        # rows = response.xpath('//*[@class="tier-two"]/div/table/tbody/tr')
        # //*[@id="mm-0"]/div[1]/header/div/div/nav[1]/ul/li[2]/ul/div/div/li[1]/ul
        rows = response.xpath('//a[@class="omniture-subnav"]')

        industries = []

        for row in rows:
            item = IndustryItem()
            item['link'] = row.xpath('./@href').extract_first()
            item['nav_levels'] = json.loads(row.xpath('./@data-omniture').extract_first())
            industries.append(item)

        for industry in industries:
            absolute_page_url = response.urljoin(industry['link'])

            # test only
            #if "Women" not in str(industry['nav_levels']):
            #    continue

            yield scrapy.Request(absolute_page_url, callback=self.parse_news_list, meta={'industry': industry})

            # test only
            #break

    def parse_news_list(self, response):
        """

        :param response:
        :return:
        """
        rows = response.xpath('//a[@class="news-release"]')
        meta = response.meta
        meta['page_number'] = meta.get('page_number', 1)

        rows = response.xpath('//*[@id="main"]/section[3]/div/div[1]/div[@class="row"]')
        if len(rows) > 0:
            for row in rows:
                item = NewsItem()

                item['link'] = row.xpath('.//a[@class="news-release"]/@href').extract_first()
                item['title'] = row.xpath('.//a[@class="news-release"]/@title').extract_first()
                item['release_date'] = row.xpath('.//small/text()').extract_first().strip()
                item['levels'] = meta['industry']['nav_levels']
                yield item
                #yield scrapy.Request(item['link'], callback=self.parse_news_content, meta={'item': item})
            meta['page_number'] += 1
            absolute_page_url = self.join_page_number(response, meta['industry']["link"], meta['page_number'])

            yield scrapy.Request(absolute_page_url, callback=self.parse_news_list, meta=meta)

    def parse_news_content(selfself, response):
        """
        :param response:
        :return: NewsItem
        """

        item = response.meta['item']
        item["content"] = response.xpath('//section[@itemprop="articleBody"]').extract_first()

        yield item
