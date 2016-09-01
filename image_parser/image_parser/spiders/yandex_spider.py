import scrapy
from image_parser.items import ImageParserItem
from scrapy_redis.spiders import RedisSpider
from scrapy.shell import inspect_response
import json


class YandexSpider(RedisSpider):
    name = 'yandex_spider'
    allowed_domains = ['yandex.ua']
    start_urls = ['https://yandex.ua/images/search?text=%s']
    tag = None
    images_quantity = 5
    number = 1

    # def __init__(self, tag=None, images_quantity=5, *args, **kwargs):
    #     super(YandexSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = ['https://yandex.ua/images/search?text=%s' % tag]
    #     self.tag = tag
    #     self.images_quantity = int(images_quantity)

    def make_request_from_data(self, data):
        data = json.loads(data)
        if 'tag' in data and 'images_quantity' in data:
            url = self.start_urls[0] % data['tag']
            self.tag = data['tag']
            self.images_quantity = int(data['images_quantity'])
            return self.make_requests_from_url(url)
        else:
            self.logger.error("Unexpected data from '%s': %r", self.redis_key,
                              data)

    def parse(self, response):
        # inspect_response(response, self)
        images = response.xpath(
            '//div[contains(@class, "serp-item_type_search")]')
        for img in images:
            if self.number <= self.images_quantity:
                item = ImageParserItem()
                item['image_url'] = 'https:' + img.xpath('.//a/img/@src').extract()[0]
                item['site'] = 'https://' + self.allowed_domains[0]
                item['tag'] = self.tag
                item['rank'] = self.number
                self.number += 1
                yield item
            else:
                self.number = 1
                return

        next_page = response.xpath(
            '//div[contains(@class, "more_direction_next")]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, self.parse)