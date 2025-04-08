from django.shortcuts import render
from produto.models import Produto
from django.core.paginator import Paginator

def index(request):
    produtos = Produto.objects.all()
    paginator = Paginator(produtos, 4)  # 8 produtos por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
    'page_obj': page_obj,
    'from_index': True  # <- isso ativa a lógica no template
}

    return render(request, 'loja/index.html', context)
