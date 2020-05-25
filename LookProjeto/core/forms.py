from django import forms
from django.core.mail import send_mail
from django.conf import settings  #importando configuração do settings

class ContactForm(forms.Form): #classe do formulario do site

    name = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail') #emialfield valida se o email é de vdd @alguma coisa
    message = forms.CharField(label='Mensagem', widget=forms.Textarea()) # o widet difine que é um charfild de textarea

    def send_mail(self): #Funcao de enviar emails
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        message = 'Nome: {0}\nE-mail:{1}\n{2}'.format(name, email, message)
        send_mail(
            'Contato do Django E-Commerce', message, settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL]
        )