from django.urls import path
from .views import LoginUserView, RegistrationUserView, ProfileUserView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('profile/', login_required(ProfileUserView.as_view()), name='profile'),
]