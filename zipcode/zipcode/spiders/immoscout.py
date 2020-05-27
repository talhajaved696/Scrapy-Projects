import scrapy
import urllib
import json
from scrapy_selenium import SeleniumRequest

class ImmoscoutSpider(scrapy.Spider):
        name = 'immoscout'
        base_url = 'https://www.immoscout24.ch/en/real-estate/rent/'
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        params = {
         'pn':'1',
          'r':0
        }  
        def start_requests(self):
                zipcodes = ""
                with open('label.txt','r') as f:
                        for line in f.read():
                                zipcodes+=line
                zips = zipcodes.split("\n")
                for zipcode in zips:
                        url = 'https://www.immoscout24.ch/en/real-estate/rent/' + zipcode + '?pn=1&r=0' 
                        yield SeleniumRequest(url=url,wait_time=3, callback=self.parse, headers=self.header)
                        

            

        def parse(self, response):
                print(response.url)
                for card in response.css('div[class="sc-18zf79l-0 cpuXZS"]'):
            # property features
                        yield {
                                'title': card.css('h2[class="bkivry-0 csYOrJ qjwil1-6 iCnXmG"]::text')
                                        .getall()[1],
                                
                                'details': ''.join(card.css('h3[class="bkivry-0 kXCbXB qjwil1-5 iCnXmF"] *::text')
                                                .getall()),
                                
                                'address': card.css('div[class="qjwil1-7 iCnXmH"]')
                                        .css('a[class="bkivry-0 sc-1u0if05-0 eKnuaM"] *::text')
                                        .get(),
                                
                                'price': card.css('h3[class="bkivry-0 eDrwLl"]::text')
                                        .get(),
                                
                                'image': card.css('div[class="r5r22j-0 loCtpM swiper-slide"]')
                                        .css('img::attr(src)')
                                        .get()
                                
                        }
                next_page = response.xpath("//div[@class='bkivry-0 j3cl20-0 bGnbFY']/a/@href").get()
                if next_page:
                        abs = f'https://www.immoscout24.ch{next_page}'
                        yield SeleniumRequest(url=abs,wait_time=3,callback=self.parse)


