# Generated by Django 5.0.2 on 2024-03-08 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_product_description_product_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Количество продаж'),
        ),
    ]
