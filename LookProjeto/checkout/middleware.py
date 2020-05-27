from .models import CartItem


def cart_item_middleware(get_response): 
    def middleware(request):
        session_key = request.session.session_key #ele pega o session_key
        response = get_response(request)
        if session_key != request.session.session_key and request.session.session_key: #se caso haja alteração na session_key
            CartItem.objects.filter(cart_key=session_key).update(
                cart_key=request.session.session_key
            ) #atualiza a session_key, assim mantendo os intem no carrinhos de comprar MESMO DESLOGADO
        return response
    return middleware

#middleare , sao calsses com metodos que podemos modificar a resposta que será dada.
#ele é executado em toda view.
#session_key é possivel visualizar em cokies/resources/session_key
#vamos usar no carrinho de compra, 