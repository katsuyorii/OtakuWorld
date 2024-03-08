from django.db import models

# Модель изображений слайдеров
class SliderImage(models.Model):
    icon_slider = models.ImageField(verbose_name='Изображение', upload_to='icons_slider')

    class Meta:
        verbose_name = 'Изображение слайдера'
        verbose_name_plural = 'Изображения слайдеров'
        
    # При удалении объекта удаляется связанное фото (оптимизация)
    def delete(self, *args, **kwargs):
        self.icon_slider.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.icon_slider.url


# Модель изображений для новостного продукта
class NewsProductImage(models.Model):
    icon_new_product = models.ImageField(verbose_name='Изображение', upload_to='icons_new_products')

    class Meta:
        verbose_name = 'Изображение новостного продукта'
        verbose_name_plural = 'Изображения новостного продукта'

    # Перед сохранением нового объекта, делается выборка, которая не соответсвует PK нового изображения и удаляется (1 запись в БД)
    def save(self, *args, **kwargs):
        NewsProductImage.objects.exclude(pk=self.pk).delete()
        super().save(*args, **kwargs)

    # При удалении объекта удаляется связанное фото (оптимизация)
    def delete(self, *args, **kwargs):
        self.icon_new_product.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.icon_new_product.url