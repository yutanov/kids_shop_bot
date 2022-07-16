from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
        # path('', views.index, name='home'),
        path('', views.CategoryListView.as_view(), name='home'),
        path('users/', views.UserList.as_view()),
        path('users/<int:pk>/', views.UserDetail.as_view()),
        path('login/', views.LoginView.as_view(), name='login'),
        path('logout/', views.LogoutView.as_view(), name='logout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
