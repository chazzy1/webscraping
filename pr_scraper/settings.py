# -*- coding: utf-8 -*-
BOT_NAME = 'pr_scraper'

SPIDER_MODULES = ['pr_scraper.spiders']
NEWSPIDER_MODULE = 'pr_scraper.spiders'

DOWNLOAD_DELAY = 3

#ITEM_PIPELINES = {'pr_scraper.pipelines.WriteItemPipeline': 100, }
