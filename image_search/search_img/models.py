from django.db import models
from django.shortcuts import get_object_or_404, get_list_or_404


class TagManager(models.Manager):
    """
    This is the interface through which database query operations
    are provided to models.
    """

    def get_tag(self, name):
        """
        Returns the tag by name.

        Args:
            name: Tag name.

        Returns:
            The tag by name if the tag does not exist raises Http404 exception.
        """
        return get_object_or_404(Tag, name=name)

    def get_or_create_tag(self, name):
        """
        If tag is no in the database, add it.

        Args:
            name: Tag name.

        Returns:
            The tag by name if the tag does not exist raises Http404 exception.
        """
        Tag.objects.get_or_create(name=name)
        return Tag.objects.get_tag(name)


class SearchResultManager(models.Manager):
    """
    This is the interface through which database query operations
    are provided to models.
    """

    def get_list(self, name):
        """
        Get list of search results.

        Args:
            name: Tag name.

        Returns:
            The result of filter() on a given model manager
            cast to a list, raising Http404 if the resulting list is empty.
        """
        return get_list_or_404(SearchResult,
                               tag__name=name,
                               tag__status_google='ready',
                               tag__status_yandex='ready',
                               tag__status_instagram='ready')

    def get_results(self, name):
        """
        Get list of search results.

        Args:
            name: Tag name.

        Returns:
            The list of search results sorted by rank.
        """
        return SearchResult.objects.filter(tag__name=name,
                                           tag__status_google='ready',
                                           tag__status_yandex='ready',
                                           tag__status_instagram='ready'
                                           ).order_by('rank').all()


class Tag(models.Model):
    """
    Model for storing the tag names and status.

    Attributes:
        name: Tag name.
        status_google: The status of Google parsing.
        status_yandex: The status of Yandex parsing.
        status_instagram: The status of Instagram parsing.
        objects: Instance of class TagManager.
    """

    SCHEDULED = 'scheduled'
    READY = 'ready'
    STATUS_CHOICES = (
        (SCHEDULED, 'Scheduled'),
        (READY, 'Ready'),
    )
    name = models.CharField(max_length=100, unique=True)
    status_google = models.CharField(max_length=100, choices=STATUS_CHOICES,
                                     default=SCHEDULED)
    status_yandex = models.CharField(max_length=100, choices=STATUS_CHOICES,
                                     default=SCHEDULED)
    status_instagram = models.CharField(max_length=100, choices=STATUS_CHOICES,
                                        default=SCHEDULED)
    objects = TagManager()

    def __str__(self):
        return str(self.name)


class SearchResult(models.Model):
    """
    Model for storing the search results.

    Attributes:
        tag: Tag id.
        image_url: Image link.
        site: A site that has found the image.
        date: Search date.
        rank: Rank image by relevance.
        objects: Instance of class SearchResultManager.
    """

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=300)
    site = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    rank = models.PositiveIntegerField(default=1)
    objects = SearchResultManager()

    def __str__(self):
        return str(self.site)
