import traceback

from chalice import Chalice

from chalicelib import services
from chalicelib.models import Pedido, Cliente, ItensCarrinho, Pagamento

app = Chalice(app_name='projectbazar')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/{cliente_id}/carrinho/{carrinho_id}', methods=['PUT'])
def adicionar_carrinho(cliente_id, carrinho_id):
    try:
        json_body = app.current_request.json_body
        item_carrinho = services.adicionar_carrinho(carrinho_id, json_body['item'])
        return {'id_item': item_carrinho.id}
    except Exception as e:
        traceback.format_exc()
        raise e


@app.route('/{cliente_id}/carrinho/{carrinho_id}/frete', methods=['GET'])
def simular_frete(cliente_id, carrinho_id):
    try:
        cliente = Cliente.get_by_id(cliente_id)
        itens = ItensCarrinho.select().where(ItensCarrinho.carrinho == carrinho_id)
        frete = services.simular_frete(itens, cliente.endereco.estado)
        return {'frete': frete}
    except Exception as e:
        traceback.format_exc()
        raise e


@app.route('/{cliente_id}/carrinho/{carrinho_id}/fechar_pedido', methods=['POST'])
def create_pedido(cliente_id, carrinho_id):
    try:
        json_body = app.current_request.json_body
        pedido_id = services.criar_pedido(cliente_id, carrinho_id, json_body)
        return {"id-pedido": pedido_id}
    except Exception as e:
        traceback.format_exc()
        raise e


@app.route('/{cliente_id}/pedidos/{pedido_id}/pagamento', methods=['POST'])
def fazer_pagamento(cliente_id, pedido_id):
    try:
        status_pagamento = services.fazer_pagamento(pedido_id)
        return {"status_pagamento": status_pagamento}
    except Exception as e:
        traceback.format_exc()
        raise e


@app.route('/cadastro', methods=['POST'])
def cadastrar_cliente():
    try:
        json_body = app.current_request.json_body
        id_cliente = services.cadastrar_cliente(json_body)
        return {"id_cliente": id_cliente}
    except Exception as e:
        traceback.format_exc()
        raise e
