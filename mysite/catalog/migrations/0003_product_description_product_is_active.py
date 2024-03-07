# Generated by Django 5.0.2 on 2024-03-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_genre_property_source_product_productproperty'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='abc', verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активный продукт'),
        ),
    ]
