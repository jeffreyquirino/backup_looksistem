from django.contrib.auth.backends import ModelBackend as BaseModelBackend 

from .models import User


class ModelBackend(BaseModelBackend):

    def authenticate(self, username=None, password=None): #funcao garante que seja atenticado a mesma está sendo chamada pela classe la no settings
        if not username is None:
            try:
                user = User.objects.get(email=username) #ira pegar o usuario pelo email
                if user.check_password(password): #se o usuario existir
                    return user  #retorna usuario
            except User.DoesNotExist:
                pass