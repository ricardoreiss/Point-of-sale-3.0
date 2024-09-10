class Service():
    def __init__(self, ordem, ncliente, telefone, data, placa, marca, modelo, cor, ano, kmatual, observacoes, maodeobra, pecas, desconto):
        self.ordem = ordem
        self.ncliente = ncliente
        self.telefone = telefone
        self.data = data
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
        self.kmatual = kmatual
        self.observacoes = observacoes
        self.maodeobra = maodeobra
        self.pecas = pecas
        if self.maodeobra == '':
            self.maodeobra = 0
        self.maodeobra = float(self.maodeobra)
        self.desconto = desconto
        if self.desconto == '':
            self.desconto = 0