# Generated by Django 4.1 on 2022-08-21 06:03

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_options_alter_productvariation_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='no.jpg', upload_to='photos/products'),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='image',
            field=models.ImageField(null=True, upload_to='photos/products'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field='image', max_length=18, null=True, samples=None),
        ),
    ]