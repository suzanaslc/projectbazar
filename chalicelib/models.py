from peewee import Model, ForeignKeyField, DoubleField, IntegerField, CharField, DateField, TextField, BooleanField, \
    PostgresqlDatabase


class BaseModel(Model):
    class Meta:
        database = PostgresqlDatabase(database='host')


class Cliente(BaseModel):
    nome = CharField()
    cpf = CharField()
    telefone = CharField()


class Endereco(BaseModel):
    cliente = ForeignKeyField(Cliente)
    rua = TextField()
    numero = CharField()
    complemento = TextField()
    estado = CharField()
    cidade = CharField()


class Entrega(BaseModel):
    endereco = ForeignKeyField(Endereco)
    frete = DoubleField()


class Pagamento(BaseModel):
    cliente = ForeignKeyField(Cliente)
    esta_pago = BooleanField()


class Produto(BaseModel):
    nome = CharField()
    quantidade = IntegerField()
    preco = DoubleField()
    fornecedor = CharField()


class Pedido(BaseModel):
    cliente = ForeignKeyField(Cliente)
    valor_total = DoubleField()
    entrega = ForeignKeyField(Entrega)
    pagamento = ForeignKeyField(Pagamento)

    def calcular_valor_total_pedido(self):
        self.valor_total = 0
        query = (ItensPedidos
                 .select(ItensPedidos, Pedido, Produto)
                 .join(Pedido)
                 .switch(ItensPedidos)
                 .join(Produto))
        for item in query:
            self.valor_total += item.preco
        return self.valor_total

    def calcular_valor_total_frete(self):
        if self.valor_total <= 100:
            if self.cliente.endereco.estado == 'SP':
                self.valor_total += 10
            elif self.cliente.endereco.estado != 'RJ':
                self.valor_total += 20
        return self.valor_total


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

    def simular_frete(self):
        if self.valor_total > 100:
            return 0
        else:
            if self.cliente.estado == 'RJ':
                return 0
            elif self.cliente.endereco.estado == 'SP':
                return 10
            else:
                return 20


class ItensCarrinho(BaseModel):
    carrinho = ForeignKeyField(Carrinho)
    produto = ForeignKeyField(Produto)
    quantidade = IntegerField()
    preco = DoubleField()
