from django.forms import ModelForm
from django import forms
from loja.models.Usuario import Usuario
from django.contrib.auth.models import User

# Classe UserForm
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"})
        }

# Classe UserUsuarioForm
class UserUsuarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUsuarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.perfil != 1:
            del self.fields['perfil']  # Deleta o campo 'perfil' se o usuário não for admin

    class Meta:
        model = Usuario
        fields = ['user', 'perfil', 'aniversario']
        widgets = {
            'user': forms.HiddenInput(),
            'perfil': forms.Select(attrs={'class': "form-control"}),
            'aniversario': forms.DateInput(attrs={'class': "form-control", "type": "date"})
        }
