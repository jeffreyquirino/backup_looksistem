

import re #importando o modulo que faz a regex

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin #O UserManager permite criar super usuario e outros privilegios

class User(AbstractBaseUser, PermissionsMixin): #PermissionsMixin é para que o admin funcione perfeitamente

    username = models.CharField(
        'Apelido / Usuário', max_length=30, unique=True, validators=[ #validador da regex
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-/_ .'
                , 'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de forma única na plataforma'
    )
    name = models.CharField('Nome', max_length=100, blank=True) 
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Equipe', default=False) #esse campo é para informa que se o membro é ou não da equipe
    is_active = models.BooleanField('Ativo', default=True) #informa se é ativo ou não
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True) 

    USERNAME_FIELD = 'username' #indica qual campo será usado como username 
    REQUIRED_FIELDS = ['email'] #campo que o django faz a pergunta quando rodamos o createsuperuser

    objects = UserManager() #pode se criar super usuarios

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.name or self.username

    def get_full_name(self): #informação de como é o nome completo no admin
        return str(self)

    def get_short_name(self): #informação de como é o nome curto no admin
        return str(self).split(" ")[0]


#assim o django quando vc rodar o migrate não cria uma tabela de usuario, irá iria apatir daqui