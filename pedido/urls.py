from django.urls import path
from pedido import views

app_name = "pedido"
urlpatterns = [
  path('',views.pagar,name = "pagar"),  
  path('salvarpedido/',views.fecharpedido,name = "salvarpedido"),  
  path('detalhe/',views.detalhe,name = "detalhe"),  
]
