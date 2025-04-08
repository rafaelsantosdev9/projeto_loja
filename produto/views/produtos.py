from django.shortcuts import render, get_object_or_404, redirect     
from produto.models import Produto
from django.core.paginator import Paginator

def lista_produto(request):
    produtos = Produto.objects.all()
    paginator = Paginator(produtos, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'produtos': produtos,
        'page_obj': page_obj,
    }
    return render(request, 'produto/produtos.html', context)


def detalhe_produto(request, slug):
    produtos = Produto.objects.filter(slug=slug)  # Retorna uma lista de objetos
    if produtos.exists():
        produto = produtos.first()  # Obtém o primeiro registro encontrado
    else:
        produto = None  # Caso não existam registros
    return render(request, 'produto/detalhe.html', {'produto': produto})

def adicionar_carrinho(request,id):
    return render(request, 'produto/produtos.html')

def remover_carrinho(request):
    return render(request, 'loja/produtos.html')

def carrinho(request):
    return render(request, 'loja/produtos.html')

def finalizar(request):
    return render(request, 'loja/produtos.html')