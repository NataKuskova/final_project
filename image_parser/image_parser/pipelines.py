# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from django.shortcuts import get_object_or_404
import redis
from search_img.models import *


class ImageParserPipeline(object):
    """
    Class to store the results in a database.

    Attributes:
        num: Record number counter.
    """

    num = 1

    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component and
        stores item in database.

        Args:
            item: The item scraped.
            spider:  The spider which scraped the item.

        Returns:
            The item scraped.
        """
        tag = Tag.objects.get(name=item['tag'])
        SearchResult.objects.create(tag=tag,
                                    image_url=item['image_url'],
                                    site=item['site'],
                                    rank=item['rank'])

        if self.num == item['images_quantity']:
            r = redis.StrictRedis(host='127.0.0.1', port=6379)
            if 'google' in item['site']:
                Tag.objects.filter(name=item['tag']).update(
                    status_google='ready')
                r.publish('spiders', 'google')
            elif 'yandex' in item['site']:
                Tag.objects.filter(name=item['tag']).update(
                    status_yandex='ready')
                r.publish('spiders', 'yandex')
            else:
                Tag.objects.filter(name=item['tag']).update(
                    status_instagram='ready')
                r.publish('spiders', 'instagram')
            self.num = 1
        else:
            self.num += 1
        return item

