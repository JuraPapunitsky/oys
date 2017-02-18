# coding=utf-8

from base.models import User


class UsernameAuthBackend(object):
    u""" 
    Авторизацию пользователей по username
    Пользоваться можно только тогда, если мы предварительно проверили оператора, 
    например, по клиентскому сертификату
    """

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, username):
        u""" Если пользователь не найден, создаем его и возвращаем.
        Но не сохраняем, так как в него на стороне view будут 
        еще параметры добавлять, специфичные для проекта, 
        в котором используется этот backend """

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
