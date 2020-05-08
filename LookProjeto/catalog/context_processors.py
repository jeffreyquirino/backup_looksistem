# coding=utf-8

from .models import Category


def categories(request):
    return {
        'categories': Category.objects.all()
    }

    #a funcao acima define, recebe um request e retorna um dicionario. 