from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from produto.models import Variacao
from utils import utils
from django.core.paginator import Paginator
from pedido.models import Pedido,ItemPedido
from produto.models import Produto
from django.contrib.auth.decorators import login_required

def salvarpedido (request):
    if request.method != 'POST':
        messages.error(request, 'Método não permitido.')
        return redirect('produto:carrinho')
    
    if not request.user.is_authenticated:
        messages.error(request,'Você precisa estar logado para acessar essa pagina')
        return redirect('perfil:criar')
    if not request.session.get('carrinho'):

        messages.error(request,'Carrinho vazio, Adicione produtos para continuar o pedido')
        return redirect('produto:lista')
    carrinho = request.session.get('carrinho')
    carrinho_variacao_id = [variacao for variacao in carrinho]

    bd_variacoes = list(
        Variacao.objects.select_related('produto').filter(id__in = carrinho_variacao_id)
        )
    for variacao in bd_variacoes:
        #converti para str pq no carrinho la criado era str tbm
        vid = str(variacao.id) # fica aparecendo como errado mas não está
        estoque = variacao.estoque
        quantidade_carrinho = carrinho[vid]['quantidade']
        preco_unitario = carrinho[vid]['preco_unitario']
        preco_unitario_promocional = carrinho[vid]['preco_unitario_promocional']
        if estoque< quantidade_carrinho:
            carrinho[vid]['quantidade'] = estoque
            carrinho[vid]['preco_quantitativo'] = estoque * preco_unitario
            carrinho[vid]['preco_quantitativo_promocional'] = estoque * preco_unitario_promocional

            messages.error(request,'estoque insuficiente em alguns produtos')
            request.session.save()
            return redirect('produto:carrinho')
    quantidade_total_carrinho  = utils.cart_total_qtd(carrinho)
    valor_total_carrinho = utils.cart_totals(carrinho)
    pedido = Pedido(
        usuario = request.user,
        total = valor_total_carrinho,
        quantidade_total = quantidade_total_carrinho,
        status= 'C',
    )
    pedido.save()
    ItemPedido.objects.bulk_create(
    [
        ItemPedido(
            pedido=pedido,
            produto=v['nome_produto'],
            produto_id=Produto.objects.get(id=v['produto_id']),
            variacao=v['nome'],
            variacao_id=v['produto_id'],
            preco=v['preco_quantitativo'],
            preco_promocional=v['preco_quantitativo_promocional'],
            quantidade=v['quantidade'],
            imagem=v['imagem']
        )
        for v in carrinho.values()
    ]
)

# Esvazia o carrinho da sessão
    del request.session['carrinho']
    request.session.save()

    messages.success(request, 'Pedido criado com sucesso!')
    return redirect('pedido:pagar', pedido_id=pedido.id)
    
   


@login_required(login_url='perfil:criar')
def pagar(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    contexto = {'pedido': pedido}
    
    return render(request, 'pedido/pagar.html', contexto)

@login_required(login_url='perfil:criar')
def detalhe(request,pk):
    #Pega os pedidos, filtra e ordena
    pedido = get_object_or_404(Pedido,id=pk, usuario = request.user)
    
    #isso vai ser usado em um for no template
    contexto = {
        'pedido':pedido
    }
    return render(request,'pedido/detalhe.html',contexto)


@login_required(login_url='perfil:criar')
def lista(request):
    #Pega os pedidos, filtra e ordena
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-id')
    #quantas linhas por page aparecem
    paginator = Paginator(pedidos,2)
    page_number = request.GET.get('page')
    page_obj= paginator.get_page(page_number)
    #isso vai ser usado em um for no template
    contexto = {
        'page_obj': page_obj
    }
    return render(request,'pedido/lista.html',contexto)

