from django.conf.urls import url

from . import views #importa a views do modulo atual


urlpatterns = [
    url(r'^$', views.products, name='products'), 
]