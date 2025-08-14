import math
class calculoSecagem:
    def __init__(self,umidadeInicial,massaEspecifica,vazaoAr,areaCamara,intervaloTempo,razaoMistura,
                 temperaturaSecagem, temperaturaInicialMassa,pressaoAtmosferica,umidadeAtual):
        self.umidadeInicial = umidadeInicial
        self.P = massaEspecifica
        self.atm = pressaoAtmosferica
        self.vazao = vazaoAr
        self.umidadeAtual = umidadeAtual
        self.areaCamara=areaCamara
        self.w = razaoMistura
        self.deltaT = intervaloTempo
        self.ve=10
        self.to = temperaturaSecagem
        self.tgo = temperaturaInicialMassa
        #self.P = massaEspecifica
    def balancoMasas (self):
        #calculo do balanço de massas 
        #explicar variáveis
        r = (self.P*self.ve* self.areaCamara*0.1)/(self.vazao*self.deltaT*60*(1-self.conversaoUmidadeBaseSeca()))
        return r
    def conversaoUmidadeBaseSeca(self):
        #converte a umidade de base umida para base seca
        baseSeca = (self.umidadeInicial/(100-self.umidadeInicial))/100
        return baseSeca

    def calorEspecificoDoMilho (self):
        #calor especifico do milho
        return (0.35 +(0.851*self.conversaoUmidadeBaseSeca()/(1+self.conversaoUmidadeBaseSeca())))

    def temperaturaDeEquilibrio(self):
        #parei na construção dessa função
        #razão de mistura tem que ser implementada (ela muda a cada interação com o ar)
        cp = self.calorEspecificoDoMilho()
        r = self.balancoMasas()
        u=self.conversaoUmidadeBaseSeca
        te = ((0.24+0.45*(self.w))*self.to+cp*r(1+u)*self.tgo)/(0.24+0.45*self.w+cp*r*(1+u))
        return te
    
    def calculoPressaoVaporSaturacao (self):
        temp = self.temperaturaDeEquilibrio()
        pvs = 51.715 * math.exp((51.594 - 6834/(temp+273.16))-(5.169*(math.log(temp+273.16))))
        return pvs
    
    def conversorPressao(self,pressao):
        pc = pressao * 7.5
        return pc
    
    def calculoUmidadeRelativa(self):
        wc = self.conversorPressao(self.w)
        atmc = self.conversorPressao(self.atm)
        ur = 100*((atmc*wc)/((0.622+self.w)+self.calculoPressaoVaporSaturacao()))
        return ur
    
    def calculoUmidadeEquilibrio (self):
        u = self.calculoUmidadeRelativa()
        te =self.temperaturaDeEquilibrio()
        ue = 1.206*math.sqrt((-1*math.log((1-0.01*(u))/(te+45.6))))
        return ue
    
    def calcucloRazaoUmidadeInicial(self):
        u = self.conversaoUmidadeBaseSeca(self.umidadeAtual)
        u0 = self.conversaoUmidadeBaseSeca(self.umidadeInicial)
        ue = self.calculoUmidadeEquilibrio()
        ru0 = (u-ue)/(u0-ue)
        return ru0
    
    def calculoVariavelA(self):
        a = -1.706+0.0088*self.temperaturaDeEquilibrio()
        return a
    
    def calculoVariavelB(self):
        b = 148.7*math.exp(-0.059*self.temperaturaDeEquilibrio())
        return b
    
    def calculoTempoEquivalente(self):
        a = self.calculoVariavelA(self)
        b = self.calculoVariavelB(self)
        ru0 = self.calcucloRazaoUmidadeInicial(self)
        p1 = a*math.log(ru0)
        p2 = b*math.pow(math.log(ru0),2)
        return p1+p2
    
    