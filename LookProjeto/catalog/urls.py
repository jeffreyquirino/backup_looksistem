from django.conf.urls import url

from . import views #importa a views do modulo atual


urlpatterns = [
    url(r'^$', views.products, name='products'),
    url(r'^(?P<slug>[\w_-]+)/$', views.category, name='category'),
    url(r'^produtos/(?P<slug>[\w_-]+)/$', views.product, name='product'), #as paginas de produtos terao prefixos de produto 
]   

#(?P<slug>[\w_-]+) expresão regular qe=ue tras uma url amigavel,ele chama a view de forma nomeavel , uma URL PARAMETRIZADA