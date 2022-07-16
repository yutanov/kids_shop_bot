from django.db import models

class Sale(models.Model):
    product_id = models.IntegerField(blank=False)
    product_title = models.CharField(max_length=60, blank=False)
    product_size = models.IntegerField(blank=False)
    product_color = models.CharField(max_length=60, blank=False)
    product_price = models.CharField(max_length=60, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    contacts = models.CharField(max_length=600, blank=False)
