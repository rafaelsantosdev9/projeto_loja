from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('salvar/', views.salvarpedido, name='salvarpedido'),
    path('pagar/<int:pedido_id>/', views.pagar, name='pagar'),
    path('detalhe/<int:pk>/', views.detalhe, name='detalhe'),
    path('lista/', views.lista, name='lista'),
]
