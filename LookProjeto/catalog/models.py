# coding=utf-8

from django.db import models
from django.core.urlresolvers import reverse

class Category(models.Model): #modelo que representa uma tabela no banco de dados
    
    name = models.CharField('Nome', max_length=100) #CharFiel seria como o varchar do sql
    slug = models.SlugField('Indentificador', max_length=100) #um tipo de charfield, mas ele é unico no banco

    created = models.DateTimeField('Criado em', auto_now_add=True) #seta a data atual e não muda
    modified = models.DateTimeField('Modificado em', auto_now=True) # toda vez quer for salvo pega a data atual

    class Meta: #são metas aplicações aceita neste modelo
        verbose_name = 'Categoria' # o verbose_name seria como descrever uma classe
        verbose_name_plural = 'Categorias'
        ordering = ['name'] #deixa em ordem alfabetica

    def __str__(self): #representação em string de um objeto
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug}) #kwargs parametros nomeados, essa função é um padrao para utilizar url 



class Product(models.Model): #classe do produto

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)
    category = models.ForeignKey('catalog.Category', on_delete=models.PROTECT, verbose_name='Categoria') #a categoria tem um ou mais produtos associados
    description = models.TextField('Descrição', blank=True)  #campo não obrigatorio
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8) 

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug}) #kwargs parametros nomeados, essa função é um padrao para utilizar url 



    

