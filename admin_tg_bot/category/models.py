from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=60, unique=True, blank=True, default='')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_view', args=[str(self.id)])
