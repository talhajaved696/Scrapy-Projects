# -*- coding: utf-8 -*-
import scrapy


class OnthemarketSpider(scrapy.Spider):
    name = 'onthemarket'
    allowed_domains = ['www.onthemarket.com']
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

    def start_requests(self):
        base_url = 'https://www.onthemarket.com/for-sale/property/london/?page='
        
        for index in range(0,5):
            yield scrapy.Request(url=base_url+str(index),callback=self.parse,headers = self.header)

    def parse(self, response):
        rows = response.xpath("//li[contains(@class,'result property-result')]")
        for row in rows:
            yield{
                'Title': row.xpath(".//span[@class='title']/a/text()").get(),
                'Address': row.xpath(".//span[@class='address']/a/text()").get(),
                'Description': row.xpath(".//p[@class='description']/text()").get(),
                'Price': row.xpath("normalize-space(.//p[@class='price-text']/a/text())").get(),
                'Agency': row.xpath(".//p[@class='marketed-by']/a/text()").get(),
                'Phone': row.xpath(".//span[@class='call']/strong/text()").get(),
                'Image': row.xpath(".//picture//img/@src").get(),
            }

            
