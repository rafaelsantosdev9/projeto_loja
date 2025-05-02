from django.contrib import admin
from . import models

@admin.register(models.Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = 'usuario','telefone','endereco'
# Register your models here.
