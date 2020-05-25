import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #apenas para configurar o banco de dados

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #ele pega todo conteudo enviado ao email e joga no terminal

#Arquivo que sobrescreve algumas configurações de produção olhe a linha 123 do aqruivo settings.py 