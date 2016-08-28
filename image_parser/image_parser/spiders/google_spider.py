import scrapy
from image_parser.items import ImageParserItem


class GoogleSpider(scrapy.Spider):
    name = 'google_spider'
    allowed_domains = ['google.com.ua']
    tag = None
    images_quantity = 10
    number = 1

    def __init__(self, tag=None, images_quantity=None, *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'https://www.google.com.ua/search?site=imghp&tbm=isch&q=%s&oq=%s' %
            (tag, tag)
        ]
        self.tag = tag
        self.images_quantity = int(images_quantity)

    def parse(self, response):
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
                break
