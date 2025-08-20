import math
from conversores import conversor
class calculoSecagem:
    def __init__(self,umidadeInicial,massaEspecifica,vazaoAr,areaCamara,intervaloTempo,razaoMistura,
                 temperaturaSecagem, temperaturaInicialMassa,pressaoAtmosferica,umidadeAtual,volumeEspecificoAr,altura):
        self.umidadeInicial = umidadeInicial #umidade bu
        self.P = massaEspecifica
        self.atm = pressaoAtmosferica
        self.vazao = vazaoAr
        self.umidadeAtual = umidadeAtual  #umidade bu
        self.areaCamara= areaCamara
        self.w = razaoMistura
        self.deltaT = intervaloTempo
        self.ve= volumeEspecificoAr
        self.to = temperaturaSecagem
        self.tgo = temperaturaInicialMassa
        self.h = altura
        self.umidadeInicialConvertida = 0
        self.umidadeAtualConvertida = 0
        self.r = self.calculoRazaoMassas()
        self.cp = self.calculoEntalpiaEspecifica()
        self.te = self.calculoTemperaturaEquilibrio()
        self.pvsTe = self.calculoPressaoVaporSaturadoEmTe()
        self.urTe = self.calculoUmidadeRelativaEmTe()
        self.ue = self.teorUmidadeEquilibrio()
        self.ruo = self.calculoRazaoUmidadeAtual()
        self.varA = self.calculoVariavelA()
        self.varB = self.calculoVariavelB()
        self.tempoEqui = self.tempoEquivalente()
        self.ruf = self.novaRazaoUmidadeAposTempoT()
        self.uf = self.umidadeNoTempoCorrigido()
        self.wf = self.correcaoRazaoMistura()
        self.deltaL = self.calculoDeltaL()
        self.tf = self.CalculoTemperaturaFinal()
        self.tef = self.calculoPressaoVaporSaturadoEmTe(self.tf)
        self.umidadeSaida = self.calculoUmidadeRelativaEmTe(self.tef)
    def calculoRazaoMassas (self):
        #calculo da razão entre as massas ar seco x ar seco 
        #Segue a Eq 24 do livro do Juareaz
        #u0 = teor de umidade inicial (bs), deltaX altura camada fina, ve = volume específico do ar
        # P = massa específica do grão no início da secagem, deltaT = intervalo de tempo, a = área do plenum
        # q = vazão 
        c = conversor(self.umidadeInicial)
        self.umidadeInicialConvertida = c.conversorUmidadeBuxBs()
        c = None
        p1 = self.P * self.ve*self.areaCamara*self.h
        p2 = self.vazao*self.deltaT*60
        p3 = (1+(self.umidadeInicialConvertida))
        p4 = p3*p2
        return p1/p4
    
    def calculoEntalpiaEspecifica (self):
        #entalpia específico do milho de acordo com a umidade
        # U = umidade atual em base seca
        c = conversor(self.umidadeAtual)
        self.umidadeAtualConvertida = c.conversorUmidadeBuxBs()
        c = None
        u = self.umidadeAtualConvertida
        p1 = 1 + u
        p2 = 0.851* u
        p3 = 0.35 +(p2/p1)
        return p3

    def calculoTemperaturaEquilibrio(self):
        #calculo da temperatura de equiblibro do material 
        #eq 25
        # w = razao mistura do ar de entrada
        #cp e r calculados a cima
        # U = umidade atual em bs 
        p1 = self.cp *self.r*(1+self.umidadeAtualConvertida)
        p2 = 0.24+(0.45 *self.w)
        p3 = p1 +p2
        p4 = p1 * self.tgo
        p5 = self.to*p2
        return (p4+p5)/p3
        
    def calculoPressaoVaporSaturadoEmTe(self,temp=None):
        #calculo da pressão de vapor saturado da temperatura de equilibrio
        #eq 27
        if temp == None:
            te = self.te
        else:
            te = temp

        teC = te + 273.16
        p1 = 5.169*(math.log(teC))
        p2 = 6834/teC
        p3 = 51.594 -p2-p1
        return 51.715*math.exp(p3)
    
    def calculoUmidadeRelativaEmTe(self,pvs=None):
        #calculo de umidade relativa do ar em temperatura de equilibrio
        #eq 26
        #Pressão em hhmg
        c = conversor(self.atm)
        atmMmhg = c.conversorPressaoPaemMmhg()
        c = None
       #c = conversor(self.pvsTe)
       #pvsTeMmhg = c.conversorPressaoPaemMmhg()
        c = None
        if pvs == None:
            w0 = self.w
            pv = self.pvsTe
        else:
            w0 = self.wf
            pv = self.tef

        p1 = 0.622+w0
        p2 = p1 * pv
        p3 = atmMmhg *w0*100
        return (p3/p2)
    
    def teorUmidadeEquilibrio (self):
        #calculo da umidade de ponto de equilibrio higrospopico
        #eq 28
        p1 = self.te+45.6
        p2 = 1-(self.urTe*0.01)
        p3 = math.log(p2)
        p4 = (-p3)/p1
        p5 = 1.206*math.sqrt(p4)
        return p5
    
    def calculoRazaoUmidadeAtual (self):
        #calculo da raão de umidade entre a umidade atual e o ponto de equilibrio
        #eq 30
        p1 = self.umidadeAtualConvertida - self.ue
        p2 = self.umidadeInicialConvertida - self.ue
        return p1/p2
    
    def calculoVariavelA(self):
        #calculo da váriavel A usada no calculo de tempo equivalente
        #eq 31
        return -1.706 + (0.0088*(self.te))
    
    def calculoVariavelB(self):
        #calculo da váriavel B usada no calculo de tempo equivalente
        #eq 32
        p1 = -0.059 * self.te
        return 148.7 * math.exp(p1)
    
    def tempoEquivalente (self):
        #calculo do tempo equivalente, ou seja, quanto tempo o material deve ficar exposto 
        #ao ar nas condições Te e W0 para que seja alcançado a umidade desejada
        #eq 29
        p1 = math.log(self.ruo)
        p2 = math.pow(p1,2) * self.varB
        p3 = self.varA * p1
        return p2+p3

    def novaRazaoUmidadeAposTempoT(self):
        #eq 33
        p1 = self.deltaT + self.tempoEqui
        p2 = math.pow(self.varA,2)+(4*self.varB*(p1))
        p3 = math.sqrt(p2)
        p4 = (-self.varA -p3)/(2*self.varB)
        return math.exp(p4)
    
    def umidadeNoTempoCorrigido(self):
        #eq 34
        #
        p1 = self.umidadeInicialConvertida - self.ue
        p2 = self.ruf * p1
        return p2 + self.ue 

    def correcaoRazaoMistura(self):
        #eq 35
        p1 = self.r*(self.umidadeAtualConvertida - self.uf)
        return self.w + p1

    def calculoDeltaL(self):
        #eq 36
        p1 = 4.35*(math.exp(-28.25 * self.umidadeAtualConvertida))
        p2 = 606-(0.57*self.te)
        return p1*p2
    
    def CalculoTemperaturaFinal(self):
        #eq 39
        p0 = self.te
        p1 = self.cp*self.r*(1+self.umidadeAtualConvertida)
        p2 = 0.24 + (0.45*self.wf) + p1   #denominador
        p3 = (0.24+(0.45*self.w))*p0
        p4 = (self.wf-self.w)
        p5 = (588+self.deltaL-p0)
        p6 = p1*p0
        p7 = p4*p5
        p8 = p3-p7+p6
        return p8/p2