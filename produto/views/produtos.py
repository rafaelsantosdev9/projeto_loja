from django.shortcuts import render, get_object_or_404, redirect     
from produto.models import Produto,Variacao,Genero
from perfil.models import Perfil
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
import urllib.parse
from django.http import HttpResponseRedirect

def busca(request):
    valor_busca = request.GET.get('q','').strip()

    if valor_busca =='':
        return redirect('produto:lista')
    # filtra pela busca
    produtos = Produto.objects.filter(Q(nome__icontains = valor_busca)| 
                                      Q(descricao_curta__icontains = valor_busca)|
                                    Q(descricao_longa__icontains = valor_busca)).order_by('-id') 
    paginator = Paginator(produtos,8)
    generos = Genero.objects.all()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    contexto = {
        'page_obj':page_obj,
        'valor_busca':valor_busca,
        'generos':generos,
    }
    return render(request,'produto/produtos.html',contexto)
def filtro_genero(request,genero_id):
    genero = get_object_or_404(Genero,id = genero_id)
    produtos = Produto.objects.filter(generos = genero)
    generos = Genero.objects.all()
    contexto ={
        'page_obj': produtos,
        'genero_selecionado': genero,
        'generos':generos
    }
    return render (request,'produto/produtos.html', contexto)


def lista_produto(request):
    #ordenando por nome 
    
    ordenar = request.GET.get('ordenar')
    if ordenar == 'preco_asc':
        produtos = Produto.objects.all().order_by('preco')
    elif ordenar == 'preco_desc':
        produtos = Produto.objects.all().order_by('-preco')
    else:
        produtos = Produto.objects.all().order_by('-nome')

    

    paginator = Paginator(produtos, 16)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    generos = Genero.objects.all()

    context = {
        'produtos': produtos,
        'page_obj': page_obj,
        'generos':generos,
        'ordenar':ordenar,
    }
    return render(request, 'produto/produtos.html', context)


def detalhe_produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    variacoes = Variacao.objects.filter(produto=produto)
    return render(request, 'produto/detalhe.html', {'produto': produto, 'variacoes': variacoes})
    

def adicionar_carrinho(request, id):
    if request.method != 'POST':
        return redirect('produto:lista')

    variacao_id = request.POST.get('variacao_id')
    

    if not variacao_id:
        messages.error(request, 'Nenhuma variação selecionada.')
        return redirect('produto:detalhe', slug=Produto.objects.get(id=id).slug)

    variacao = get_object_or_404(Variacao, id=variacao_id)
    variacao_estoque = variacao.estoque
    
    produto = variacao.produto
    carrinho = request.session.get('carrinho', {})
    variacao_id_str = str(variacao.id)
   
    produto_nome = variacao.nome
    variacao_nome = variacao.nome or ''
    preco_unitario = variacao.preco
    preco_unitario_promocional = variacao.preco_promocional
    quantidade = 1
    imagem_url = ''
    if variacao.imagem:
        imagem_url = variacao.imagem.url
    elif produto.imagem:
        imagem_url = produto.imagem.url 
    
    



    # O problema estava no uso de "self.request" dentro de uma view baseada em função (function-based view).
    # A palavra-chave "self" só é utilizada dentro de métodos de @3@ classes @3@, como nas views baseadas em classe (Class-Based Views).
    # Como essa é uma função normal, o correto é usar apenas "request" diretamente.
    if variacao.estoque < 1:
        messages.error(
            request,
                       'estoque insuficiente')
        return redirect('produto:detalhe', slug=Produto.objects.get(id=id).slug) 

    if variacao_id_str in carrinho:
        quantidade_carrinho = carrinho[variacao_id]['quantidade']
        quantidade_carrinho += 1
        # carrinho[variacao_id_str]['quantidade'] += 1
        if variacao_estoque < quantidade_carrinho:
            messages.warning(
                request,f'Estoque insuficiente para {quantidade_carrinho} no produto '
                f'{variacao.nome}'
            )

            quantidade_carrinho = variacao_estoque

        carrinho[variacao_id_str]['quantidade'] = quantidade_carrinho
        carrinho[variacao_id_str]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho  
        carrinho[variacao_id_str]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                quantidade_carrinho
    else:
        carrinho[variacao_id_str] = {
        'produto_id': produto.id or variacao_id,
        'nome_produto': produto.nome,  # <-- nome do produto
        'nome': variacao.nome or produto.nome,  # <-- nome da variação
        'preco': variacao.preco,
        'preco_unitario': preco_unitario,
        'preco_unitario_promocional': preco_unitario_promocional,
        'preco_quantitativo': preco_unitario,
        'preco_quantitativo_promocional': preco_unitario_promocional,
        'preco_promocional': variacao.preco_promocional,
        'quantidade': 1,
        'slug': produto.slug,
        'imagem': imagem_url,  # <-- url da imagem
}

    request.session.save()
    print(carrinho)
    request.session['carrinho'] = carrinho
    request.session.modified = True
    messages.success(request, f'Produto "{variacao.produto.nome}" ({variacao.nome}) )) adicionado ao carrinho. {carrinho[variacao_id_str]["quantidade"]}')


    return redirect('produto:detalhe', slug=variacao.produto.slug)

def remover_carrinho(request, id):
    carrinho = request.session.get('carrinho', {})
    
    if str(id) in carrinho:
        del carrinho[str(id)]
        request.session['carrinho'] = carrinho
        request.session.modified = True
        messages.success(request, 'Produto removido do carrinho.')

    return redirect('produto:carrinho')

def carrinho(request):
    carrinho = request.session.get('carrinho', {})
    total = 0
    total_promocional = 0

    for item in carrinho.values():
        total += item.get('preco_quantitativo', 0)
        total_promocional += item.get('preco_quantitativo_promocional', 0)

    context = {
        'carrinho': carrinho,
        'total': total,
        'total_promocional': total_promocional,
    }
    return render(request, 'produto/carrinho.html', context)

def finalizar(request):
    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('produto:lista')

    # Aqui você poderia salvar o pedido, enviar e-mail, etc.
    messages.success(request, 'Compra finalizada com sucesso!')
    request.session['carrinho'] = {}
    return redirect('produto:lista')

def esvaziar_carrinho(request):

    request.session['carrinho'] = {}
    request.session.modified = True
    messages.success(request, 'Carrinho esvaziado.')
    return redirect('produto:carrinho')

def resumo_compra(request):
    if not request.user.is_authenticated:
        return redirect('produto:lista')
    perfil = Perfil.objects.filter(usuario=request.user).exists()
    if not perfil:
        messages.error(request,'É necessario que você tenha dados de perfil cadastrados')
        return redirect('perfil:criar')
    contexto = {
        'usuario':request.user,
        'carrinho':request.session['carrinho'],

    }
    return render (request,'produto/resumo.html',contexto)


def whatsapp_pedido(request):
    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('produto:lista')

    if not request.user.is_authenticated:
        messages.error(request, 'Você precisa estar logado.')
        return redirect('perfil:criar')

    perfil = getattr(request.user, 'perfil', None)
    if not perfil:
        messages.error(request, 'Você precisa preencher seu perfil.')
        return redirect('perfil:criar')

    mensagem = f"📦 *Novo Pedido*\n\n"
    mensagem += f"👤 *Nome:* {request.user.first_name} {request.user.last_name}\n"
    mensagem += f"📧 *Email:* {request.user.email}\n"
    mensagem += f"📍 *Endereço:* {perfil.endereco}, {perfil.cidade} - {perfil.estado}, {perfil.cep}\n"
    mensagem += f"🆔 *CPF:* {perfil.cpf}\n\n"
    mensagem += "🛒 *Itens do Carrinho:*\n"

    total = 0
    for item in carrinho.values():
        nome = item.get("nome")
        quantidade = item.get("quantidade", 1)
        preco = item.get("preco_unitario_promocional") or item.get("preco_unitario")
        subtotal = quantidade * preco
        total += subtotal

        mensagem += f"- {nome} | Quantidade: {quantidade} | R$ {preco:.2f} cada\n"

    mensagem += f"\n💰 *Total:* R$ {total:.2f}\n"
    mensagem += "\nPor favor, confirme o pedido!"

    # Codificar para URL
    mensagem_codificada = urllib.parse.quote(mensagem)

    # Seu número de WhatsApp com DDI (ex: +55 para Brasil)
    numero = '5561998645333'  # exemplo: 5599999999999
    link = f"https://wa.me/{numero}?text={mensagem_codificada}"

    return HttpResponseRedirect(link)