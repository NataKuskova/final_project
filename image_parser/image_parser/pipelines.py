# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from django.shortcuts import get_object_or_404
from search_img.models import *


class ImageParserPipeline(object):
    def process_item(self, item, spider):
        tag = Tag.objects.get(name=item['tag'])
        SearchResult.objects.create(tag=tag,
                                    image_url=item['image_url'],
                                    site=item['site'],
                                    rank=item['rank'])
        return item
