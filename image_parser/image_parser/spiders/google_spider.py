import scrapy
from image_parser.items import ImageParserItem
from scrapy_redis.spiders import RedisSpider
from scrapy.shell import inspect_response


class GoogleSpider(RedisSpider):
    name = 'google_spider'
    allowed_domains = ['google.com.ua']
    tag = None
    images_quantity = 5
    number = 1

    def __init__(self, tag=None, images_quantity=5, *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'https://www.google.com.ua/search?site=imghp&tbm=isch&q=%s&oq=%s' %
            (tag, tag)
        ]
        self.tag = tag
        self.images_quantity = int(images_quantity)

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
                self.number += 1
                yield item
            else:
                return False

        next_page = response.xpath(
            '//table[contains(@id, "nav")]//tr/td[last()]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, self.parse)
