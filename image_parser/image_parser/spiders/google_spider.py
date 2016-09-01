import scrapy
from image_parser.items import ImageParserItem
from scrapy_redis.spiders import RedisSpider
from scrapy.shell import inspect_response
import json


class GoogleSpider(RedisSpider):
    name = 'google_spider'
    allowed_domains = ['google.com.ua']
    start_urls = [
        'https://www.google.com.ua/search?site=imghp&tbm=isch&q=%s&oq=%s']
    tag = None
    images_quantity = 5
    number = 1
    page_number = 1
    i = 0

    # def __init__(self, tag=None, images_quantity=5, *args, **kwargs):
    #     super(GoogleSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = [
    #         'https://www.google.com.ua/search?site=imghp&tbm=isch&q=%s&oq=%s' %
    #         (tag, tag)
    #     ]
    #     self.tag = tag
    #     self.images_quantity = int(images_quantity)

    def make_request_from_data(self, data):
        data = json.loads(data)
        if 'tag' in data and 'images_quantity' in data:
            url = self.start_urls[0] % (data['tag'], data['tag'])
            self.tag = data['tag']
            self.images_quantity = int(data['images_quantity'])
            return self.make_requests_from_url(url)
        else:
            self.logger.error("Unexpected data from '%s': %r", self.redis_key,
                              data)

    def parse(self, response):
        # inspect_response(response, self)
        images = response.xpath(
            '//table[contains(@class, "images_table")]//a//img')
        for img in images:
            if self.number <= self.images_quantity:
                item = ImageParserItem()
                item['image_url'] = img.xpath('@src').extract()[0]
                item['site'] = 'https://' + self.allowed_domains[0]
                item['tag'] = self.tag
                # if self.page_number > 1 and self.number <= 20:
                #     item['rank'] = self.page_number * 10 + self.number + self.i
                # else:
                item['rank'] = self.number
                self.number += 1
                yield item
            else:
                self.number = 1
                return
        # if self.page_number > 1 and self.number <= 20:
        #     self.i += 10
        next_page = response.xpath(
            '//table[contains(@id, "nav")]//tr/td[last()]/a/@href').extract()
        if next_page:
            # self.page_number += 1
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, self.parse)

