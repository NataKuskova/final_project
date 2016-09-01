from django.shortcuts import render, get_list_or_404
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import View, ListView, TemplateView
import redis
from search_img.models import *


class SearchView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if 'tags' in request.session:
            return render(request, 'index.html',
                          {'tag_history': request.session['tags']})
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        input_tag = request.POST.get('tag', None)
        if input_tag is not None:
            try:
                tag = Tag.objects.get_tag(input_tag)
                images = SearchResult.objects.get_list(input_tag)
            except:
                tag = Tag.objects.get_or_create_tag(input_tag)

                r = redis.StrictRedis(host='localhost', port=6379, db=0)
                r.lpush('google_spider:start_urls',
                        '{"tag": "' + input_tag + '", "images_quantity": 5}')
                r.lpush('yandex_spider:start_urls',
                        '{"tag": "' + input_tag + '", "images_quantity": 5}')
                r.lpush('instagram_spider:start_urls',
                        '{"tag": "' + input_tag + '", "images_quantity": 5}')
                # пока не знаю где это проверять
                if not r.llen('google_spider:start_urls') and not r.llen(
                        'yandex_spider:start_urls') and not r.llen(
                        'instagram_spider:start_urls'):
                    Tag.objects.update_tag(input_tag)

            if 'tags' in request.session:
                session = request.session['tags']
                if input_tag not in session:
                    request.session['tags'] = []
                    request.session['tags'] = session
                    request.session['tags'].append({'name': input_tag,
                                                    'status': tag.status})
            else:
                request.session['tags'] = []
                request.session['tags'].append({'name': input_tag,
                                                'status': tag.status})
            return render(request, 'index.html',
                          {'current_tag': input_tag,
                           'tag_history': request.session['tags']}
                          )
        else:
            return render(request, 'index.html', {'error': 'Enter a tag!'})


class ResultView(ListView):
    model = SearchResult
    context_object_name = 'images'
    template_name = 'result.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = super(ResultView, self).get_queryset()
        input_tag = self.request.GET.get('tag', None)
        if input_tag is not None:
            return SearchResult.objects.get_results(input_tag)
        return queryset
