from django.views import generic
from .models import Region
from django.urls import reverse_lazy


class RegionListView(generic.ListView):
    model = Region
    template_name = 'location/region.html'


class RegionDetailView(generic.DetailView):
    model = Region
    template_name = 'location/region_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['region'] = Region.objects.filter(title=self.object.id)
        return context


class RegionCreateView(generic.CreateView):
    model = Region
    template_name = 'location/region_new.html'
    fields = ['title']
    success_url = reverse_lazy('region_list')


class RegionUpdateView(generic.UpdateView):
    model = Region
    fields = ['title']
    template_name = 'location/region_edit.html'
    success_url = reverse_lazy('region_list')


class RegionDeleteView(generic.DeleteView):
    model = Region
    template_name = 'location/region_delete.html'
    success_url = reverse_lazy('region_list')
