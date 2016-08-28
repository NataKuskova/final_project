import scrapy
from image_parser.items import ImageParserItem
from scrapy.shell import inspect_response


class YandexSpider(scrapy.Spider):
    name = 'yandex_spider'
    allowed_domains = ['yandex.ua']
    tag = None
    images_quantity = 10
    number = 1

    def __init__(self, tag=None, images_quantity=None, *args, **kwargs):
        super(YandexSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://yandex.ua/images/search?text=%s' % tag]
        self.tag = tag
        self.images_quantity = int(images_quantity)

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
                self.number += 1
                yield item
            else:
                break
