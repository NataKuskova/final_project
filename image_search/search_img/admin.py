from django.contrib import admin
from search_img.models import *


class SearchResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'rank', 'tag', 'image_url', 'site', 'date']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


admin.site.register(Tag, TagAdmin)
admin.site.register(SearchResult, SearchResultAdmin)
