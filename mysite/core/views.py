from django.views.generic.base import TemplateView

# Класс-представление для главной страницы
class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аниме магазин OTAKU'

        return context
    

