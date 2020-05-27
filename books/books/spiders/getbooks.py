# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GetbooksSpider(CrawlSpider):
    name = 'getbooks'
    allowed_domains = ['books.toscrape.com']
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com',headers={'User-Agent':self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), process_request='set_user_agent'),
    )

    def set_user_agent(self,request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'Title':response.xpath("//h1/text()").get(),
            'Price':response.xpath("//p[@class='price_color']/text()").get()
        }
