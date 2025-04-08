from django.urls import path
from produto import views

app_name = 'produto'

urlpatterns = [
    path('', views.lista_produto, name="lista"),
    path('<slug:slug>/', views.detalhe_produto, name = "detalhe"),
    path('adicionaraocarrinho/<int:id>/', views.adicionar_carrinho, name="adicionaraocarrinho"),
    path('removerdocarrinho/', views.remover_carrinho, name = "removerdocarrinho"),
    path('carrinho/', views.carrinho, name = "carrinho"),
    path('finalizar/', views.finalizar, name = "finalizar"),
]
