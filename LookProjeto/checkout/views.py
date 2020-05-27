
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import RedirectView, TemplateView
from django.forms import modelformset_factory #tras a classe modelformeset 
from django.contrib import messages #sistema de menssagem
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


from catalog.models import Product

from .models import CartItem, Order


class CreateCartItemView(RedirectView): 

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug']) #ele pega o produto pela url[slug]
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(
            self.request.session.session_key, product
        )
        if created:
            messages.success(self.request, 'Produto adicionado com sucesso')
        else:
            messages.success(self.request, 'Produto atualizado com sucesso')
        #return product.get_absolute_url()
        return reverse('checkout:cart_item') #assim que adicionado ao carrinho redireriona para carrinho


class CartItemView(TemplateView): 

    template_name = 'checkout/cart.html' 

    def get_formset(self, clear=False): #get_formset ja faz a logica de gerar o formset, cada item no carrinho é como se fosse um mini formulario cada
        CartItemFormSet = modelformset_factory(
            CartItem, fields=('quantity',), can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        if session_key:
            if clear:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key)
                )
            else:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key),
                    data=self.request.POST or None
                )
        else:
            formset = CartItemFormSet(queryset=CartItem.objects.none())
        return formset

    def get_context_data(self, **kwargs): #funcao que define o contexto
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset() #essa linha evita reptição de cod so trazendo a func do get_formset
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs) #pegando o contexto
        if formset.is_valid(): #verifica se o formset esta valido
            formset.save() #garante que seja alterado no banco de dados quando salva intem no carrinho ou remove, ele pegas os dados atuais.
            messages.success(request, 'Carrinho atualizado com sucesso') #se for valido
            context['formset'] = self.get_formset(clear=True) #se estiver valido sobescreve o formset
        return self.render_to_response(context) #o template view tem o metodo render_to_response que recebe o contexto e depois rotorna a renderização do template

class CheckoutView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key 
        if session_key and CartItem.objects.filter(cart_key=session_key).exists(): #verifica se a sessão existe, se o user fez algo mesmo
            cart_items = CartItem.objects.filter(cart_key=session_key) #se houver ele carrega no carrinho de compras
            order = Order.objects.create_order(
                user=request.user, cart_items=cart_items 
            ) #e depois faz o pedido chamando o metodo que foir criado em checkout\models.py 'Oder'
        else:
            messages.info(request, 'Não há itens no carrinho de compras')
            return redirect('checkout:cart_item')
        return super(CheckoutView, self).get(request, *args, **kwargs)

create_cartitem = CreateCartItemView.as_view()
cart_item = CartItemView.as_view() #criando views chamaveis
checkout = CheckoutView.as_view()
