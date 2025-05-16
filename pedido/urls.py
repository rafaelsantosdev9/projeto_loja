from django.urls import path
from pedido import views

app_name = "pedido"
urlpatterns = [
    
  path('pagar/<int:pedido_id>/', views.pagar, name='pagar'),
  path('salvarpedido/',views.salvarpedido,name = "salvarpedido"),  
  path('detalhe/<int:pk>/',views.detalhe,name = "detalhe"),  
  path('lista/',views.lista,name = "lista"), 
]
