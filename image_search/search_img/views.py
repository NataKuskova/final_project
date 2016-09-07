from django.shortcuts import render, get_list_or_404
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.views.generic import View, ListView, TemplateView
import redis
import logging
from search_img.models import *


FORMAT = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s ' \
         u'[%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename=u'logs.log')


class SearchView(TemplateView):
    """
    Class for displaying the field for searching images and
    users' search history.

    Attributes:
        template_name: A template name for displaying.
    """

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        """
        Checks whether the current tag in the session and if it has
        a 'scheduled' status, changes it to 'ready'.

        Args:
            request: The requested data.

        Returns:
            Template with users' search history.
        """
        if 'tags' in request.session:
            if 'current_tag' in request.session:
                for item in request.session['tags']:
                    if request.session['current_tag'] in item['name'] \
                            and item['status'] == 'scheduled':
                        item['status'] = 'ready'
                        logging.debug('Set the status "' + item['status'] +
                                      '" for the tag "' +
                                      request.session['current_tag'] + '".')

            logging.info('Successful displaying the field for searching '
                         'images and users search history.')
            return render(request, 'index.html',
                          {'tag_history': request.session['tags']})
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        """
        Checks the tag entered by a user, checks its availability  in
        the database, if there is no, add it to the database and redis.
        Adds the tag's name and its status into the session.

        Args:
            request: The requested data.

        Returns:
            Template with users' search history.
            If the tag is empty, returns an error message.
        """
        status = 'scheduled'
        input_tag = request.POST.get('tag', None)
        if input_tag is not None:
            try:
                tag = Tag.objects.get_tag(input_tag)
                images = SearchResult.objects.get_list(input_tag)
                status = 'ready'
                logging.info('The tag and the search results for the tag '
                             'present in the database.')
                logging.debug('Set the status "' + status +
                              '" for the tag "' + tag.name + '".')
            except:
                tag = Tag.objects.get_or_create_tag(input_tag)

                spider_list = ['google_spider',
                               'yandex_spider',
                               'instagram_spider']
                try:
                    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

                    for spider in spider_list:
                        r.lpush(spider + ':start_urls',
                                '{"tag": "' + input_tag + '", '
                                '"images_quantity": 5}')
                    logging.info('Tag "' + tag.name + '" is successfully transmitted to spiders.')

                    status = 'scheduled'
                    logging.debug('Set the status "' + status +
                                  '" for the tag "' + tag.name + '".')
                except:
                    logging.error('Something went wrong.')

            if 'tags' in request.session:
                session = request.session['tags']
                exist = False
                for item in session:
                    if input_tag in item['name']:
                        exist = True
                if not exist:
                    request.session['tags'] = []
                    request.session['tags'] = session
                    request.session['tags'] += [{'name': input_tag,
                                                 'status': status}]
            else:
                request.session['tags'] = []
                request.session['tags'] += [{'name': input_tag,
                                             'status': status}]
            request.session['current_tag'] = input_tag

            logging.info('Tag "' + input_tag + '" is added to the session.')

            logging.info('Successful displaying users search history.')
            return render(request, 'all.html',
                          {'current_tag': input_tag,
                           'tag_history': request.session['tags']}
                          )
        else:
            logging.error('The tag is empty.')
            return render(request, 'all.html', {'error': 'Enter a tag!'})


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
            return SearchResult.objects.get_results(input_tag)
        else:
            logging.error('Empty tag!')
        return queryset
