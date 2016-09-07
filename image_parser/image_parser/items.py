# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class ImageParserItem(Item):
    """
    Class for define the fields for item.

    Attributes:
        image_url: Image link.
        site: A site that has found the image.
        tag: Tag name.
        date: Search date.
        rank: Rank image by relevance.
        images_quantity: The number of images.
    """

    image_url = Field()
    site = Field()
    tag = Field()
    date = Field()
    rank = Field()
    images_quantity = Field()
