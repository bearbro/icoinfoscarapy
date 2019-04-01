#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy import cmdline

# scrapy crawl itcast （itcast为爬虫名）
cmdline.execute("scrapy crawl infoSpider -a beginpage=1 -a endpage=10".split())
#线程数可以在setting.py中设置CONCURRENT_REQUESTS = 1
#若要用命令行（scrapy crawl）运行，需要先删除该文件（好像不需要）