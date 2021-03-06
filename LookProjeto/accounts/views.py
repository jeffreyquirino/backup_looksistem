from django.shortcuts import render
from django.views.generic import (
    CreateView, TemplateView, UpdateView, FormView
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin #utilizado pois nossa view é baseada em classe, esse LoginRequiredMixin força sempre o usuario estar logado para realizar a ação
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import login as auth_login

from .models import User
from .forms import UserAdminCreationForm

class IndexView(LoginRequiredMixin, TemplateView): #so renderiza um template

    template_name = 'accounts/index.html'

class RegisterView(CreateView):

    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm 
    success_url = reverse_lazy('index') 

class UpdateUserView(LoginRequiredMixin, UpdateView):

    model = User 
    template_name = 'accounts/update_user.html'
    fields = ['name', 'email']
    success_url = reverse_lazy('accounts:index')

    def get_object(self): #funcao pega o usuario
        return self.request.user

class UpdatePasswordView(LoginRequiredMixin, FormView):

    template_name = 'accounts/update_password.html'
    success_url = reverse_lazy('accounts:index')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    #def form_valid(self, form):
    #    form.save()
    #    return super(UpdatePasswordView, self).form_valid(form)


index = IndexView.as_view()
register = RegisterView.as_view()
update_user = UpdateUserView.as_view()
update_password = UpdatePasswordView.as_view()