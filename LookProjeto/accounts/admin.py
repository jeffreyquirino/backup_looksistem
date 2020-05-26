from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin #UserAdmin é a conif de usuario padrao do django, este codigo fizemos algumas alterações nela

from .models import User #SuperUser criado 
from .forms import UserAdminCreationForm, UserAdminForm


class UserAdmin(BaseUserAdmin):

    add_form = UserAdminCreationForm #classe que representa o formulario de criar user
    add_fieldsets = (  
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    ) #uma tupla que carrega um dicionario que exibe os campos
    form = UserAdminForm 
    fieldsets = (
        (None, {
            'fields': ('username', 'email')
        }),
        ('Informações Básicas', {
            'fields': ('name', 'last_login')
        }),
        (
            'Permissões', {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser', 'groups',
                    'user_permissions'
                )
            }
        ),
    )
    list_display = ['username', 'name', 'email', 'is_active', 'is_staff', 'date_joined'] 


admin.site.register(User, UserAdmin)