import requests
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm #formalario do proprio django de register
from django.conf import settings  #importando configuração do settings 
from django.core.urlresolvers import reverse_lazy #importando reverse_lazy ele busca o valor quando necessario (URL)
from django.views.generic import View, TemplateView, CreateView #template_name #CreateView
from django.contrib.auth import get_user_model #essa funcao resgata o modelo de usuario
from django.contrib import messages #funcao que tras as menssagens

from .forms import ContactForm

User = get_user_model() 

class IndexView(TemplateView):

    template_name = 'index.html'


index = IndexView.as_view() # "as_view" trasforma a classe num objeto chamavel

def contact(request):
    success = False
    form = ContactForm(request.POST or None) #Quando a requisisão for POST ele vai acessar essa view, ele sera um form com POST carregado, esse None é como se o formulario nao estivesse preenchido então ele nao retorna ERRO neste caso
    if form.is_valid():
        form.send_mail() #essa funcao esta no core/forms.py
        success = True
    elif request.method == 'POST':
        messages.error(request, 'Formulário inválido') #quando nao carregar a apgina será exibido esse texto
    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)


# Logica de registro de usuario sem a aplicação accounts
#class RegisterView(CreateView): #o Create View dentro do template q ele e usa cria uma variavel chamada form com o formulario atual, ele processa o post

#    form_class = UserCreationForm
#    template_name = 'register.html'
#    model = User
#    success_url = reverse_lazy('index') 

#register = RegisterView.as_view() #transformou a classe em um objeto chamavel dentro da viriavel register

#ele renderiza um template com este usuariio



# Estilo de contexto que não vamos utilizar, o mesmo define template por template, so que 
#ele nao define em todos os templates.
# na catalog/context_processors.py esta definido a que define todos de uma vez
#context = {
 #       'categories': Category.objects.all() #resgatando todas as categorias do banco
  #  } context é um dicionario aonde voce vai adionar variaveis na sua rederização de template