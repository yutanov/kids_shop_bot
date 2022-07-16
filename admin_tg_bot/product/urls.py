from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('products/', views.ProductListView.as_view(), name='product_list'),
        path('products/new/', views.product_create, name='product_new'),
        # path('products/new/', views.ProductCreateView.as_view(), name='product_new'),
        # path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
        path('products/<int:pk>/edit/', views.product_update, name='product_edit'),
        # path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_view'),
        path('products/<int:pk>/', views.detail_view, name='product_view'),
        path('products/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
