"""LookProjeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login, logout #ele pega as views do django de login e logout

from core import views
from catalog import views as views_catalog

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contato/$', views.contact, name='contact'),
    url(r'^entrar/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^sair/$', logout, {'next_page': 'index'}, name='logout'),
    #url(r'^registro/$', views.register, name='register'), o mesmo so era utiizado quando não havia a aplicação accounts
    url(r'^catalogo/', include('catalog.urls', namespace='catalog')), #ele indica aonde estão definidas as urls, o namespace meio q define um pefixo do template
    url(r'^conta/', include('accounts.urls', namespace='accounts')), #tudo que começar com conta quem vai definir a URL é as urls do accounts
    url(r'^compras/', include('checkout.urls', namespace='checkout')),
    url(r'^admin/', admin.site.urls),
]

 