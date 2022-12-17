from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class AuthBackend(object):
    # def authenticate(self, request, phone=None, code=None):

    #     #Найти юзера по номеру и проверить код
    #     return None
    #     # Check the username/password and return a user.
    def authenticate(self, phone=None, code=None):
        # assert False, 'Работает!'
        try:
            user = CustomUser.objects.get(phone=phone)
            if user.check_code(code):
                user.code = None
                user.save()
                return user
            #return None
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None