from django.db import models
from pytils.translit import slugify

# Модель для категорий товаров (Манга, канцелярия, одежда)
class Category(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=128, unique=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=128, unique=True, db_index=True, editable=False)
    icon_image = models.ImageField(verbose_name='Изображение категории', upload_to='icons_categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    '''
    Переопределение метода сохранения записи.
    С помощью библиотеки pytils переводим киррилицу в латиницу по полю name.
    В поле slug записывается поле name на латинице.
    '''
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name