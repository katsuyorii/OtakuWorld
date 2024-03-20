from django import forms
from .models import User

# Класс-форма для авторизации пользователя
class LoginUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'login-email-input', 
        'placeholder': 'Введите email',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs= {
        'class': 'login-email-input', 
        'placeholder': 'Введите пароль',
    }))


# Класс-форма для регистрации нового пользователя
class RegistrationUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'login-email-input', 
        'placeholder': 'Введите email',
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login-email-input', 
        'placeholder': 'Введите email',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs= {
        'class': 'login-email-input', 
        'placeholder': 'Введите пароль',
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs= {
        'class': 'login-email-input', 
        'placeholder': 'Введите пароль',
    }))