from django.views.generic.base import TemplateView

# Класс-представление для главной страницы
class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аниме магазин OTAKU'

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
