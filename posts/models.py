from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class Post(models.Model):
    titulo_post = models.CharField(max_length=255, verbose_name='Título')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    data_post = models.DateTimeField(default=timezone.now, verbose_name='Data da Postagem')
    conteudo_post = models.TextField()
    excerto_post = models.TextField()
    categoria_post = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING,
                                      blank=True, null=True, verbose_name='Categoria')
    imagem_post = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True)
    publicado_post = models.BooleanField(default=False, verbose_name='Publicado')

    def __str__(self):
        return self.titulo_post

    # Altera tamanho da foto.
    def save(self):
        super().save()

        img = Image.open(self.imagem_post.path)

        if img.height > 300 or img.width > 300:
            novo_tamanho = (300, 300)
            img.thumbnail(novo_tamanho)
            img.save(self.imagem_post.path)


