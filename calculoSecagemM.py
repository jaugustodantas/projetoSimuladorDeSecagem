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
        p3 = (1+(self.umidadeInicialConvertida/100))
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
        
    def calculoPressaoVaporSaturadoEmTe(self):
        #calculo da pressão de vapor saturado da temperatura de equilibrio
        #eq 27
        teC = self.te + 273.16
        p1 = 5.169*(math.log(teC))
        p2 = 6834/teC
        p3 = 51.594 -p2-p1
        return 51.715*math.exp(p3)
    
    def calculoUmidadeRelativaEmTe(self):
        #calculo de umidade relativa do ar em temperatura de equilibrio
        #eq 26
        #Pressão em hhmg
        c = conversor(self.atm)
        atmMmhg = c.conversorPressaoPaemMmhg()
        c = None
        c = conversor(self.pvsTe)
        pvsTeMmhg = c.conversorPressaoPaemMmhg()
        c = None
        w0 = self.w
        p1 = 0.622+w0
        p2 = p1 * pvsTeMmhg
        p3 = atmMmhg *w0
        return (p3/p2) * 100
    
    def teorUmidadeEquilibrio (self):
        #calculo da umidade de ponto de equilibrio 
        #eq 28
        p1 = self.te+45.6
        p2 = 1-(self.urTe*0.01)
        p3 = math.log(p2)
        p4 = (-p3)/p1
        p5 = 1.206*math.sqrt(p4)
        return p5
    
