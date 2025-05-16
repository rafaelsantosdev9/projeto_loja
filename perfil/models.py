from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from utils.validadordecpf import valida_cpf
# Create your models here.
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE,
                                   verbose_name='Usuário')
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)
    
    endereco = models.CharField(max_length=500)
    cpf = models.CharField(max_length=11,help_text='Apenas numeros',)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=8)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='SP',
        choices=(  
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AM', 'Amazonas'),
    ('AP', 'Amapá'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MG', 'Minas Gerais'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('PR', 'Paraná'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('RS', 'Rio Grande do Sul'),
    ('SC', 'Santa Catarina'),
    ('SE', 'Sergipe'),
    ('SP', 'São Paulo'),
    ('TO', 'Tocantins'),)
    )

    def __str__(self) -> str:
        return f'{self.usuario}'
    
    def clean(self):
       error_messages = {}
       #logica para cpf unico
       cpf_enviado = self.cpf or None
       cpf_salvo = None
       perfil = Perfil.objects.filter(cpf = cpf_enviado).first()
       if perfil:
           cpf_salvo = perfil.cpf
           if cpf_salvo is not None and self.pk != perfil.pk:
               error_messages['cpf'] = 'CPF já existe'


       if not valida_cpf(self.cpf): 
           error_messages['cpf'] = 'Digite um cpf valido'
       else:
           ...
           self.cpf = f'{self.cpf[:3]}-{self.cpf[3:6]}-{self.cpf[6:9]}-{self.cpf[9:]}'
           
        #digitar apenas numeros
       if re.search(r'[^0-9]',self.cep) or len(self.cep) < 8:
           error_messages['cep'] = 'CEP invalido, digite apenas numero'
       else:
           self.cep = f'{self.cep[:5]}-{self.cep[5:]}'
                   
        #por esse if que mostra os erros , por conta do validation
       if error_messages:
           raise ValidationError(error_messages)
               
               


    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'    