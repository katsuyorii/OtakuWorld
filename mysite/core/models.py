from django.db import models

class SliderImage(models.Model):
    icon_slider = models.ImageField(verbose_name='Изображение', upload_to='icons_slider')

    class Meta:
        verbose_name = 'Изображение слайдера'
        verbose_name_plural = 'Изображения слайдеров'
        
    def __str__(self):
        return self.icon_slider.url