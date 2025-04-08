from django.urls import path
from pedido import views

app_name = "pedido"
urlpatterns = [
  path('',views.pagar,name = "pagar"),  
  path('fechar_pedido/',views.fechar_pedido,name = "fechar_pedido"),  
  path('detalhe/',views.detalhe,name = "detalhe"),  
]
