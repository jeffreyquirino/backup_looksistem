from pagseguro import PagSeguro

from django.db import models
from django.conf import settings

from catalog.models import Product

class CartItemManager(models.Manager): #feita para adicionar alguns metados para facilitar

    def add_item(self, cart_key, product): #funcao para adicionar intem no carrinho
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product) 
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(
                cart_key=cart_key, product=product, price=product.price
            )
        return cart_item, created

class CartItem(models.Model):

    cart_key = models.CharField(
        'Chave do Carrinho', max_length=40, db_index=True
    )
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'),) #criar um index de unicidade, o banco de dados evita ter o mesmo produto duas vezes

    def __str__(self):
        return '{} [{}]'.format(self.product, self.quantity)

class OrderManager(models.Manager): #para que a logica de criação do pedido esteja unificada em um determinado metodo

    def create_order(self, user, cart_items): #recebe usuario e o cart
        order = self.create(user=user)  
        for cart_item in cart_items: 
            order_item = OrderItem.objects.create(
                order=order, quantity=cart_item.quantity, product=cart_item.product,
                price=cart_item.price
            )
        return order #cria os intems do pedidos e retorna o pedido

class Order(models.Model): #representa o pedido de forma geral

    STATUS_CHOICES = (
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelada'),
    )

    PAYMENT_OPTION_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário') #indica que o usuario é o user logado
    status = models.IntegerField(
        'Situação', choices=STATUS_CHOICES, default=0, blank=True
    ) #situação tem mais de um status definidos em  STATUS_CHOICES
    payment_option = models.CharField(
        'Opção de Pagamento', choices=PAYMENT_OPTION_CHOICES, max_length=20, default='deposit'
    )  

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido #{}'.format(self.pk)

    def products(self): #retorna todos os produtos no pedido
        products_ids = self.items.values_list('product') #retorna apenas os produtos
        return Product.objects.filter(pk__in=products_ids) #como se fosse um select dentro de um select, buscando para todos os prodtos, mais os Ids estão em outros selects.

    def total(self): #funcao do total, aggregate_queryset metodo do django de agregar o mesmo tem funcao de soma
        aggregate_queryset = self.items.aggregate(  
            total=models.Sum(
                models.F('price') * models.F('quantity'), #nessa logica ele pega o preço e multiplica pela quantidade, o '.f' é como se fosse um calculo no select
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']

    def pagseguro_update_status(self, status): #status do pagseguro
        if status == '3': #status 3 é concluido
            self.status = 1 #entao setamos o 1 
        elif status == '7': #status cancelado
            self.status = 2
        self.save()

    def complete(self):
        self.status = 1
        self.save()

    def pagseguro(self):
        self.payment_option = 'pagseguro'
        self.save()
        #if settings.PAGSEGURO_SANDBOX: #valida para estar no ambiente de sendbox
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox':settings.PAGSEGURO_SANDBOX}
        ) #Cria a instancia do pagseguro, passando o email configurado no settings, e o token tabem. 
        #else:
        #    pg = PagSeguro(
        #        email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN
        #    )#config sobrepoe a configuração padrao da API
        pg.sender = {
            'email': self.user.email
        } #informações de quem ta realizando a compra
        pg.reference_prefix = None #prfixo adicionado junto com o id pedido
        pg.shipping = None #dados de entrega
        pg.reference = self.pk #id do pedido
        for item in self.items.all(): #para cada item de pedido, ele adicioa carrinho
            pg.items.append(
                {
                    'id': item.product.pk,
                    'description': item.product.name,
                    'quantity': item.quantity,
                    'amount': '%.2f' % item.price #ele pede o preço em forma de STR
                }
            )
        return pg 

    def paypal(self):
        paypal_dict = {
            'upload': '1', 
            'business': settings.PAYPAL_EMAIL, #é o email cadastrado no paypal
            'invoice': self.pk, #referencia do ID
            'cmd': '_cart', #este _cart é para indentificar que é um carrinho de compra
            'currency_code': 'BRL', #moeda utilizada
            'charset': 'utf-8',
        }
        index = 1
        for item in self.items.all():  #ele pega os intem de acordo com quantos voce tem no carrinho
            paypal_dict['amount_{}'.format(index)] = '%.2f' % item.price
            paypal_dict['item_name_{}'.format(index)] = item.product.name
            paypal_dict['quantity_{}'.format(index)] = item.quantity
            index = index + 1
        return paypal_dict

class OrderItem(models.Model):

    order = models.ForeignKey(Order, verbose_name='Pedido', related_name='items') #como um filtro que terao somente os intems associado ao pedido
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens dos pedidos'

    def __str__(self):
        return '[{}] {}'.format(self.order, self.product) #o mesmo exibe o produto e o pedido


def post_save_cart_item(instance, **kwargs): #sinals são sinais que são desperados quando acontece um derterminado evento
    if instance.quantity < 1: #instance 
        instance.delete()


models.signals.post_save.connect(
    post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item'
) #sender garante que o sinal so seja disparado quando for cart_item
        #dispatch_uid= garante q seja salvo so uma vez