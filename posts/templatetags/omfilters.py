from django import template


# Fazer próprios filtros. Entra no template com |
register = template.Library()  # Usada como decorador.


@register.filter(name='plural_comentarios')  # Decorador e nome para colocar no template.
def plural_comentarios(num_comentarios):
    try:
        num_comentarios = int(num_comentarios)  # Torna variável em inteiro.

        if num_comentarios == 0:
            return f'Não há comentários a serem exibidos.'
        elif num_comentarios ==1:
            return f'{num_comentarios} comentário.'
        else:
            return f'{num_comentarios} comentários.'
    except:
        return f'{num_comentarios} comentário(s)'

