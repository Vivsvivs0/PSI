from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm

def list_usuario_view(request, id=None):
    # Carrega somente usuários, não inclui os admin
    usuarios = Usuario.objects.filter(perfil=2)
    context = {
        'usuarios': usuarios
    }
    return render(request, template_name='usuario/usuario.html', context=context, status=200)

# Método de edição
def edit_usuario_view(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    emailUnused = True
    message = None  # Adiciona a variável message inicialmente como None
    
    if request.method == 'POST':
        usuarioForm = UserUsuarioForm(request.POST, instance=usuario)
        userForm = UserForm(request.POST, instance=request.user)

        # Verifica se o e-mail que o usuário está tentando utilizar já existe em outro perfil
        verifyEmail = Usuario.objects.filter(user__email=request.POST['email']).exclude(user__id=request.user.id).first()
        emailUnused = verifyEmail is None

        if usuarioForm.is_valid() and userForm.is_valid() and emailUnused:
            usuarioForm.save()
            userForm.save()
            message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
            return redirect('nome_da_view_para_redirecionar')  # Ajuste o nome da view conforme necessário
        else:
            if emailUnused:
                # Se o e-mail não está em uso, mas algum dado é inválido
                message = {'type': 'danger', 'text': 'Dados inválidos'}
            else:
                # Se o e-mail já está em uso por outra pessoa
                message = {'type': 'warning', 'text': 'E-mail já usado'}
    
    else:
        usuarioForm = UserUsuarioForm(instance=usuario)
        userForm = UserForm(instance=request.user)

    context = {
        'usuarioForm': usuarioForm,
        'userForm': userForm,
        'message': message  # Inclui a mensagem no contexto
    }

    return render(request, 'usuario/usuario-edit.html', context=context, status=200)
