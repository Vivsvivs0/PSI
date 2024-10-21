from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm

# Lista de usuários, filtrando apenas os que não são administradores (perfil 2)
def list_usuario_view(request, id=None):
    usuarios = Usuario.objects.filter(perfil=2)
    context = {
        'usuarios': usuarios
    }
    return render(request, 'usuario/usuario.html', context=context, status=200)

# Método de edição de usuário
def edit_usuario_view(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    emailUnused = True
    message = None  # Variável para armazenar mensagens de feedback

    if request.method == 'POST':
        usuarioForm = UserUsuarioForm(request.POST, instance=usuario)
        userForm = UserForm(request.POST, instance=request.user)

        # Verifica se o e-mail que o usuário está tentando utilizar já existe em outro perfil
        verifyEmail = Usuario.objects.filter(user__email=request.POST['email']).exclude(user__id=request.user.id).first()
        emailUnused = verifyEmail is None

        # Valida os formulários e se o e-mail está disponível
        if usuarioForm.is_valid() and userForm.is_valid() and emailUnused:
            usuarioForm.save()
            userForm.save()
            message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
            return redirect('nome_da_view_para_redirecionar')  # Ajuste para a view correta
        else:
            # Define a mensagem de erro adequada
            if emailUnused:
                message = {'type': 'danger', 'text': 'Dados inválidos'}
            else:
                message = {'type': 'warning', 'text': 'E-mail já usado'}

    else:
        # Caso não seja POST, carrega os formulários com os dados atuais do usuário
        usuarioForm = UserUsuarioForm(instance=usuario)
        userForm = UserForm(instance=request.user)

    # Contexto para renderização
    context = {
        'usuarioForm': usuarioForm,
        'userForm': userForm,
        'message': message  # Inclui a mensagem no contexto para feedback ao usuário
    }

    return render(request, 'usuario/usuario-edit.html', context=context, status=200)
