from django.urls import reverse_lazy
from .models import Comment
from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import AnonymousUser


'''
    Декоратор для проверки редактирования/удаления комментариев.
    Если пользователь не анонимный и это его комментарий, функция выполняется.
'''
def check_comment_user(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user_comment = get_object_or_404(Comment, pk=kwargs.get('comment_id'))
        if not isinstance(request.user, AnonymousUser) and request.user == user_comment.user:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('login'))

    return wrapper