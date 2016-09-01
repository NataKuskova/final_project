import scrapy
from image_parser.items import ImageParserItem
from scrapy_redis.spiders import RedisSpider
from scrapy.shell import inspect_response
import json


class InstagramSpider(RedisSpider):
    name = 'instagram_spider'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/explore/tags/%s/']
    tag = None
    images_quantity = 5
    number = 1
    next_page = None

    # def __init__(self, tag=None, images_quantity=5, *args, **kwargs):
    #     super(InstagramSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = ['https://www.instagram.com/explore/tags/%s/' % tag]
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
        scripts = response.xpath(
            '//script[contains(text(), "sharedData")]/text()').re_first(
            r'window._sharedData = (.*);')
        js = json.loads(scripts)
        if self.next_page:
            images = js['entry_data']['TagPage'][0]['tag']['media']['nodes']
        else:
            images = js['entry_data']['TagPage'][0]['tag']['top_posts']['nodes']
            images += js['entry_data']['TagPage'][0]['tag']['media']['nodes']

        for img in images:
            if self.number <= self.images_quantity:
                item = ImageParserItem()
                item['image_url'] = img['display_src']
                item['site'] = 'https://' + self.allowed_domains[0]
                item['tag'] = self.tag
                item['rank'] = self.number
                self.number += 1
                yield item
            else:
                self.number = 1
                return

        self.next_page = js["entry_data"]["TagPage"][0]["tag"]["media"][
            "page_info"]["has_next_page"]
        if self.next_page:
            url = response.urljoin('?max_id=' +
                                   js["entry_data"]["TagPage"][0]["tag"][
                                       "media"]["page_info"]["end_cursor"]
                                   )
            yield scrapy.Request(url, self.parse)
