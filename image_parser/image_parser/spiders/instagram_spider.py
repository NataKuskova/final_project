import scrapy
from image_parser.items import ImageParserItem
from scrapy_redis.spiders import RedisSpider
import redis
import json
from scrapy.http import Request
from search_img.models import *


class InstagramSpider(RedisSpider):
    """
    Class to parse instagram.com.

    Attributes:
        name: Spider name.
        allowed_domains: List of strings containing domains that this spider
        is allowed to crawl.
        start_urls: A list of URLs where the spider will begin to crawl
        from, when no particular URLs are specified.
        tag: Tag name.
        images_quantity: The number of images that need to parse.
        number: Record number counter.
        next_page: Number of the next page, if it exists.
    """

    name = 'instagram_spider'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/explore/tags/%s/']
    # tag = None
    images_quantity = 5
    # number = 1
    next_page = None
    # finish = True

    # def __init__(self):
    #     self.finish = True
    #     super(InstagramSpider, self).__init__()

    def make_request_from_data(self, data):
        """
        Make request from data.

        Args:
            data: Data.

        Returns:
            Transmits URL into the function make_requests_from_url.
        """
        # self.finish = False

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
            if quantity < self.images_quantity:
                item = ImageParserItem()
                item['image_url'] = img['display_src']
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
                    status_instagram='ready')
                r.publish('instagram', response.meta['tag'])
                return

        self.next_page = js["entry_data"]["TagPage"][0]["tag"]["media"][
            "page_info"]["has_next_page"]
        if self.next_page:
            url = response.urljoin('?max_id=' +
                                   js["entry_data"]["TagPage"][0]["tag"][
                                       "media"]["page_info"]["end_cursor"]
                                   )
            yield scrapy.Request(url, self.parse,
                                 meta={'tag': response.meta['tag'],
                                       'quantity': quantity})

