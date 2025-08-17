import math
class calculoSecagem:
    def __init__(self,umidadeInicial,massaEspecifica,vazaoAr,areaCamara,intervaloTempo,razaoMistura,
                 temperaturaSecagem, temperaturaInicialMassa,pressaoAtmosferica,umidadeAtual,volumeEspecificoAr,altura):
        self.umidadeInicial = float(umidadeInicial)
        self.P = float(massaEspecifica)
        self.atm = float(pressaoAtmosferica)
        self.vazao = float(vazaoAr)
        self.umidadeAtual = float(umidadeAtual)
        self.areaCamara=float(areaCamara)
        self.w = float(razaoMistura)
        self.deltaT = float(intervaloTempo)
        self.ve= float(volumeEspecificoAr)
        self.to = float(temperaturaSecagem)
        self.tgo = float(temperaturaInicialMassa)
        self.h = float(altura)
        #self.P = massaEspecifica
    def balancoMassas (self):
        #calculo do balanço de massas 
        #explicar variáveis
        p1 = self.P*self.ve* self.areaCamara*self.h
        p2 = 1+self.conversaoUmidadeBaseSeca(self.umidadeInicial)
        p3 = self.vazao*self.deltaT*60
        p4 = p3 * p2
        r = p1/p4
     #   r = (self.P*self.ve* self.areaCamara*self.h)/(self.vazao*self.deltaT*60*(1-self.conversaoUmidadeBaseSeca(self.umidadeInicial)))
        return float(r)
    def conversaoUmidadeBaseSeca(self,umidade):
        #converte a umidade de base umida para base seca
        u=umidade
        baseSeca = (u/(100-u))
        return baseSeca

    def calorEspecificoDoMilho (self):
        #calor especifico do milho
        return (0.35 +(0.851*self.conversaoUmidadeBaseSeca(self.umidadeAtual)/(1+self.conversaoUmidadeBaseSeca(self.umidadeAtual))))

    def temperaturaDeEquilibrio(self):
        #eq 25
        #parei na construção dessa função
        #razão de mistura tem que ser implementada (ela muda a cada interação com o ar)
        cp = self.calorEspecificoDoMilho()
        r = float(self.balancoMassas())
        u=self.conversaoUmidadeBaseSeca(self.umidadeAtual)
        te = ((0.24+0.45*(self.w))*self.to+cp*r*(1+u)*self.tgo)/(0.24+0.45*self.w+cp*r*(1+u))
        return te
    
    def calculoPressaoVaporSaturacao (self):
        #eq 27
        temp = self.temperaturaDeEquilibrio()
        pvs = 51.715 * math.exp((51.594 - 6834/(temp+273.16))-(5.169*(math.log(temp+273.16))))
        return pvs
    
    def conversorPressao(self,pressao):
        pc = pressao * 7.5
        return pc
    
    def calculoUmidadeRelativa(self):
        #eq 26
        tst = self.calculoPressaoVaporSaturacao()
        wc = self.w
        atmc = self.conversorPressao(self.atm)
        ur = 100*((atmc*wc)/((0.622+self.w)*tst))
        return ur
    
    def calculoUmidadeEquilibrio (self):
        #eq 28
        u = self.calculoUmidadeRelativa()
        te =self.temperaturaDeEquilibrio()
        p1 = 1 - 0.01*u
        p2 = te+45.6
        p3 = -math.log(p1)
        p4 = p3/p2
        p5 = math.sqrt(p4)
        ue = 1.206 * p5
        #ue = 1.206*math.sqrt((-1*math.log((1-0.01*(u))/(te+45.6))))
        return ue
    
    def calcucloRazaoUmidadeAtual(self):
        #eq 30
        u = self.conversaoUmidadeBaseSeca(self.umidadeAtual)
        u0 = self.conversaoUmidadeBaseSeca(self.umidadeInicial)
        ue = self.calculoUmidadeEquilibrio()
        ru0 = (u-ue)/(u0-ue)
        return ru0
    
    def calculoVariavelA(self):
        #eq 31
        a = -1.706+0.0088*self.temperaturaDeEquilibrio()
        return a
    
    def calculoVariavelB(self):
        #eq 32
        b = 148.7*math.exp(-0.059*self.temperaturaDeEquilibrio())
        return b
    
    def calculoTempoEquivalente(self):
        #eq 29
        a = self.calculoVariavelA()
        b = self.calculoVariavelB()
        ru0 = self.calcucloRazaoUmidadeAtual()
        p1 = a*math.log(ru0)
        p2 = b*math.pow(math.log(ru0),2)
        return p1+p2
    
    def razaoUmidadePorTempo(self):
        #eq 33
        a = self.calculoVariavelA()
        b = self.calculoVariavelB()
        t = self.deltaT
        te = self.calculoTempoEquivalente()
        var1 = t + te
        var2 =math.sqrt(math.pow(a,2)+4*(b*var1))
        var3 = ((-1*a)-var2)/(2*b)
        rUf = math.exp(var3)
        return rUf

    def calculoUmidadeAposIncremeto(self):
        # eq34
        ruf= self.razaoUmidadePorTempo()
        ue = self.calculoUmidadeEquilibrio()
        u0 = self.conversaoUmidadeBaseSeca(self.umidadeInicial)
        uf= ruf*(u0-ue)+ue
        return uf
    
    def calculoRazaoMisturaAr(self):
        #eq 35
        #wf = wo +R(U-Uf)
        r = self.balancoMassas()
        uf = self.calculoUmidadeAposIncremeto()
        wf = self.w + r*((self.umidadeInicial/100) - uf)
        return wf
    
    def calculoCalorLatenteExcedente(self):
        #eq 37
        #deltaL = (606 - 0.57*Te)*4.35*exp(-28.25* U)
        #necessário para o calculo das temperaturas finais
        u = self.conversaoUmidadeBaseSeca(self.umidadeAtual)
        te= self.temperaturaDeEquilibrio()
        deltaL = (606-0.57*te)*4.35*math.exp(-28.25*u)
        return deltaL

    def calculoTemperaturaFinais(self):
        #eq 39, passo 12
        # Considerando que a temperatura do grão será igual a temperatuda do ar
        # parte1 = (0.24 + 0.45W0)*Te - (Wf - W0)*(588+deltaL - Te) + Cp*R(1+U)*Te
        # parte2 = 0.24+0.45*wf+cp*r*(1+u)
        deltaL = self.calculoCalorLatenteExcedente()
        u = self.conversaoUmidadeBaseSeca(self.umidadeAtual)
        wf = self.calculoRazaoMisturaAr()
        cp = self.calorEspecificoDoMilho()
        r = self.balancoMassas()
        te = self.temperaturaDeEquilibrio()
        w0 = self.w
        p1 = (0.24+(0.45*w0)) * te - (wf-w0)*(588+deltaL - te) + cp*r*(1+u)*te
        p2 = 0.24+0.45*wf+cp*r*(1+u)
        tf = p1/p2
        return tf
    

    def calculoPressaoVaporSaturacaoFinal (self):
        #eq 27
        #Essa é uma adaptação para poder calcular a ur que sai da massa
        temp = self.to
        pvs = 51.715 * math.exp((51.594 - 6834/(temp+273.16))-(5.169*(math.log(temp+273.16))))
        return pvs
    
    def calculoUmidadeRelativaSaida(self):
        #eq 26
        #Essa é uma adaptação para poder calcular a ur que sai da massa
        tst = self.calculoPressaoVaporSaturacaoFinal()
        wc = self.w
        atmc = self.conversorPressao(self.atm)
        ur = 100*((atmc*wc)/((0.622+self.w)*tst))
        return ur