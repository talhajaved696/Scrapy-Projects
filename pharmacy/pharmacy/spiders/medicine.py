# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
import json
class MedicineSpider(scrapy.Spider):
    name = 'medicine'
    
    base_url = "https://pharmeasy.in/api/otc/getCategoryProducts?categoryId=89&page="
    
    def start_requests(self):
        for i in range(1,5):
            next_page = self.base_url + str(i)
            yield scrapy.Request(url=next_page, callback=self.parse,headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"})

    def parse(self, response):
        
        print(response.url)
        data = json.loads(response.text)
        #data extraction

        for product in data['data']['products']:
            yield {
                'name': product['name'],
                'slug': product['slug'],
                'manufacturer': product['manufacturer'],
                'price': product['salePriceDecimal'],
                'availability': product['productAvailabilityFlags']['isAvailable']
                
            }
            



