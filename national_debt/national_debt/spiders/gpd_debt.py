# -*- coding: utf-8 -*-
import scrapy


class GpdDebtSpider(scrapy.Spider):
    name = 'gpd_debt'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath('//tbody/tr')
        for row in rows:
            name = row.xpath('.//td/a/text()').get()
            gdp = row.xpath('.//td[2]/text()').get()
            link = row.xpath('.//td/a/@href').get()
            
            yield response.follow(url=link,callback=self.parse_country,meta={'Name':name,'GDP':gdp})

    def parse_country(self,response):
            rows= response.xpath("(//table[@class='datatableStyles__StyledTable-bwtkle-1 cyosFW table table-striped'])[2]/tbody/tr[1]")
            for row in rows:
                name = response.request.meta['Name']
                gdp = response.request.meta['GDP']
                year = row.xpath('.//td[1]/text()').get()
                Pop = row.xpath('.//td[2]/text()').get()
                
                yield{
                    'Name':name,
                    'Year':year,
                    'GDP':gdp,
                    'Population':Pop
                }