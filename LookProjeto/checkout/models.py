from django.db import models
from django.conf import settings

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
        #('pagseguro', 'PagSeguro'),
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