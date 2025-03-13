from django.contrib import admin
from . import models 

# Register your models here.
@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = 'nome','preco','tipo','imagem'
    ordering = 'nome',
    search_fields = 'nome','tipo'
    list_editable = 'preco','tipo',

   
    