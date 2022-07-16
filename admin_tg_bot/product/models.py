from django.db import models
from django.urls import reverse

SIZE_CHOICE = (('18', '18'), ('20', '20'), ('22', '22'), ('24', '24'), ('26', '26'), ('28', '28'), ('30', '30'),
               ('32', '32'), ('34', '34'), ('36', '36'), ('38', '38'), ('40', '40'))
COLOR_CHOICE = (('красный', 'красный'), ('зеленый', 'зеленый'), ('синий', 'синий'), ('желтый', 'желтый'),
                ('оранжевый', 'оранжевый'), ('белый', 'белый'), ('черный', 'черный'), ('фиолетовый', 'фиолетовый'),
                ('коричневый', 'коричневый'), ('другой', 'другой'))


class Images(models.Model):
    p = models.ForeignKey('Product', blank=False, on_delete=models.CASCADE)
    oth_images = models.ImageField(upload_to='media/', blank=True, null=True)


class Sizes(models.Model):
    s = models.ForeignKey('Product', blank=False, on_delete=models.CASCADE)
    size = models.CharField(max_length=30, choices=SIZE_CHOICE)


class Colors(models.Model):
    c = models.ForeignKey('Product', blank=False, on_delete=models.CASCADE)
    color = models.CharField(max_length=30, choices=COLOR_CHOICE)


class Product(models.Model):
    title = models.CharField(max_length=60, blank=False, default='')
    category = models.ForeignKey('category.Category', blank=False, related_name='product', on_delete=models.PROTECT)
    image = models.ImageField(upload_to='media/')
    oth_images = models.ManyToManyField(Images, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    gender = models.CharField(max_length=30, blank=False, choices=(('Для девочки', 'Для девочки'),
                                                                   ('Для мальчика', 'Для мальчика'))
                              )
    size = models.ManyToManyField(Sizes, blank=False)
    color = models.ManyToManyField(Colors, blank=False)
    quantity = models.IntegerField(blank=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_view', args=[str(self.id)])
