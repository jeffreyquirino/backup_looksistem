from django.shortcuts import render, get_object_or_404 #get_object_or_404 faz uma consulta ou retorna 404
from django.views import generic

from .models import Product, Category


class ProductsView(generic.ListView): #ListView lista objetos, tabem fornece paginação de graça

    model = Product
    template_name = 'catalog/products.html'
    context_object_name = 'produtos' #nome a listagem de produtos no template, pode-se colocar qualquer varivael contatno q a ponha no template
    paginate_by = 3 #ele vai paginar por n numeros, funcao do proprio django


products = ProductsView.as_view() 

#def products(request):
#    context = {
#        'products': Product.objects.all() #utilizado como variavel no cod html para referenciar produtos
#    }
#    return render(request, 'catalog/products.html', context)

class CategoryListView(generic.ListView):

    template_name = 'catalog/category.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self): #verifica se há uma variavel chamada model
        return Product.objects.filter(category__slug=self.kwargs['slug']) #ele busca a categoria que tem o slug ( __ )

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs) #com o SUPER esta chamando o comportamento da classe mãe, super chama a implementação interior
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug']) #ele vai consultar se não existir retonará 404
        return context

category = CategoryListView.as_view()

#def category (request, slug):
#    category = Category.objects.get(slug = slug) #pega o slug q ta sendo passado
#    context = {
#        'current_category': category,
#        'products': Product.objects.filter(category=category), #tras os produtos filtrados, da categoria que o slug trazer
#    }
#    return render(request,'catalog/category.html', context)

def product(request, slug):
    product = Product.objects.get(slug=slug)
    context = {
        'product': product
    }
    return render(request, 'catalog/product.html', context)
