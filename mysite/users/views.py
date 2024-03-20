from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from .forms import LoginUserForm, RegistrationUserForm
from django.contrib import messages
from .models import User
from django.contrib.auth import logout
from django.shortcuts import redirect


# Класс-представление авторизации пользователя
class LoginUserView(FormView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form): 
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Вы успешно вошли в систему!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка авторизации!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context


# Класс-представление регистрации нового пользователя
class RegistrationUserView(FormView):
    form_class = RegistrationUserForm
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form): 
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']

        if password == password2 and User.objects.filter(email=email).exists() == False:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(self.request, user)
        
            messages.success(self.request, 'Вы зарегестрировались в системе!')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
            
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка регистрации!')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Регистрация'

            return context
    

# Класс-представление профиля пользователя
class ProfileUserView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Мой профиль'

            return context
    
# # Класс-представление выхода из системы
class LogoutUserView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы!')
        return redirect(reverse_lazy('index'))