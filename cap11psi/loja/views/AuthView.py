from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from loja.forms.AuthForm import LoginForm, RegisterForm

def login_view(request):
    message = None

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)  # Instancia o formulário com os dados POST
        
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']  # Pega os dados validados do formulário
            password = loginForm.cleaned_data['password']

            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Adicione as linhas a seguir
                _next = request.GET.get('next')
                if _next is not None:
                    return redirect(_next)
                else:
                    return redirect("/")
                # Até aqui
                
            else:
                message = {'type': 'danger', 'text': 'Dados de usuário incorretos'}

    else:
        loginForm = LoginForm()  # Instancia o formulário vazio se o método não for POST

    context = {
        'form': loginForm,
        'message': message,
        'title': 'Login',
        'button_text': 'Entrar',
        'link_text': 'Registrar',
        'link_href': '/register'
    }
    
    return render(request, template_name='auth/auth.html', context=context, status=200)

def logout_view(request):
    logout(request)
    return redirect('/login')

def register_view(request):
    message = None
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)  # Instancia o formulário com os dados POST
        
        if registerForm.is_valid():
            username = registerForm.cleaned_data['username']
            email = registerForm.cleaned_data['email']
            password = registerForm.cleaned_data['password']

            # Verificando se já existe um usuário ou e-mail
            verifyUsername = User.objects.filter(username=username).first()
            verifyEmail = User.objects.filter(email=email).first()

            if verifyUsername:
                message = {'type': 'danger', 'text': 'Já existe um usuário com este username!'}
            elif verifyEmail:
                message = {'type': 'danger', 'text': 'Já existe um usuário com este e-mail!'}
            else:
                # Cria o usuário
                user = User.objects.create_user(username=username, email=email, password=password)
                if user:
                    message = {'type': 'success', 'text': 'Conta criada com sucesso!'}
                else:
                    message = {'type': 'danger', 'text': 'Um erro ocorreu ao tentar criar o usuário.'}
        else:
            # Caso o formulário não seja válido
            message = {'type': 'danger', 'text': 'Por favor, corrija os erros no formulário.'}

    else:
        registerForm = RegisterForm()  # Instancia o formulário vazio se o método não for POST

    context = {
        'form': registerForm,
        'message': message,
        'title': 'Registrar',
        'button_text': 'Registrar',
        'link_text': 'Login',
        'link_href': '/login'
    }
    
    return render(request, template_name='auth/auth.html', context=context, status=200)
