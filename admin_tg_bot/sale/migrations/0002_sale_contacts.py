# Generated by Django 4.0.4 on 2022-06-07 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='contacts',
            field=models.CharField(default=0, max_length=600),
            preserve_default=False,
        ),
    ]
