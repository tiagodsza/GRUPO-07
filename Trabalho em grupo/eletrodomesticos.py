class Eletrodomesticos:
    def __init__(self, tipo, marca, modelo, data_fabric, preco):
        self.serie = 0
        self.marca = marca
        self.modelo = modelo
        self.data_fabric = data_fabric
        self.preco = preco
        self.tipo = tipo

        @property
        def nome(self):
            return self.nome

        @property
        def cpf(self):
            return self.cpf

        @property
        def endereco(self):
            return self.endereco     