from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 5
    context_object_name = 'posts'  # Iterável que será usado no template.

    def get_queryset(self):  # Método herdade e subscrito de ListView.
        qs = super().get_queryset()
        qs = qs.select_related('categoria_post')  # Melhora a performance com menos buscas na bd.
        qs = qs.order_by('-id').filter(publicado_post=True)  # Posts em ordem decrescente, se publicados.
        qs = qs.annotate(  # Filtro utilizando linguagem SQL.
            numero_comentarios=Count(  # Contar
                Case(  # Se
                    When(comentario__publicado_comentario=True, then=1)  # Quando houver comentário publicado, conta 1.
                )
            )
        )

        return qs


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')  # Termo que é exibido na busca.

        if not termo:
            return qs

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__icontains=termo)
        )
        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)  # Puxa as informações e salva em categoria.

        if not categoria:
            return qs
        # Busca em categoria pelo campo nome_cat pelo termo exato (iexact=)
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs


class PostDetalhes(UpdateView):
    template_name = 'posts/post_detalhes.html'
    model = Post
    form_class = FormComentario
    context_object_name = 'post'  # Contexto para ser usado no template.

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()  # Pega o post utilizado.
        comentarios = Comentario.objects.filter(publicado_comentario=True,  # Filtra por comentário publicado
                                                post_comentario=post.id)
        contexto['comentarios'] = comentarios
        return contexto

    def form_valid(self, form):
        post = self.get_object()  # Pega o formulário.
        comentario = Comentario(**form.cleaned_data)  # Pega as informações refeitas no comentário.
        comentario.post_comentario = post

        if self.request.user.is_authenticated:  # Confirma a autenticação do usuário.
            comentario.usuario_comentario = self.request.user

        comentario.save()
        messages.success(self.request, 'Comentario enviado com sucesso.')
        return redirect('post_detalhes', pk=post.id)

