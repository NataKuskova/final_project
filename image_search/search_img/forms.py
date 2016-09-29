from django import forms
from django.shortcuts import render, render_to_response
from search_img.models import *
import redis
import logging


FORMAT = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s ' \
         u'[%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)  # filename=u'logs.log'


class SearchForm(forms.Form):
    tag = forms.CharField(label='Enter a tag', max_length=100, required=True)

    def save(self):
        status = 'scheduled'
        current_tag = self.data.get('tag', None)
        if current_tag is not None:
            # try:
                # input_tag = Tag.objects.get_tag(current_tag)

                # images = SearchResult.objects.get_list(current_tag)

            images = SearchResult.objects.get_list_exist(current_tag)
            if images:
                status = 'ready'
                logging.info('The tag and the search results for the tag '
                             'present in the database.')
                logging.debug('Set the status "' + status +
                              '" for the tag "' + str(current_tag) + '".')
            else:
                input_tag, res = Tag.objects.get_or_create_tag(current_tag)

                spider_list = ['google_spider',
                               # 'yandex_spider',
                               'instagram_spider'
                               ]
                try:
                    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

                    for spider in spider_list:
                        r.lpush(spider + ':start_urls',
                                '{"tag": "' + str(current_tag) + '", '
                                                                 '"images_quantity": 5}')
                    logging.info('Tag "' + str(input_tag) + '" is successfully '
                                                            'transmitted to spiders.')

                    status = 'scheduled'
                    logging.debug('Set the status "' + status +
                                  '" for the tag "' + str(input_tag) + '".')
                except:
                    logging.error('Something went wrong.')
                    return False

            """
            if 'tags' in self.request.session:
                session = self.request.session['tags']
                exist = False
                for item in session:
                    if input_tag in item['name']:
                        exist = True
                if not exist:
                    self.request.session['tags'] = []
                    self.request.session['tags'] = session
                    self.request.session['tags'] += [{'name': input_tag,
                                                      'status': status}]
            else:
                self.request.session['tags'] = []
                self.request.session['tags'] += [{'name': input_tag,
                                                  'status': status}]
                self.request.session['current_tag'] = input_tag

            logging.info('Tag "' + input_tag + '" is added to the session.')

            logging.info('Successful displaying users search history.')
            """
            # return HttpResponseRedirect('index')
            return {'name': current_tag,
                    'status': status}
        # return render(self.request, 'all.html',
        #               {'current_tag': input_tag,
        #                'tag_history': self.request.session['tags']}
        #               )
        else:
            return False
