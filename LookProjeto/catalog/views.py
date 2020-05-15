from django.shortcuts import render

from .models import Product, Category


def products(request):
    context = {
        'products': Product.objects.all() #utilizado como variavel no cod html para referenciar produtos
    }
    return render(request, 'catalog/products.html', context)

def category (request, slug):
    category = Category.objects.get(slug = slug) #pega o slug q ta sendo passado
    context = {
        'current_category': category,
        'products': Product.objects.filter(category=category), #tras os produtos filtrados, da categoria que o slug trazer
    }
    return render(request,'catalog/category.html', context)

def product(request, slug):
    product = Product.objects.get(slug=slug)
    context = {
        'product': product
    }
    return render(request, 'catalog/product.html', context)
