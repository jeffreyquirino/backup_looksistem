#arquivo para fazer paginação de qualquer objeto
from django.template import Library


register = Library() #registra a biblioteca de templates


@register.inclusion_tag('pagination.html') #tag de inclusão, onde vc inclui um template
def pagination(request, paginator, page_obj): #essa funcao pode ser colocada dentro do template
    context = {}
    context['paginator'] = paginator
    context['request'] = request
    context['page_obj'] = page_obj
    getvars = request.GET.copy() #variaveis querystring
    if 'page' in getvars: 
        del getvars['page'] #remove o page na visualização
    if len(getvars) > 0: 
        context['getvars'] = '&{0}'.format(getvars.urlencode()) #ele vai separar mais contextos por & e mantem a querystring
    else:
        context['getvars'] = ''
    return context

