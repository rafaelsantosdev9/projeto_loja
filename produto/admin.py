from django.contrib import admin
from . import models 



class VariacaoInline(admin.TabularInline):
    model = models.Variacao         
    extra = 1 


@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    #quais inlines terão dentro 
    inlines = [
        VariacaoInline,
    ]
    list_display = 'nome','get_preco_formatado','get_preco_formatado_promo','tipo','descricao_curta'
    ordering = 'nome',
    search_fields = 'nome','tipo'
    

@admin.register(models.Variacao)
class VariacaoAdmin(admin.ModelAdmin):
    list_display = 'nome','produto','preco' 

 
    