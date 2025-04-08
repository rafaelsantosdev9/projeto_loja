from django.contrib import admin
from . import models

@admin.register(models.Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = 'telefone','email','endereco'
# Register your models here.
