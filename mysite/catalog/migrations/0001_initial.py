# Generated by Django 5.0.2 on 2024-03-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(editable=False, max_length=128, unique=True, verbose_name='Слаг')),
                ('icon_image', models.ImageField(upload_to='icons_categories', verbose_name='Изображение категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
    ]
