from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings  #importando configuração do settings 
from django.views.generic import View, TemplateView #template_name

from .forms import ContactForm

class IndexView(TemplateView):

    template_name = 'index.html'


index = IndexView.as_view() # "as_view" trasforma a classe num objeto chamavel

def contact(request):
    success = False
    form = ContactForm(request.POST or None) #Quando a requisisão for POST ele vai acessar essa view, ele sera um form com POST carregado, esse None é como se o formulario nao estivesse preenchido então ele nao retorna ERRO neste caso
    if form.is_valid():
        form.send_mail() #essa funcao esta no core/forms.py
        success = True
    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)






# Estilo de contexto que não vamos utilizar, o mesmo define template por template, so que 
#ele nao define em todos os templates.
# na catalog/context_processors.py esta definido a que define todos de uma vez
#context = {
 #       'categories': Category.objects.all() #resgatando todas as categorias do banco
  #  } context é um dicionario aonde voce vai adionar variaveis na sua rederização de template