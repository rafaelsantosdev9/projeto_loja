from django.urls import path, include
from loja import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'loja'

urlpatterns = [
    path('', views.index, name='index'),  # deixa o index da loja aqui
    path('produtos/', include('produto.urls', namespace='produto')),  # agora com prefixo real
    path('perfil/', include('perfil.urls', namespace='perfil')),
    path('pedido/', include('pedido.urls', namespace='pedido')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
