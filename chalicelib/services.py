from chalicelib.models import ItensPedidos, Pedido, Produto, Pagamento


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
        item_classe = ItensPedidos(produto=item['id_produto'],
                                   pedido=id_pedido,
                                   quantidade=item['quantidade'],
                                   preco=item['preco'])
        item_classe.save()
        valor_total += item['preco']
    return valor_total


def simular_frete(itens, estado):
    valor_total = 0
    for item in itens:
        valor_total += item['preco']
    if valor_total > 100:
        return 0
    else:
        if estado == 'RJ':
            return 0
        elif estado == 'SP':
            return 10
        else:
            return 20
