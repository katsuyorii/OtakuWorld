from django.urls import path
from .views import LoginUserView, RegistrationUserView, ProfileUserView, LogoutUserView, EditInfoUserView, ChangePasswordUserView, FavoritesUserView, FavoritesDeleteUserView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
    path('profile/', login_required(ProfileUserView.as_view()), name='profile'),
    path('logout/', login_required(LogoutUserView.as_view()), name='logout'),
    path('profile-edit/', login_required(EditInfoUserView.as_view()), name='profile_edit'),
    path('change-password/', login_required(ChangePasswordUserView.as_view()), name='change_password'),
    path('favorites/', login_required(FavoritesUserView.as_view()), name='favorites'),
    path('delete-favorites/<int:favorites_id>', login_required(FavoritesDeleteUserView.as_view()), name='delete-favorites'),
]