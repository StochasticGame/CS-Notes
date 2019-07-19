#!/usr/bin/env python 
# encoding: utf-8 


"""
 Created by songyao@mail.ustc.edu.cn on 2019/4/26 下午4:08
 
 Function: 湖南湘西经济开发区门户网站
 
""" 
import random

import re
import scrapy
import sys
import time
from jishou_news.items import JishouNewsItem
from jishou_news.spiders.util import spiderUtil


class xuanjiangjiaNews(scrapy.Spider):
    name = "hnxxjjkfqNewsSpider"
    start_url = "http://www.hnxxjkq.gov.cn/"
    header = spiderUtil.header_util()

    def start_requests(self):
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/tjxx/", callback=self.parse_item_home,headers=self.header)
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/czxx/", callback=self.parse_item_home,headers=self.header)
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/ghjh/", callback=self.parse_item_home,headers=self.header)
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/rsxx/", callback=self.parse_item_home,headers=self.header)
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/zcwjjjd/flfg/", callback=self.parse_item_home,headers=self.header)
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/tzgg/", callback=self.parse_item_home,headers=self.header)
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/gzdt/", callback=self.parse_item_home,headers=self.header)
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/zfxxgknb/", callback=self.parse_item_home,headers=self.header)
        yield scrapy.Request(url="http://www.hnxxjkq.gov.cn/zwgk/zfxxgkzn/", callback=self.parse_item_home,headers=self.header)


    def parse_item_home(self, response):
        detail_urls = response.xpath("""//div[@class="content"]//a[contains(@href,'html')]//@href""").extract()
        for detail_url in detail_urls:
            time.sleep(random.uniform(1, 2))
            yield scrapy.Request(url=detail_url, callback=self.parse, headers=self.header)


    def parse(self, response):
        if response.status == 200:
            text = response.text
            html_size = sys.getsizeof(text)

            try:
                content_time = response.xpath("""//div[@class="docInfo"]""").extract()
                public_time = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", content_time[0]).group(0)

            except:
                spiderUtil.log_level(8, response.url)

            try:
                content_arr = response.xpath("""//div[@class="con1_text"]//p//text()""").extract()
                content = "".join(content_arr)
            except:
                spiderUtil.log_level(7, response.url)

            source = "http://www.hnxxjkq.gov.cn/"

            try:
                author_str = response.xpath("""//div[@class="con1_time"]//text()""").extract()[0].strip()
                author_s = author_str.split('：')[-1]
                if author_s.strip() == '':
                    author = '湘西经济开发区门户'
                else:
                    author = author_s
            except:
                spiderUtil.log_level(9, response.url)

            try:
                title = response.xpath("""//h2//text()""").extract()[0]
            except:
                spiderUtil.log_level(6, response.url)

            try:
                if content != "" and public_time.startswith(spiderUtil.get_first_hour()):
                # if content != "" :
                    item = JishouNewsItem()
                    item["source"] = source
                    item["content"] = content
                    item["public_time"] = public_time
                    item["url"] = response.url
                    item["title"] = title
                    item["author"] = author
                    item["crawl_time"] = spiderUtil.get_time()
                    item["html_size"] = html_size
                    # print(content,public_time,title,author)
                    yield item
            except:
                pass
        else:
            spiderUtil.log_level(response.status, response.url)
