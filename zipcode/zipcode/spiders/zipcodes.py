# -*- coding: utf-8 -*-
import scrapy
import urllib
import json

class ZipcodesSpider(scrapy.Spider):
    name = 'zipcodes'
    base_url = "https://rest-api.immoscout24.ch/v4/en/locations?"
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

    def start_requests(self):
        zipc = ''
        with open('zipcode.txt','r') as f:
            for line in f.read():
                zipc+=line

        zipcodes = zipc.split("\n")
        for zipcode in zipcodes:
            next_ = self.base_url + urllib.parse.urlencode({'term':str(zipcode)})
            yield scrapy.Request(url=next_, callback=self.parse, headers=self.header)
            

    def parse(self, response):
        try:
            data = json.loads(response.text)
            label = 'postcode-' + data[0]['label'].replace(' ','-').lower()

            with open('label.txt','a') as f:
                f.write(label + '\n')

            yield data[0]
        except :
            pass        

