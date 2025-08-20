class conversor:
    def __init__(self,atributo):
        self.a = atributo


    def conversorUmidadeBuxBs(self):
        return self.a/(100-self.a)
    
    def conversorPressaoPaemMmhg (self):
        return self.a * 7.50062