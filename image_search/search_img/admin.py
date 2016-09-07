from django.contrib import admin
from search_img.models import *


class SearchResultAdmin(admin.ModelAdmin):
    """
    Class to display search results in the admin panel.

    Attributes:
        list_display: Set which fields are displayed on the change list page
        of the admin.
    """

    list_display = ['id', 'rank', 'tag', 'image_url', 'site', 'date']


class TagAdmin(admin.ModelAdmin):
    """
    Class to display the tags in the admin panel.

    Attributes:
        list_display: Set which fields are displayed on the change list page
        of the admin.
    """

    list_display = ['id', 'name', 'status_google', 'status_yandex',
                    'status_instagram']


admin.site.register(Tag, TagAdmin)
admin.site.register(SearchResult, SearchResultAdmin)
