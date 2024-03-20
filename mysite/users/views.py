from django.views.generic.base import TemplateView


# Класс-представление авторизации пользователя
class LoginUserView(TemplateView):
    template_name = 'users/login.html'
