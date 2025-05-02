from django.shortcuts import render, get_object_or_404, redirect

def pagar (request):
    return render(request, 'loja/produtos.html')


def fecharpedido(request):
    return render(request, 'loja/produtos.html')

def detalhe(request,id):
    return render(request, 'loja/produtos.html')

