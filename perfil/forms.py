from django import forms
from . import models 
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
import re

class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='A senha deve ser maior que 6 dígitos'
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação de senha'
    )
    

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'password', 'password2', 'email')

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'classe a classe b',
                    'placeholder': 'Primeiro nome'
                }
            )
        }

    def clean(self):
        
        validation_error_msgs = {}
        cleaned = self.cleaned_data

        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')
        

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).exclude(pk=self.usuario.pk if self.usuario else None).first()


        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'Email já existe'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Senha com menos de 6 caracteres'
        error_msg_required_field = 'O campo é obrigatório'
        

        if self.usuario:
            # Verifica se o username já existe para outro usuário
            if usuario_db and usuario_db != self.usuario:
                validation_error_msgs['username'] = error_msg_user_exists

            # Verifica se o email já existe para outro usuário
            if email_db and email_db.pk != self.usuario.pk:
                validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match
                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short
        else:
            # Para usuários não autenticados (criando conta)
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field
            if not password2_data:
                validation_error_msgs['password2'] = error_msg_required_field
                #comparando se as senhas estão vazias para atualização dela
            if password_data and password2_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if password_data and len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short
                

        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)
