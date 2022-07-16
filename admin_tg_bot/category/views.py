from django.views import generic
from .models import Category
from django.urls import reverse_lazy
from django.apps import apps

Product = apps.get_model('product', 'Product')


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'category/categories.html'


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.objects.filter(category=self.object.id)
        return context


class CategoryCreateView(generic.CreateView):
    model = Category
    template_name = 'category/category_new.html'
    fields = ['title']
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(generic.UpdateView):
    model = Category
    fields = ['title']
    template_name = 'category/category_edit.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(generic.DeleteView):
    model = Category
    template_name = 'category/category_delete.html'
    success_url = reverse_lazy('category_list')
