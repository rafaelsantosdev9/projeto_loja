from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.FloatField()
    descricao_curta = models.TextField(max_length=200)
    imagem = models.ImageField(
        upload_to='global/images/imagem-produtos',
        null=True,
        blank=True)
    tipo = models.CharField(
        default='ABS',max_length=4,choices=(('ABS','ABS'),('PLA','PLA'),('PETG','PETG')))
        
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.nome