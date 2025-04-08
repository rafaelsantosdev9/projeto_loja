from django.contrib import admin
from . import models
# Register your models here.

class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1


@admin.register(models.Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]
    list_display = 'total','status',
    ordering = 'status',
    search_fields = 'total',
    list_editable = 'status',

@admin.register(models.ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = 'pedido','produto','variacao','preco'
    ordering = 'produto',
    search_fields = 'preco','produto',
    list_editable = 'preco','produto',



    