from rest_framework.authtoken.models import Token

from testing import models


class AuthorizeError(Exception):
    pass


def authorize_user(validated_data: dict) -> models.User:
    """Аутентификация пользователя"""
    user = models.User.objects.filter(username=validated_data['username']).first()
    if not user:
        raise AuthorizeError('Неверный логин или пароль')

    if not user.check_password(validated_data['password']):
        raise AuthorizeError('Неверный логин или пароль')

    Token.objects.get_or_create(user=user)
    return user
