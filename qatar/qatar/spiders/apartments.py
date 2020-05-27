# -*- coding: utf-8 -*-
import scrapy
import urllib

class ApartmentsSpider(scrapy.Spider):
    name = 'apartments'
    base_url = "https://www.qatarliving.com/classifieds/properties/apartment?"
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

    def start_requests(self):
        
        for page in range(0,112):
            next_page = self.base_url + urllib.parse.urlencode({'page': str(page)})
            yield scrapy.Request(url=next_page,callback=self.parse,headers=self.header)
            break

    def parse(self, response):
        items = response.xpath("//span[@class='b-card b-card-mod-h property']")
        for item in items:
            yield {
                'Type': item.xpath(".//div[@class='b-card--el-details']/p/text()").get().split(", ")[0],
                'Price': ' '.join(item.xpath(".//div[@class='b-card--el-price-conditions ']/p/text()").getall()),
                'Address': item.xpath(".//div[@class='b-card--el-details']/p/text()").get().split(", ")[-1],
                'Description': item.xpath(".//p[@class='b-card--el-description']/text()").get(),
                'Bedrooms': item.xpath(".//div[@class='b-feature bedroom bedroom-mod-small']/p/text()").get(),
                'Bathrooms': item.xpath(".//div[@class='b-feature bathroom bathroom-mod-small']/p/text()").get(),
                'Agency_Name': item.xpath(".//a[@class='b-card--el-agency-title']/text()").get(),
                'Agency_Link': 'https://www.qatarliving.com' + item.xpath(".//a[@class='b-card--el-agency-title']/@href").get(),
                'Images': item.xpath(".//div[@class='b-card--el-header']/a/img/@src").get(),
            }
