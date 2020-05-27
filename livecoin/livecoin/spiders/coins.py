# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class CoinsSpider(scrapy.Spider):
    name = 'coins'
    allowed_domains = ['www.livecoin.net/en']
    
    script = '''function main(splash, args)
                    splash.private_mode_enabled = false
                    assert(splash:go(args.url))
                    assert(splash:wait(1))
                    usd_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
                    usd_tab[5]:mouse_click()  
                    assert(splash:wait(1))
                    splash:set_viewport_full()
                    
                    return {
                        html = splash:html()
                    }
                end'''

    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en",callback=self.parse,endpoint="execute",args={
            'lua_source':self.script
        })

    def parse(self, response):
        rows = response.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]")
        for rwo in rows:
            yield {
                'Pair':rwo.xpath(".//div[1]/div/text()").get(),
                'Volume(24h)':rwo.xpath(".//div[2]/span/text()").get()
            }
