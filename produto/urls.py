from django.urls import path
from produto import views

app_name = 'produto'

urlpatterns = [
    path('', views.lista_produto, name="lista"),
    path('adicionaraocarrinho/<int:id>/', views.adicionar_carrinho, name="adicionaraocarrinho"),
    path('removerdocarrinho/<int:id>/', views.remover_carrinho, name = "removerdocarrinho"),
    path('carrinho/', views.carrinho, name = "carrinho"),
    path('finalizar/', views.finalizar, name = "finalizar"),
    path('esvaziarcarrinho/', views.esvaziar_carrinho, name="esvaziarcarrinho"),
    path('resumo/', views.resumo_compra, name="resumo"),
    path('busca/', views.busca, name = "busca"),
    path('genero/<int:genero_id>/', views.filtro_genero, name='produtos_por_genero'),
    path('whatsapp-pedido/', views.whatsapp_pedido, name='whatsapp_pedido'),
    path('<slug:slug>/', views.detalhe_produto, name = "detalhe"),
    
]
