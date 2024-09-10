from components.ServiceClass import Service
from tkinter.messagebox import askokcancel
import json
import os

def save_data(self):
        servico_old = self.old_service
        val = askokcancel("Salvar-Serviço", "Salvar serviço?")
        if val:
            val_orderserver = self.val_orderserver
            self.servico = Service(self.servico.ordem, self.enter_ncliente.get(), self.enter_telefone.get(), self.enter_date.get(), self.enter_placa.get(), self.enter_marca.get(), self.enter_modelo.get(), self.enter_cor.get(), self.enter_ano.get(), self.enter_kmatual.get(), self.my_text.get("1.0", "end-1c"), self.maodeobra, self.produtos, self.enter_desconto.get())

            nomes_arquivos = os.listdir("./JSON_db/")
            for nome_arquivo in nomes_arquivos:
                if self.servico.ordem in nome_arquivo and ".json" in nome_arquivo:
                    os.remove("JSON_db/"+nome_arquivo)

            if not servico_old:
                # Abrir o arquivo JSON e carregar os dados
                with open("JSON_db/orderserver.json", "r") as arquivo_json:
                    val_orderserver = json.load(arquivo_json)
                self.servico.ordem = f"{(val_orderserver['ordem de servico'][-1] + 1):06d}"

            # Converter a instância em um dicionário
            dados = {
                "ordem": self.servico.ordem,
                "ncliente": self.servico.ncliente,
                "telefone": self.servico.telefone,
                "data": self.servico.data,
                "placa": self.servico.placa,
                "marca": self.servico.marca,
                "modelo": self.servico.modelo,
                "cor": self.servico.cor,
                "ano": self.servico.ano,
                "kmatual": self.servico.kmatual,
                "observacoes": self.servico.observacoes,
                "maodeobra": self.servico.maodeobra,
                "pecas": self.servico.pecas,
                "desconto": self.servico.desconto
            }

            nm = f"{self.servico.ordem}_{self.servico.placa}_{self.servico.ncliente}".upper()
            nome_json = f"JSON_db/{nm}.json"
            with open(nome_json, "w") as arquivo_json:
                json.dump(dados, arquivo_json, indent=4)

            # Listar todos os arquivos na pasta
            nomes_arquivos = os.listdir("./JSON_db/")
            for nome_arquivo in nomes_arquivos:
                if self.servico.ordem in nome_arquivo and ".json" in nome_arquivo:
                    if not int(self.servico.ordem) in val_orderserver["ordem de servico"]:
                        val_orderserver["ordem de servico"].append(int(self.servico.ordem))
                    print(val_orderserver)
                    novo_json = json.dumps(val_orderserver)
                    with open("JSON_db/orderserver.json", "w") as arquivo_json:
                        arquivo_json.write(novo_json)

            self.val_orderserver = val_orderserver
            self.old_service = nome_json
            self.add_bbtc()

            return nome_json[8:-5]

def def_address(address):
    address
    old_service = False
    if address:
        with open("JSON_db/" + address + ".json", "r") as file_json:
            old_service = json.load(file_json)

    return old_service