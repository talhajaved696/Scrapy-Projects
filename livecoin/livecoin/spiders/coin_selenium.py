# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
from shutil import which
from  scrapy.selector import Selector

class CoinSeleniumSpider(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ["https://www.livecoin.net/en"]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        chrome_path = which("chromedriver")

        driver = webdriver.Chrome(executable_path = chrome_path, options = chrome_options)
        driver.set_window_size(1920,1080)
        driver.get("https://www.livecoin.net/en")

        ltc = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        ltc[4].click()
        self.html = driver.page_source
        driver.close()


    def parse(self, response):
        resp = Selector(text=self.html)
        rows = resp.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]")
        for rwo in rows:
            yield {
                'Pair':rwo.xpath(".//div[1]/div/text()").get(),
                'Volume(24h)':rwo.xpath(".//div[2]/span/text()").get()
            }
