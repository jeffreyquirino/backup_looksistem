from django.contrib import admin

from .models import Product, Category

class CategoryAdmin(admin.ModelAdmin): #Campos do amdin

    list_display = ['name', 'slug', 'created', 'modified'] #lista por nome,slug,criado e modificado
    search_fields = ['name', 'slug'] #consegue pesquisar apartir de nome ou slug
    list_filter = ['created', 'modified'] #filtro lateral


class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'category', 'created', 'modified']
    search_fields = ['name', 'slug', 'category__name']
    list_filter = ['created', 'modified']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)