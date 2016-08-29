import scrapy
from image_parser.items import ImageParserItem
from scrapy.shell import inspect_response
import json


class InstagramSpider(scrapy.Spider):
    name = 'instagram_spider'
    allowed_domains = ['instagram.com']
    tag = None
    images_quantity = 5
    number = 1

    def __init__(self, tag=None, images_quantity=5, *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.instagram.com/explore/tags/%s/' % tag]
        self.tag = tag
        self.images_quantity = int(images_quantity)

    def parse(self, response):
        # inspect_response(response, self)
        scripts = response.xpath(
            '//script[contains(text(), "sharedData")]/text()').re_first(
            r'window._sharedData = (.*);')
        js = json.loads(scripts)
        images = js['entry_data']['TagPage'][0]['tag']['top_posts']['nodes']
        images += js['entry_data']['TagPage'][0]['tag']['media']['nodes']
        for img in images:
            if self.number <= self.images_quantity:
                item = ImageParserItem()
                item['image_url'] = img['display_src']
                item['site'] = 'https://' + self.allowed_domains[0]
                item['tag'] = self.tag
                self.number += 1
                yield item
            else:
                return False
