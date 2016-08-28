from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import View, ListView, TemplateView
from django.db.models import Min, Count
from search_img.forms import *
from search_img.models import *

class SearchView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        input_tag = request.POST.get('tag', None)
        if input_tag is not None:
            try:
                tag = Tag.objects.get(name=input_tag)
            except:
                tag = Tag.objects.create(name=input_tag)
                # запуск scrapy
            images = SearchResult.objects.filter(tag__name=tag).all()
            """
            images = SearchResult.objects.raw('SELECT * FROM (Select search_img_searchresult.id, '
                                              'search_img_searchresult.site, '
                                              'search_img_searchresult.image_url, '
                                              'min(search_img_searchresult.id) '
                                              'from search_img_searchresult INNER JOIN '
                                              'search_img_tag ON '
                                              '(search_img_searchresult.tag_id = search_img_tag.id)'
                                              'where search_img_tag.name = "' + input_tag + '"'
                                              'group by search_img_searchresult.site) AS t1')
            """
            # images = SearchResult.objects.all().values('site').filter(tag__name=tag).annotate(pk=Min('id'))
            return render(request, 'index.html', {'images': images,
                                                  'tag': input_tag})
        else:
            return render(request, 'index.html', {'error': 'Enter a tag!'})
