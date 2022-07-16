from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('location/', views.RegionListView.as_view(), name='region_list'),
    path('location/new/', views.RegionCreateView.as_view(), name='region_new'),
    path('location/<int:pk>/edit/', views.RegionUpdateView.as_view(), name='region_edit'),
    path('location/<int:pk>/', views.RegionDetailView.as_view(), name='region_view'),
    path('location/<int:pk>/delete', views.RegionDeleteView.as_view(), name='region_delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
