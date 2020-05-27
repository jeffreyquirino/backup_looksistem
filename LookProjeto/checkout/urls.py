from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^carrinho/adicionar/(?P<slug>[\w_-]+)/$', views.create_cartitem, #url junto com o slug do produto
        name='create_cartitem'
    ),
    url(r'^carrinho/$', views.cart_item, name='cart_item'),
    url(r'^finalizando/$', views.checkout, name='checkout')
]