from django.contrib import admin
from search_img.models import *


class SearchResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag', 'image_url', 'site']


admin.site.register(Tag)
admin.site.register(SearchResult, SearchResultAdmin)
