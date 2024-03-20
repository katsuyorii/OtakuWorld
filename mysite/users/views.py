from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LoginUserForm, RegistrationUserForm
from django.contrib import messages
from .models import User


# Класс-представление авторизации пользователя
class LoginUserView(FormView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def form_valid(self, form): 
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Вы успешно вошли в систему!')
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return self.form_invalid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context


# # Класс-представление регистрации нового пользователя
class RegistrationUserView(FormView):
    form_class = RegistrationUserForm
    template_name = 'users/registration.html'

    def form_valid(self, form): 
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']

        if password == password2:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(self.request, user)
        
            messages.success(self.request, 'Вы зарегестрировались в системе!')
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return self.form_invalid(form)
            

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Авторизация'

            return context