from django.test import TestCase, RequestFactory
from django.test import Client
from django.http import Http404
from datetime import datetime
from search_img.models import *
from search_img.views import *


class TagTestCase(TestCase):

    def setUp(self):
        Tag.objects.get_or_create_tag(name='minions')
        Tag.objects.get_or_create_tag(name='cat')

    def test_get_tag(self):
        with self.assertRaises(Http404):
            tag = Tag.objects.get_tag(name='nonexistent_tag')


class SearchResultTestCase(TestCase):

    def setUp(self):
        tag = Tag.objects.get_or_create_tag(name='minions')
        SearchResult.objects.create(tag=tag,
                                    image_url='https://encrypted-tbn2.'
                                              'gstatic.com/images?q=tbn:ANd9Gc'
                                              'TFOtVrw6Lzf-NulP3kmQ5BcTkCnduI'
                                              'LwZdgpgdW9F2Ty8DXr8mVQ24NwE',
                                    site='google.com.ua',
                                    date=datetime.now(),
                                    rank=1)

    def test_get_list(self):
        with self.assertRaises(Http404):
            list = SearchResult.objects.get_list(name='nonexistent_tag')

    def test_get_results(self):
        SearchResult.objects.get_results(name='minions')


class SearchViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_get_query(self):
        request = self.factory.get('')

        session = self.client.session
        session['tags'] = [{'name': 'minions',
                            'status': 'ready'}]
        session.save()
        request.session = session
        response = SearchView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_query(self):
        response = self.client.post('', {'tag': 'minions'})
        self.assertEqual(response.status_code, 200)


class ResultViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_query(self):
        tag = Tag.objects.get_or_create_tag(name='minions')
        SearchResult.objects.create(tag=tag,
                                    image_url='https://encrypted-tbn2.'
                                              'gstatic.com/images?q=tbn:ANd9Gc'
                                              'TFOtVrw6Lzf-NulP3kmQ5BcTkCnduI'
                                              'LwZdgpgdW9F2Ty8DXr8mVQ24NwE',
                                    site='google.com.ua',
                                    date=datetime.now(),
                                    rank=1)
        response = self.client.get('/result/?tag=' + tag.name)
        self.assertEqual(response.status_code, 200)
