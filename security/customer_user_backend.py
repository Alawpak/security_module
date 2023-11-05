from django.contrib.auth.backends import ModelBackend
from .models import CustomUser


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, login_usuario=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(login_usuario=login_usuario)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
