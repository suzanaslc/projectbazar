from chalicelib.models import ItensPedidos, Pagamento, Carrinho, ItensCarrinho, Cliente, Pedido


def adicionar_carrinho(carrinho_id, item):
    Carrinho.get(id=carrinho_id)
    item_carrinho = ItensCarrinho(carrinho=carrinho_id, produto=item['id_produto'],
                                  quantidade=item['quantidade'], preco=item['preco'])
    item_carrinho.save()
    query = Carrinho.update(valor_total=Carrinho.valor_total + item['preco']).where(Carrinho.id == carrinho_id)
    query.execute()
    return item_carrinho


def calcular_valor_total_frete(valor_total, estado):
    if valor_total > 100:
        return valor_total
    else:
        if estado == 'RJ':
            return valor_total
        elif estado == 'SP':
            return valor_total + 10
        else:
            return valor_total + 20


def save_pagamento(forma_pagamento):
    pagamento = Pagamento(esta_pago=False, forma_pagamento=forma_pagamento)
    pagamento.save()
    return pagamento


def save_itens(itens, id_pedido):
    valor_total = 0
    for item in itens:
        item_classe = ItensPedidos(produto=item.produto,
                                   pedido=id_pedido,
                                   quantidade=item.quantidade,
                                   preco=item.preco)
        item_classe.save()
        valor_total += item.preco
    return valor_total


def simular_frete(itens, estado):
    valor_total = 0
    for item in itens:
        valor_total += item.preco
    if valor_total > 100:
        return 0
    else:
        if estado == 'RJ':
            return 0
        elif estado == 'SP':
            return 10
        else:
            return 20


def criar_pedido(cliente_id, carrinho_id, json_body):
    cliente = Cliente.get_by_id(cliente_id)
    pagamento = save_pagamento(json_body['forma_pagamento'])
    itens = ItensCarrinho.select().where(ItensCarrinho.carrinho == carrinho_id)
    pedido = Pedido(cliente=cliente_id, valor_total=0, pagamento=pagamento)
    pedido.save()
    valor_total = save_itens(itens, pedido.id)
    valor_total = calcular_valor_total_frete(valor_total, cliente.endereco.estado)
    query = Pedido.update(valor_total=valor_total).where(Pedido.id == pedido.id)
    query.execute()
    return pedido.id


def fazer_pagamento(id_pedido):
    pedido = Pedido.get(Pedido.id == id_pedido)
    pagamento_id = pedido
    query = Pagamento.update(esta_pago=True).where(Pagamento.id == pagamento_id)
    query.execute()
    pagamento = Pagamento.get(Pagamento.id == pagamento_id)
    return pagamento.esta_pago
