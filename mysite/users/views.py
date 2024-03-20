from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LoginUserForm
from django.contrib import messages


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

