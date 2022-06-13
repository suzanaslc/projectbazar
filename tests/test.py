import json

from chalice.test import Client
from app import app
from chalicelib import services
from chalicelib.models import ItensCarrinho, Cliente


def testar_adicionar_carrinho(cliente_id, carrinho_id):
    with Client(app) as client:
        response = client.http.put(
            f'/{cliente_id}/carrinho/{carrinho_id}',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({
                'item': {
                    'id_produto': 1,
                    'quantidade': 1,
                    'preco': 20.0
                }
            })
        )
        assert response.json_body == {'id_item': 19}


def testar_simular_frete(cliente_id, carrinho_id):
    with Client(app) as client:
        response = client.http.get(
            f'/{cliente_id}/carrinho/{carrinho_id}/frete'
        )
        assert response.json_body == {'frete': 0}


def testar_criar_pedido(cliente_id, carrinho_id):
    with Client(app) as client:
        response = client.http.post(
            f'/{cliente_id}/carrinho/{carrinho_id}/fechar_pedido',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({
                "forma_pagamento": "debito"
            })
        )
    assert response.json_body == {'id_pedido': 16}


def testar_fazer_pagamento(cliente_id, pedido_id):
    with Client(app) as client:
        response = client.http.post(
            f'/{cliente_id}/pedidos/{pedido_id}/pagamento'
        )
    assert response.json_body == {'status_pagamento': True}


if __name__ == '__main__':
    testar_fazer_pagamento(1, 12)
