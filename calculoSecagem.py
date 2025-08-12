class calculoSecagem:
    def __init__(self,umidadeInicial,massaEspecifica,vazaoAr,areaCamara,intervaloTempo,razaoMistura,temperaturaSecagem):
        self.umidadeInicial = umidadeInicial
        self.P = massaEspecifica
        self.vazao = vazaoAr
        self.areaCamara=areaCamara
        self.w = razaoMistura
        self.deltaT = intervaloTempo
        self.ve=10
        self.to = temperaturaSecagem
        #self.P = massaEspecifica
    def balancoMasas (self):
        r = (self.P*self.ve* self.areaCamara*0.1)/(self.vazao*self.deltaT*60*(1-self.conversaoUmidadeBaseSeca()))
        return r
    def conversaoUmidadeBaseSeca(self):
        baseSeca = (self.umidadeInicial/(100-self.umidadeInicial))/100
        return baseSeca

    def calorEspecificoDoMilho (self):
        return (0.35 +(0.851*self.conversaoUmidadeBaseSeca()/(1+self.conversaoUmidadeBaseSeca())))

    def temperaturaDeEquilibrio(self):
        #parei na construção dessa função
        #razão de mistura tem que ser implementada (ela muda a cada interação com o ar)
        cp = self.calorEspecificoDoMilho()
        r = self.balancoMasas()
        u=self.conversaoUmidadeBaseSeca
        te = ((0.24+0.45*(self.w))*self.to+cp*r(1+u)*tgo)/(0.24+0.45*self.w+cp*r*(1+u))
    