# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']

    def start_requests(self):
        yield SeleniumRequest(url="", callback=self.parse)

    def parse(self, response):
        pass
