# Generated by Django 4.0.4 on 2022-05-29 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_rename_product_images_p_remove_product_oth_images_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='oth_images',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('Для девочки', 'Для девочки'), ('Для мальчика', 'Для мальчика')], max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='oth_images',
            field=models.ManyToManyField(blank=True, to='product.images'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('18', '18'), ('20', '20'), ('22', '22'), ('24', '24'), ('26', '26'), ('28', '28'), ('30', '30'), ('32', '32'), ('34', '34'), ('36', '36'), ('38', '38'), ('40', '40')], max_length=30)),
                ('s_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(to='product.sizes'),
        ),
    ]