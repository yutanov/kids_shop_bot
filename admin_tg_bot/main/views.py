from django.shortcuts import render
from rest_framework import generics
from . import serializers
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout
from django.views import generic
from django.apps import apps


Category = apps.get_model('category', 'Category')


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "index.html"
    success_url = "/"

    def form_valid(self, form):
        messages.success(self.request, 'YouIn')
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(self.request, 'YouOut')
        return HttpResponseRedirect("/")


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'index.html'


def index(request):
    return render(request, 'index.html')
