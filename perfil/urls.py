from django.urls import path
from perfil import views
app_name = "perfil"
urlpatterns = [
    path('',views.criar,name = "criar"),
    path('atualizar/',views.atualizar,name = "atualizar"),
    path('login/',views.login,name = "login"),
    path('logout/',views.logout,name = "logout"),

    
]
