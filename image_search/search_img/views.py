from django.shortcuts import render, get_list_or_404
from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import View, ListView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.template import loader
import redis
import logging
from search_img.models import *
from search_img.forms import *


FORMAT = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s ' \
         u'[%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)  # filename=u'logs.log'


class SearchView(FormView):
    """
    Class for displaying the field for searching images and
    users' search history.

    Attributes:
        template_name: A template name for displaying.
    """

    template_name = 'index.html'
    form_class = SearchForm
    # success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        if 'tags' in self.request.session:
            if 'current_tag' in self.request.session:
                for item in self.request.session['tags']:
                    if self.request.session['current_tag'] in item['name'] \
                            and item['status'] == 'scheduled':
                        item['status'] = 'ready'
                        logging.debug('Set the status "' + item['status'] +
                                      '" for the tag "' +
                                      self.request.session['current_tag'] + '".')

            logging.info('Successful displaying the field for searching '
                         'images and users search history.')
            context['tag_history'] = self.request.session['tags']
        return context

    def form_invalid(self, form):
        print(form)
        return HttpResponse('invalid')

    def form_valid(self, form):
        if form.save():
            tag = form.save()
            if 'tags' in self.request.session:
                session = self.request.session['tags']
                exist = False
                for item in session:
                    if tag['name'] in item['name']:
                        exist = True
                if not exist:
                    self.request.session['tags'] = []
                    self.request.session['tags'] = session
                    self.request.session['tags'] += [{'name': tag['name'],
                                                      'status': tag['status']}]
            else:
                self.request.session['tags'] = []
                self.request.session['tags'] += [{'name': tag['name'],
                                                  'status': tag['status']}]
            self.request.session['current_tag'] = tag['name']

            logging.info('Tag "' + tag['name'] + '" is added to the session.')

            logging.info('Successful displaying users search history.')

            return render(self.request, 'all.html',
                          {'current_tag': tag['name'],
                           'tag_history': self.request.session['tags']}
                          )
        else:
            logging.error('Something went wrong.')
            # logging.error('The tag is empty.')
            return render(self.request, 'all.html', {'error': 'Enter a tag!'})


class ResultView(ListView):
    """
    Class for displaying images search results.

    Attributes:
        model: The name of the model class.
        context_object_name: Specifies the context variable to use.
        template_name: A template name for displaying.
        paginate_by: Number of elements that will be displayed on one page.
    """

    model = SearchResult
    context_object_name = 'images'
    template_name = 'result.html'
    paginate_by = 12

    def get_queryset(self):
        """
        It filters the results.

        Returns:
             A list of filtered images.
        """

        queryset = super(ResultView, self).get_queryset()
        input_tag = self.request.GET.get('tag', None)
        if input_tag is not None:
            logging.info('Successful display of results.')
            return SearchResult.objects.get_list(input_tag)
        else:
            logging.error('Empty tag!')
        return queryset
