from psicometria import psicometria
from calculoSecagem import calculoSecagem
from salvarJson import salvarInfos
def calculoInversao (umidadeInicial):
    return umidadeInicial - ((umidadeInicial-11.5)*0.45)

def main ():
    ur = 70
    temp = 25
    pa = 101.325
    p = psicometria(temp,ur,pa)
    umidade0 = 32
    umidade1 = calculoInversao(umidade0)
    massaEspecifica = 245
    vazao = 33333
    area = 30
    tempSec = 36
    w = p.razaoMistura()
    tempo = 0.2
    vespeci = 0.96
    tempM = 28
    h = 0.1
    alturaDeCamada = 3
    tempoAcumulado = 0 
    camadas = int(alturaDeCamada/h)
  #  print(camadas)
    s=salvarInfos()

    for ciclo in range(2):
        if ciclo == 1:
            w = p.razaoMistura()
            tempSec = 40
            umidade0 = calculoInversao(umidade0)
            umidade1 = 11.5

        for x in range(camadas):
            cs = calculoSecagem(umidade0,massaEspecifica,vazao,area,tempo,w,tempSec,tempM,pa,umidade1,vespeci,h)
            cs.calculoRazaoMassas()
            # print(f"informações camada {x}\n")
            # print(f" tempo {cs.tempoEqui}\n")
            # print(f"a umidade {cs.umidadeSaida}\n")
            # print(f"razão de mistura {cs.wf}\n")
            tempoAcumulado += cs.tempoEqui
            s.criarDicionario(x,cs.tf,cs.umidadeSaida,cs.tempoEqui,tempoAcumulado)
            w = cs.wf
            tempSec = cs.tf
            cs = None

    s.gerarJson()
    s = None
if __name__ == "__main__":
    main()