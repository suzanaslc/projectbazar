import json

from chalice.test import Client
from app import app
from chalicelib.models import ItensCarrinho


def testar_adicionar_carrinho():
    with Client(app) as client:
        response = client.http.put(
            '/1/carrinho/1',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({
                'item': {
                    'id_produto': 1,
                    'quantidade': 1,
                    'preco': 20.0
                }
            })
        )
        carrinho = ItensCarrinho.select().order_by(ItensCarrinho.id.desc()).get()
        id_carrinho = carrinho.id
        assert response.json_body == {'id_item': id_carrinho}


if __name__ == '__main__':
    testar_adicionar_carrinho()
