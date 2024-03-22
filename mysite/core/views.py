from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from catalog.models import Product

from .models import SliderImage, NewsProductImage

# Класс-представление для главной страницы
class IndexView(ListView):
    model = Product
    template_name = 'core/index.html'
    context_object_name = 'hits'

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-sales')[:5].select_related('category')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аниме магазин OTAKU'
        context['slider_images'] = SliderImage.objects.all()
        context['new_product_image'] = NewsProductImage.objects.first()
        context['manga_list'] = Product.objects.all().filter(category__slug='manga').select_related('category')

        return context


# Класс-представление для страницы "Оплата и доставка"
class DeliveryView(TemplateView):
    template_name = 'core/delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оплата и доставка'

        return context


# Класс-представление для страницы "Возврат и обмен"
class RefundView(TemplateView):
    template_name = 'core/refund.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Возврат и обмен'

        return context


# Класс-представление для страницы "О нас"
class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'

        return context


# Класс-представление для страницы "Контакты"
class ContactsView(TemplateView):
    template_name = 'core/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'

        return context
