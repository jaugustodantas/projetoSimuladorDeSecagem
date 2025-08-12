import math
class psicometria:
    def __init__(self,temperatura,umidadeRelativaAr,pressaoAtmosferica):
        self.temperatura = temperatura
        self.umidade = umidadeRelativaAr
        self.pressao = pressaoAtmosferica

    def conversaoTemperatura(self):
        return self.temperatura + 273
    
    def calculoPressaoVaporSaturacao(self):
        temperaturaConvertida = self.conversaoTemperatura()
        pressaoVaporSaturacao = ((6*(10**25)/(1000*(temperaturaConvertida**5)))) * math.exp(-6800/temperaturaConvertida)
        return pressaoVaporSaturacao
    
    def calculoPressaoVaporParcial (self):
        pressaoVaporParcial = (self.umidade/100)*self.calculoPressaoVaporSaturacao()
        return pressaoVaporParcial
    
    def razaoMistura (self):
        pv = self.calculoPressaoVaporParcial()
        pressoes = pv/(self.pressao-pv)
        return 0.622*pressoes