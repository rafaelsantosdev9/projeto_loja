from django.shortcuts import render, get_object_or_404, redirect

def criar (request):
    return render(request, 'loja/produtos.html')
def atualizar (request):
    return render(request, 'loja/produtos.html')
def login (request):
    return render(request, 'loja/produtos.html')
def logout (request):
    return render(request, 'loja/produtos.html')