from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
        path('sales', views.sales_view, name='sales'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
