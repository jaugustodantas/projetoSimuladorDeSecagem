import json

class salvarInfos:
    def __init__(self):
        self.acumulador =[]
    def criarDicionario(self,camada,temperatura,umidade,tempo,tempoAcumulado):
        dados = {
            "camada":camada,
            "tempo":tempo,
            "tempoAcumulado":tempoAcumulado,
            "temperatura":temperatura,
            "umidade":umidade    
        }
        self.acumulador.append(dados)

    def gerarJson (self,nome = "jsonSimulacao"):
        with open(nome,"w",encoding="utf-8") as o:
            json.dump(self.acumulador,o,indent=4)