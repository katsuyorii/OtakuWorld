from django import forms
from django.contrib.auth import authenticate
from .models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python
from django.contrib.auth.forms import PasswordChangeForm

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

    # Метод валидации формы
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError('Неправильный email или пароль.')

        return cleaned_data


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

    # Метод валидации формы
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Пользователь с таким email уже существует!')
        
        if password != password2:
                raise forms.ValidationError('Введенные пароли отличаются!')

        return cleaned_data
    

# Класс-форма для изменения данных пользователя
class EditInfoUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login-email-input', 
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'login-email-input', 
    }))

    phone_number = PhoneNumberField(required=False, widget=forms.TextInput(attrs={
        'class': 'login-email-input', 
    }))

    image = forms.ImageField(required=False, widget=forms.FileInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'image']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        
        users = User.objects.filter(email=email)
        phone = to_python(phone_number)

        if not phone:
            raise forms.ValidationError("Некорректный формат номера телефона")

        return cleaned_data
    

# Класс-форма для изменения пароля пользователя
class ChangePasswordUserForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login-email-input',
    }))

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login-email-input',
    }))

    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login-email-input',
    }))
