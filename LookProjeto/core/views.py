from django.shortcuts import render
from django.http import HttpResponse

from catalog.models import Category

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')






# Estilo de contexto que não vamos utilizar, o mesmo define template por template, so que 
#ele nao define em todos os templates.
# na catalog/context_processors.py esta definido a que define todos de uma vez
#context = {
 #       'categories': Category.objects.all() #resgatando todas as categorias do banco
  #  } context é um dicionario aonde voce vai adionar variaveis na sua rederização de template