from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from .models import User

UserModel = User

# Кастомная бэкенд аутентификация по Email
class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (UserModel.DoesNotExist, UserModel.MultipleObjectsReturned):
            return None
        
