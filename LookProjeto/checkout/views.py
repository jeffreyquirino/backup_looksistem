
from pagseguro import PagSeguro
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED #ST_PP_COMPLETED valor de quando a transação está terminada
from paypal.standard.ipn.signals import valid_ipn_received

from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import (
    RedirectView, TemplateView, ListView, DetailView
)
from django.forms import modelformset_factory #tras a classe modelformeset 
from django.contrib import messages #sistema de menssagem
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

#from paypal.standard.forms import PayPalPaymentsForm #formaluario do paypay 


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
            cart_items.delete() #apos fazer o pedido ele remove o intem do carrinho de compras
        else:
            messages.info(request, 'Não há itens no carrinho de compras')
            return redirect('checkout:cart_item')
        response = super(CheckoutView, self).get(request, *args, **kwargs)
        response.context_data['order'] = order
        return response

class OrderListView(LoginRequiredMixin, ListView): #é uma view que o user tem q estar logado, lista de pedidos

    template_name = 'checkout/order_list.html' #pagina dentro do MINHA CONTA 
    paginate_by = 10 

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-pk') #ele pega todos os pedidos deste usuario

class OrderDetailView(LoginRequiredMixin, DetailView): #DetailView é uma generic view que serve para detalhar um determinado objeto

    template_name = 'checkout/order_detail.html' #template que vai exibir um pedido

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user) #baseado nessa queryset, ou seja exibe pedido desse usario


class PagSeguroView(LoginRequiredMixin, RedirectView): #login requirido, e redireciona

    def get_redirect_url(self, *args, **kwargs): #ele pega a url de redirecionamento
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user), pk=order_pk
        ) #pega o pedido ou 404, usamos uma query set para pegar o pedido do usuario atual
        pg = order.pagseguro() #metodo criado em models, que tras um carrinho com os itens
        pg.redirect_url = self.request.build_absolute_uri(
            reverse('checkout:order_detail', args=[order.pk]) 
        ) #se usasemos so o reverse ele nos retornaria a URL parcial, com esse metodo build_absolute_uri ele pega o dominio que esta sendo acessado e ele controi uma url dentro desse dominio.
        pg.notification_url = self.request.build_absolute_uri(
            reverse('checkout:pagseguro_notification')
        ) #URL de notificação 
        response = pg.checkout() #esse response tem um response.payment_url atributo de url de pagamento
        return response.payment_url

class PaypalView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/paypal.html'

    def get_context_data(self, **kwargs):
        context = super(PaypalView, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('pk') #id do pedido
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user), pk=order_pk
        ) #ele tenta pegar o pedido com o id, ele so pode pegar deste usuario evitande dele pagar de outro usuario
        paypal_dict = order.paypal()
        paypal_dict['return_url'] = self.request.build_absolute_uri(
            reverse('checkout:order_list') 
        ) #url direciona usuario apos finalizar a compra para todos os pedidos
        paypal_dict['cancel_return'] = self.request.build_absolute_uri(
            reverse('checkout:order_list')
        ) #caso ele cancele o pagamnto , direciona para o pedidos
        paypal_dict['notify_url'] = self.request.build_absolute_uri(
            reverse('paypal-ipn')
        ) #paypal ipn é url do proprio paypal, ele manda uma url para nos notificar uma atualização do pedido
        context['form'] = PayPalPaymentsForm(initial=paypal_dict) #contexo form definido 
        return context


@csrf_exempt #decorator do csrf para que podemos ter a viws que é um POST, mas a mesmo não tem a necessidade de realizar a validação de segurança
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None) #pagseguro realiza um POST e envia o notificationCode
    if notification_code: #valida de o code foi realemnte criado, se sim ele cria um novo carrinho
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        notification_data = pg.check_notification(notification_code) #ele checa o cod de verificação
        status = notification_data.status #status do pagseguro
        reference = notification_data.reference #id do pedido
        try:
            order = Order.objects.get(pk=reference) #ele busca o pedido
        except Order.DoesNotExist:
            pass
        else:
            order.pagseguro_update_status(status) #se houver o pedido
    return HttpResponse('OK')

#sender objeto ipn , api do django paypal fornece, se receber o status completa ele dispara essa funcao
def paypal_notification(sender, **kwargs):  
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED and \
        ipn_obj.receiver_email == settings.PAYPAL_EMAIL:
        try:
            order = Order.objects.get(pk=ipn_obj.invoice)
            order.complete()
        except Order.DoesNotExist:
            pass


valid_ipn_received.connect(paypal_notification) #recebeu uma notificação, e ele conecta uma funcao neste sinal 


create_cartitem = CreateCartItemView.as_view()
cart_item = CartItemView.as_view() #criando views chamaveis
checkout = CheckoutView.as_view()
order_list = OrderListView.as_view()
order_detail = OrderDetailView.as_view()
pagseguro_view = PagSeguroView.as_view()
paypal_view = PaypalView.as_view()