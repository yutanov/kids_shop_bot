from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
        path('categories/', views.CategoryListView.as_view(), name='category_list'),
        path('category/new/', views.CategoryCreateView.as_view(), name='category_new'),
        path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
        path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_view'),
        path('categories/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category_delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
