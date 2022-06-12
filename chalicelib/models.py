from peewee import Model, ForeignKeyField, DoubleField, IntegerField, CharField, DateField, TextField, BooleanField, \
    PostgresqlDatabase

db = PostgresqlDatabase(database='projectbazar', user='postgres', password='1234')


class BaseModel(Model):
    class Meta:
        database = db


class Endereco(BaseModel):
    rua = TextField()
    numero = CharField()
    complemento = TextField(null=True)
    estado = CharField()
    cidade = CharField()


class Cliente(BaseModel):
    nome = CharField()
    cpf = CharField()
    telefone = CharField()
    endereco = ForeignKeyField(Endereco)


class Pagamento(BaseModel):
    esta_pago = BooleanField()
    forma_pagamento = CharField()


class Produto(BaseModel):
    nome = CharField()
    quantidade = IntegerField()
    preco = DoubleField()
    fornecedor = CharField()


class Pedido(BaseModel):
    cliente = ForeignKeyField(Cliente)
    valor_total = DoubleField()
    pagamento = ForeignKeyField(Pagamento)


class ItensPedidos(BaseModel):
    produto = ForeignKeyField(Produto)
    pedido = ForeignKeyField(Pedido)
    quantidade = IntegerField()
    preco = DoubleField()


class Carrinho(BaseModel):
    data_compra = DateField()
    valor_total = DoubleField()
    frete = DoubleField()
    cliente = ForeignKeyField(Cliente)


class ItensCarrinho(BaseModel):
    carrinho = ForeignKeyField(Carrinho)
    produto = ForeignKeyField(Produto)
    quantidade = IntegerField()
    preco = DoubleField()


if db.table_exists('carrinho') is not None:
    db.create_tables(BaseModel.__subclasses__())
