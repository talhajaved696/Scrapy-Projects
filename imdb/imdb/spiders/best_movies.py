# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    def start_requests(self):
                yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating',headers={'User-Agent':self.user_agent})
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='lister-page-next next-page']"),process_request='set_user_agent'),
    )

    def set_user_agent(self,request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'Title': response.xpath("//div[@class='title_wrapper']/h1/text()").get().strip(),
            'Year': response.xpath("//div[@class='title_wrapper']//a/text()").get(),
            'Duration': response.xpath("//time/text()").get().strip(),
            'Genre': response.xpath("//div[@class='subtext']/a/text()").get(),
            'Rating': response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'Movie_URL': response.url,
        }
