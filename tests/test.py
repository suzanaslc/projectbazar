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
        assert response.json_body == {'id_item': 11}


def testar_simular_frete(cliente_id, carrinho_id):
    with Client(app) as client:
        response = client.http.get(
            f'/{cliente_id}/carrinho/{carrinho_id}/frete'
        )
        assert response.json_body == {'frete': 0}


if __name__ == '__main__':
    testar_adicionar_carrinho(1, 1)
    testar_simular_frete(1, 1)
