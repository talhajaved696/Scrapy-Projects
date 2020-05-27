# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.crawler import CrawlerProcess

class AapartmentsSpider(scrapy.Spider):
    name = 'aapartments'
    
    header = {"USer-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
    
    def start_requests(self):
        for index in range(5):
            yield scrapy.Request(url='https://www.olx.in/api/relevance/search?category=1725&facet_limit=100&lang=en&location=1000001&location_facet_limit=20&user=1722d17ce4ex2f5a2ec&page='+str(index), callback=self.parse, headers=self.header)

    def parse(self, response):

        data = json.loads(response.text)
        
        for offer in data['data']:
            yield  {
                "Title": offer['title'],
                "Description": offer['description'].replace('\n',", "),
                "Location": offer['locations_resolved']['COUNTRY_name'] + ", " +
                            offer['locations_resolved']['ADMIN_LEVEL_1_name'] + ", " +
                            offer['locations_resolved']['ADMIN_LEVEL_3_name'],
                            #offer['locations_resolved']['SUBLOCALITY_LEVEL_1_name'],
                "Features": offer['main_info'],
                "Date": offer['display_date'],
                "Price": offer['price']['value']['display']

            }

            

# process = CrawlerProcess()
# process.crawl("AapartmentsSpider")
# process.start()

