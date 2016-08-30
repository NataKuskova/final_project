from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class SearchResult(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=300)
    site = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.site)
