from django.shortcuts import render, get_list_or_404
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import View, ListView, TemplateView
from django.db.models import Min, Count
import subprocess
from search_img.forms import *
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
                tag = Tag.objects.get(name=input_tag)
                images = get_list_or_404(SearchResult, tag__name=input_tag)
            except:
                tag = Tag.objects.get_or_create(name=input_tag)
                spiders = ['google_spider', 'yandex_spider',
                           'instagram_spider']
                for spider in spiders:
                    process = subprocess.Popen(
                        'scrapy crawl ' + spider + ' -a tag=' + input_tag +
                        ' -a images_quantity=5',
                        cwd=r'/home/user/Nata/PycharmProjects/final_project/image_parser/image_parser',
                        shell=True,
                        stdout=subprocess.PIPE
                    )
                    out = process.communicate()
                    print(out)

            if 'tags' in request.session:
                session = request.session['tags']
                if input_tag not in session:
                    request.session['tags'] = []
                    request.session['tags'] = session
                    request.session['tags'].append(input_tag)
            else:
                request.session['tags'] = []
                request.session['tags'].append(input_tag)
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
            # images = SearchResult.objects.all().values('site').filter(tag__name=tag).annotate(pk=Min('id'))
            return queryset.filter(tag__name=input_tag).all()
        return queryset
