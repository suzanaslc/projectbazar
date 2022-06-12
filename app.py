import traceback

from chalice import Chalice

from chalicelib import services
from chalicelib.models import Pedido, Cliente

app = Chalice(app_name='projectbazar')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/{cliente_id}/pedidos', methods=['POST'])
def create_pedido(cliente_id):
    try:
        request = app.current_request
        json_body = request.json_body
        cliente = Cliente.get_by_id(cliente_id)
        pagamento = services.save_pagamento(json_body['forma_pagamento'])
        itens = json_body['itens']
        pedido = Pedido(cliente=cliente_id, valor_total=0, pagamento=pagamento)
        pedido.save()
        valor_total = services.save_itens(itens, pedido.id)
        valor_total = services.calcular_valor_total_frete(valor_total, cliente.endereco.estado)
        pedido.valor_total = valor_total
        pedido.save()
        return {"id-pedido": pedido.id}
    except Exception as e:
        traceback.format_exc()
        raise e
