from django.db import models
from django.shortcuts import get_object_or_404, get_list_or_404


class TagManager(models.Manager):

    def get_tag(self, name):
        return get_object_or_404(Tag, name=name)

    def update_tag(self, name):
        return Tag.objects.filter(name=name).update(status='ready')

    def get_or_create_tag(self, name):
        Tag.objects.get_or_create(name=name)
        return Tag.objects.get_tag(name)


class SearchResultManager(models.Manager):

    def get_list(self, name):
        return get_list_or_404(SearchResult, tag__name=name, tag__status='ready')

    def get_results(self, name):
        return SearchResult.objects.filter(tag__name=name, tag__status='ready').order_by('rank').all()


class Tag(models.Model):
    SCHEDULED = 'scheduled'
    READY = 'ready'
    STATUS_CHOICES = (
        (SCHEDULED, 'Scheduled'),
        (READY, 'Ready'),
    )
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,
                              default=SCHEDULED)
    objects = TagManager()

    def __str__(self):
        return str(self.name)


class SearchResult(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=300)
    site = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    rank = models.PositiveIntegerField(default=1)
    objects = SearchResultManager()

    def __str__(self):
        return str(self.site)
