from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from users.models import User
from django.db.models import Avg

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
    
    def get_absolute_url(self):
        return reverse('product_list', kwargs={"category_slug": self.slug})


# Модель для жанров (манга, манхва, маньхуа и т.д.)
class Genre(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=128, unique=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=128, unique=True, db_index=True, editable=False)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

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


# Модель для источников
class Source(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=128, unique=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=128, unique=True, db_index=True, editable=False)

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

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


# Модель для базовых характеристик продукта
class Product(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=128)
    name_eng = models.CharField(verbose_name='Наименование (англ.)', max_length=128)
    slug = models.SlugField(verbose_name='Слаг', max_length=128, unique=True, db_index=True, editable=False)
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.CASCADE)
    source = models.ForeignKey(verbose_name='Источник', to=Source, on_delete=models.CASCADE)
    icon_image = models.ImageField(verbose_name='Изображение продукта', upload_to='icons_products')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(verbose_name='Цена (руб.)', max_digits=6, decimal_places=2)
    discount = models.PositiveIntegerField(verbose_name='Скидка (%)', default=0)
    amount = models.PositiveIntegerField(verbose_name='Количество в наличии', default=0)
    is_active = models.BooleanField(verbose_name='Активный продукт', default=False)
    sales = models.PositiveIntegerField(verbose_name='Количество продаж', default=0, editable=False)
    rating = models.SmallIntegerField(verbose_name='Рейтинг', default=0, editable=False)

    class Meta:
        verbose_name = 'Базовый продукт'
        verbose_name_plural = 'Базовые продукты'

    '''
    Переопределение метода сохранения записи.
    С помощью библиотеки pytils переводим киррилицу в латиницу по полю name.
    Авто-слаг, при добавлении в конец слага добавляется id.
    '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + '-' + str(self.pk)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"category_slug": self.category.slug, "product_slug": self.slug})
    
    # Метод преобразования цены с учетом скидки, если она есть
    def price_discount(self):
        if self.discount:
            return self.price - ((self.price * self.discount) / 100)
        
        return self.price
    
    # Метод рассчета рейтинга
    def update_rating(self):
        average_grade = Comment.objects.filter(product__slug=self.slug).aggregate(avg_grade=Avg('grade'))['avg_grade']
        
        if average_grade is None:
            self.rating = 0
        else:
            self.rating = average_grade
            
        self.save()


# Модель для характеристик продуктов
class Property(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=128)

    class Meta:
        verbose_name = 'Характеристика продукта'
        verbose_name_plural = 'Характеристики продуктов'

    def __str__(self):
        return self.name


# Модель для сопоставления характеристик продукта и самого продукта
class ProductProperty(models.Model):
    product = models.ForeignKey(verbose_name='Продукт', to=Product, on_delete=models.CASCADE)
    property = models.ForeignKey(verbose_name='Характеристика', to=Property, on_delete=models.CASCADE)
    value_string = models.CharField(verbose_name='Текстовое значение характеристики', max_length=250, null=True, blank=True, help_text='Значение задается текстом (Автор, обложка, Цвет)')
    value_integer = models.IntegerField(verbose_name='Числовое значение характеристики', null=True, blank=True, help_text='Значение задается целым числом (Вес книги, год выпуска)')
    value_genres = models.ManyToManyField(verbose_name='Жанры', to=Genre, null=True, blank=True, help_text='Поле для категорий, где есть жанры (Манга, манхва. маньхуа, ранобэ)')

    class Meta:
        verbose_name = 'Сопоставление характеристик продуктов'
        verbose_name_plural = 'Сопоставление характеристик продуктов'

    def __str__(self):
        return f'{self.product.name} | {self.property.name}'
    

# Модель для комментария
class Comment(models.Model):
    product = models.ForeignKey(verbose_name='Продукт', to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)
    review_text = models.TextField(verbose_name='Текст комментария')
    create_date = models.DateTimeField(verbose_name='Дата создания комментария', auto_now_add=True)
    grade = models.SmallIntegerField(verbose_name='Оценка пользователя')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.product.name} | {self.user.username}'
    

# Класс-модель для избранных товаров
class Favorites(models.Model):
    product = models.ForeignKey(verbose_name='Продукт', to=Product, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | {self.product.name}'

    def get_absolute_url(self):
        return reverse('delete-favorites', kwargs={"favorites_id": self.pk})

    class Meta:
        verbose_name = 'Избранное пользователя'
        verbose_name_plural = 'Избранное пользователей'