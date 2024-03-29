# Generated by Django 4.0.4 on 2022-05-10 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=60)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=30)),
                ('size', models.CharField(choices=[(18, '18'), (20, '20'), (22, '22'), (24, '24'), (26, '26'), (28, '28'), (30, '30'), (32, '32'), (34, '34'), (36, '36'), (38, '38'), (40, '40')], max_length=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='category.category')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
