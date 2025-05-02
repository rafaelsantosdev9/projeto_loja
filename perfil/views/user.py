from django.shortcuts import render, get_object_or_404, redirect
from perfil.forms import UserForm,PerfilForm
from django.contrib.auth import authenticate, login as auth_login
#para salvar o carrinho
import copy
def criar(request):
    if request.user.is_authenticated:
        return redirect('perfil:atualizar')

    user_instance = None
    usuario_logado = None
    
    userform = UserForm(
        data=request.POST or None,
        instance=user_instance,
        usuario=usuario_logado
    )

    perfilform = PerfilForm(data=request.POST or None)

    if request.method == 'POST':
        if userform.is_valid() and perfilform.is_valid():
            username = userform.cleaned_data.get('username')
            password = userform.cleaned_data.get('password')
            email = userform.cleaned_data.get('email')

            usuario = userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

             # 🔐 AUTENTICA E LOGA O USUÁRIO
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Loga o usuário

            return redirect('perfil:atualizar')  

    context = {
        'userform': userform,
        'perfilform': perfilform
    }

    return render(request, 'perfil/criar.html', context)

def atualizar(request):
    print('view atualizar foi chamada')

    userform = UserForm(
        data=request.POST or None,
        instance=request.user,
        usuario=request.user
    )

    
    carrinho = copy.deepcopy(request.session.get('carrinho',{}))
    #perfil
    perfil_instance = getattr(request.user, 'perfil', None)

    perfilform = PerfilForm(
    data=request.POST or None,
    instance=perfil_instance
        )
    # se for post
    if request.method == 'POST':
        # if userform.is_valid() and perfilform.is_valid():
        if userform.is_valid():
            username = userform.cleaned_data.get('username')
            password = userform.cleaned_data.get('password')
            email = userform.cleaned_data.get('email')
            first_name = userform.cleaned_data.get('first_name')
            last_name = userform.cleaned_data.get('last_name')
           
            if request.user.is_authenticated:
            
                usuario = request.user
                usuario.username = username
                usuario.email = email
                usuario.first_name = first_name
                usuario.last_name  = last_name
                

                # precisa salvar o carrinho antes de alterar a senha e restaurá-lo após o re-login.
                #se não o carrinho se perde quando os dados são atualizados
                if password:
                    carrinho_backup = copy.deepcopy(request.session.get('carrinho', {}))  #salva antes de perder a sessão

                    usuario.set_password(password)
                    usuario.save()

                    auth_login(request, usuario)

                    request.session['carrinho'] = carrinho_backup  #restaura apos reautenticar
                    request.session.save()
                else:
                    usuario.save()    

                
                
                

                perfil = perfilform.save(commit=False)
                perfil.usuario = request.user
                perfil.save()

            else:
                 
                 usuario = userform.save(commit=False)
                 usuario.set_password(password)
                 usuario.save()

                 perfil = perfilform.save(commit=False)
                 perfil.usuario = usuario
                 perfil.save()

             # 🔐 AUTENTICA E LOGA O USUÁRIO
                 user = authenticate(username=username, password=password)
                 if user is not None:
                    auth_login(request, user)  # Loga o usuário
                 carrinho = copy.deepcopy(request.session.get('carrinho', {}))
                 request.session['carrinho'] = carrinho
                 request.session.save()
                 return redirect('perfil:atualizar')  
            if password:
                autentica = authenticate(request,username = usuario , password = password)
                if autentica:
                    auth_login(request, user=usuario)

            

    context = {
        'userform': userform,
        'perfilform': perfilform,
    }

    return render(request, 'perfil/criar.html', context)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            auth_login(request, usuario)

            # 🔁 Restaurar carrinho da sessão, se houver
            carrinho = copy.deepcopy(request.session.get('carrinho', {}))
            request.session['carrinho'] = carrinho
            request.session.save()

            
            return redirect('produto:lista')  # Ou onde quiser mandar o usuário após login
        else:
            ...

    return render(request, 'perfil/login.html')  # Certifique-se de que esse é o nome correto do template
def logout (request):
    return render(request, 'perfil/criar.html')