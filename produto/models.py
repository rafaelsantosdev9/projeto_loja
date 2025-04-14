from django.db import models
#redimensionar imagem, precisa do os e Image
#########
from PIL import Image
import os  
from django.conf import settings
#transforma uma string em um formato limpo e legível para ser usado como parte de uma URL
from django.utils.text import slugify
########
from utils import utils



class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.FloatField(verbose_name='Preço')
    preco_promocional = models.FloatField(default=0,verbose_name='Preço Promocional')
    descricao_curta = models.TextField(max_length=200)
    imagem = models.ImageField(
        upload_to='global/images/imagem-produtos',
        null=True,
        blank=True)
    
        
    slug = models.SlugField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.nome
    
    def get_preco_formatado(self):
        #formatação do preço              trocando ponto por virgula
        return utils.formata_preco(self.preco)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_formatado_promo(self):
        return f'R$ {self.preco_promocional:.2f}'.replace('.',',')
    get_preco_formatado_promo.short_description = 'Preço Promocional'

    def resize_image(self,image,new_width =800):
        #diretorio da imagem
        img_full_path = os.path.join(settings.MEDIA_ROOT,image.name)
        #abrir a imagem
        img_pil = Image.open(img_full_path)
        #mostrando a altura e largura da imagem
        original_width, original_height = img_pil.size
        #logica para redimensionar a imagem
        if original_width <= new_width:
            img_pil.close()
            return
        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width,new_height),Image.LANCZOS)
        new_img.save(
            img_full_path,
            quality=50,
            optimize=True
        )
        
        
       
    def save(self,*args,**kwargs):
       
       if not self.slug:
           #cria slug automaticamente, colocando o nome do produto e o id
           slug = f'{slugify(self.nome)}'
           self.slug = slug
       super().save(*args,**kwargs)
       max_image_size = 800
       if self.imagem:
           
           self.resize_image(self.imagem,max_image_size) 
class Variacao(models.Model):
    produto = models.ForeignKey(Produto,on_delete=models.CASCADE)    
    nome = models.CharField(max_length=255,blank=True,null=True)  
    preco = models.FloatField()     
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.nome or self.produto.nome
    class Meta:
        verbose_name = 'Variacao'
        verbose_name_plural = 'Variações'