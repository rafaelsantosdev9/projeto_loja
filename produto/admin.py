from django.contrib import admin
from . import models 



class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1
    can_delete = True
    show_change_link = True
    verbose_name_plural = "Variações"
    
    def get_queryset(self, request):
        return super().get_queryset(request).exclude(nome__isnull=True, preco=0) 


@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    #quais inlines terão dentro 
    inlines = [
        VariacaoInline,
    ]
    list_display = 'id','nome','get_preco_formatado','get_preco_formatado_promo','descricao_curta'
    ordering = 'nome',
    search_fields = 'nome',
    

@admin.register(models.Variacao)
class VariacaoAdmin(admin.ModelAdmin):
    list_display = 'nome','produto','preco','imagem'

 
    