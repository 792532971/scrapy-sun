# -*- coding: utf-8 -*-
import scrapy
from sun.items import SunItem


class Sun0769Spider(scrapy.Spider):
    name = 'sun0769'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=']

    def parse(self, response):

        lists = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr")
        for list in lists:
            item = SunItem()
            item['num'] = list.xpath("./td[1]/text()").get()
            item['title'] = list.xpath("./td[2]/a[2]/@title").get()
            item['href'] = list.xpath("./td[2]/a[2]/@href").get()
            print(item['href'])
            item['guanli'] = list.xpath("./td[2]/a[3]/text()").get()
            item['status'] = list.xpath("./td[3]/span/text()").get()
            item['faqiren'] = list.xpath("./td[4]/text()").get()
            item['date_time'] = list.xpath("./td[5]/text()").get()
            yield item
            # yield scrapy.Request(item['href'], callback=self.parse_detail, meta={"item": item})
        # next = response.xpath("//div[@class='pagination']/a[5]/@href").get()
        next = response.xpath(".//a[text()='>']/@href").get()
        if next:
            yield scrapy.Request(next, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        yield item
