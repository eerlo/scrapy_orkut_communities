# -*- coding: utf-8 -*-
import scrapy
from scrapy_orkut_communities.items import ScrapyOrkutCommunitiesItem
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url

class OrkutCommunitiesSpider(scrapy.Spider):
    name = "orkut_communities"
    #allowed_domains = ["https://orkut.google.com/"]
    start_urls = (
        'http://orkut.google.com/',
    )

    def parse(self, response):
        letters = response.xpath('/html/body/div[5]/div/a/@href').extract()

        for l in letters:
            link = urljoin_rfc(get_base_url(response), l)
            yield scrapy.Request(link, callback=self.parse_letter)

    def parse_letter(self, response):
        items = response.css('.innerContainer .listCommunityContainer')
        for i in items[1:-1]:
            link = i.css('a').xpath('@href').extract()[0]
            link = urljoin_rfc(get_base_url(response), link)
            yield scrapy.Request(link, callback=self.parse_detail)

        next_page = response.xpath("//a[text()='next >']/@href").extract()
        for np in next_page:
            link = urljoin_rfc(get_base_url(response), np)
            yield scrapy.Request(link, callback=self.parse_letter)
            break

    def parse_detail(self, response):
        name = response.css('.commonHeader .archiveMessage')[0].\
            xpath('text()').extract()[0]


        url = get_base_url(response)

        return ScrapyOrkutCommunitiesItem(name=name, url=url)
