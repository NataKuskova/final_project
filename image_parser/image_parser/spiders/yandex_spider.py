import scrapy
from image_parser.items import ImageParserItem
from scrapy_redis.spiders import RedisSpider
import json
import redis
from scrapy.http import Request


class YandexSpider(RedisSpider):
    """
    Class to parse yandex.ua.

    Attributes:
        name: Spider name.
        allowed_domains: List of strings containing domains that this spider
        is allowed to crawl.
        start_urls: A list of URLs where the spider will begin to crawl
        from, when no particular URLs are specified.
        tag: Tag name.
        images_quantity: The number of images that need to parse.
        number: Record number counter.
    """

    name = 'yandex_spider'
    allowed_domains = ['yandex.ua']
    start_urls = ['https://yandex.ua/images/search?text=%s']
    # tag = None
    images_quantity = 5
    # number = 1

    def make_request_from_data(self, data):
        """
        Make request from data.

        Args:
            data: Data.

        Returns:
            Transmits URL into the function make_requests_from_url.
        """
        data = json.loads(data)
        if 'tag' in data and 'images_quantity' in data:
            url = self.start_urls[0] % data['tag']
            # self.tag = data['tag']
            self.images_quantity = int(data['images_quantity'])
            # return self.make_requests_from_url(url)
            return Request(url, dont_filter=True, meta={'tag': data['tag']})
        else:
            self.logger.error("Unexpected data from '%s': %r", self.redis_key,
                              data)

    def parse(self, response):
        """
        This method is in charge of processing the response and
        returning scraped data and/or more URLs to follow.

        Args:
            response: The response to parse.
        """
        quantity = response.meta.get('quantity', 0)
        images = response.xpath(
            '//div[contains(@class, "serp-item_type_search")]')
        for img in images:
            if quantity < self.images_quantity:
                item = ImageParserItem()
                item['image_url'] = 'https:' + \
                                    img.xpath('.//a/img/@src').extract()[0]
                item['site'] = 'https://' + self.allowed_domains[0]
                item['tag'] = response.meta['tag']
                item['rank'] = quantity
                # item['images_quantity'] = self.images_quantity
                quantity += 1
                yield item
            else:
                # self.number = 1
                r = redis.StrictRedis(host='127.0.0.1', port=6379)
                Tag.objects.filter(name=response.meta['tag']).update(
                    status_yandex='ready')
                r.publish('yandex', response.meta['tag'])
                return

        next_page = response.xpath(
            '//div[contains(@class, "more_direction_next")]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, self.parse,
                                 meta={'tag': response.meta['tag'],
                                       'quantity': quantity})
