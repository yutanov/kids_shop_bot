from django.views import generic
from django.apps import apps
from .models import Product, Images, Sizes, Colors, SIZE_CHOICE, COLOR_CHOICE
from .forms import ProductForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

Category = apps.get_model('category', 'Category')


class ProductListView(generic.ListView):
    model = Product
    template_name = 'product/products.html'


# class ProductDetailView(generic.DetailView):
#    model = Product
#    template_name = 'product/product_detail.html'


def detail_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    # oth_images = Images.objects.filter(p=pk) or None
    oth_images = list(Images.objects.filter(p=pk).values_list('oth_images', flat=True)) or None
    sizes = list(Sizes.objects.filter(s=pk).values_list('size', flat=True))
    colors = list(Colors.objects.filter(c=pk).values_list('color', flat=True))
    context = {
        'title': product.title,
        'category': product.category,
        'image': product.image,
        'oth_images': oth_images,
        'description': product.description,
        'price': product.price,
        'gender': product.gender,
        'sizes': sizes,
        'colors': colors,
        'quantity': product.quantity,
        'pk': pk
    }
    return render(request, 'product/product_detail.html', context)


def product_create(request):
    if request.method == 'POST':
        # form = ProductForm(request.POST or None, request.FILES or None)
        data = request.POST
        image = request.FILES.get('image')
        oth_images = request.FILES.getlist('oth_images') or None
        title = data['title']
        category = Category.objects.get(id=data['category'])
        description = data['description']
        price = data['price']
        gender = data['gender']
        # size = data['size']
        sizes = request.POST.getlist('size')
        colors = request.POST.getlist('color')
        quantity = data['quantity']
        product = Product.objects.create(
            title=title, category=category, image=image, description=description,
            price=price, gender=gender, quantity=quantity
        )
        product.save()
        product_id = product.id
        if oth_images:
            for pic in oth_images:
                images = Images.objects.create(p=Product.objects.get(id=product_id), oth_images=pic)
                images.save()

        for size in sizes:
            s = Sizes.objects.create(s=Product.objects.get(id=product_id), size=size)
            s.save()

        for color in colors:
            c = Colors.objects.create(c=Product.objects.get(id=product_id), color=color)
            c.save()
        return HttpResponseRedirect('/categories')

    form = ProductForm()
    context = {
        'form': form,
        'size_choice': SIZE_CHOICE,
        'color_choice': COLOR_CHOICE,
    }
    return render(request, 'product/product_new.html', context)


# class ProductCreateView(generic.CreateView):
#    model = Product
#    template_name = 'product/product_new.html'
    # fields = ['title', 'category', 'image', 'oth_images', 'description', 'price', 'gender', 'size']
#    fields = ['title', 'category', 'image', 'description', 'price', 'gender', 'size']
#    success_url = reverse_lazy('category_list')


def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    sizes = list(Sizes.objects.filter(s=pk).values_list('size', flat=True))
    colors = list(Colors.objects.filter(c=pk).values_list('color', flat=True))
    if request.method == 'POST':
        # form = ProductForm(request.POST or None, request.FILES or None)
        product = get_object_or_404(Product, id=pk)
        data = request.POST
        product.image = request.FILES.get('image') or product.image
        oth_images = request.FILES.getlist('oth_images') or None
        product.title = data['title']
        print(data['category'])
        if isinstance(data['category'], int):
            product.category = Category.objects.get(id=data['category'])
        # elif isinstance(data['category'], str):
        #    product.category = Category.objects.get(title=data['category'])
        product.description = data['description']
        product.price = data['price']
        product.gender = data['gender']
        sizes = request.POST.getlist('size') or None
        colors = request.POST.getlist('color') or None
        product.quantity = data['quantity']
        product.save()

        Images.objects.filter(p=pk).delete()
        if oth_images:
            for pic in oth_images:
                images = Images.objects.create(p=Product.objects.get(id=pk), oth_images=pic)
                images.save()

        if sizes:
            Sizes.objects.filter(s=pk).delete()
            for size in sizes:
                s = Sizes.objects.create(s=Product.objects.get(id=pk), size=size)
                s.save()

        if colors:
            Colors.objects.filter(c=pk).delete()
            for color in colors:
                c = Colors.objects.create(c=Product.objects.get(id=pk), color=color)
                c.save()
        return HttpResponseRedirect('/categories')

    form = ProductForm()
    context = {
        'form': form,
        'title': product.title,
        'category': product.category,
        'image': product.image,
        'description': product.description,
        'price': product.price,
        'gender': product.gender,
        'sizes': sizes,
        'colors': colors,
        'size_choice': SIZE_CHOICE,
        'color_choice': COLOR_CHOICE,
        'quantity': product.quantity,
    }
    print(product.image)
    return render(request, 'product/product_edit.html', context)


# class ProductUpdateView(generic.UpdateView):
#    model = Product
#    fields = '__all__'
    # fields = ['title', 'category', 'image', 'оth_images', 'description', 'price', 'gender', 'size']
#    template_name = 'product/product_edit.html'
#    success_url = reverse_lazy('category_list')


class ProductDeleteView(generic.DeleteView):
    model = Product
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('category_list')
