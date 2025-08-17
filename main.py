#pressao atmosferica santa helena 101.325 Kpa
from psicometria import psicometria
from calculoSecagem import calculoSecagem
def main ():
    ur = 70
    temp = 25
    pa = 101.325
    p = psicometria(temp,ur,pa)
    #print(p.razaoMistura())
    umidade0 = 20
    umidade1 = 16.67
    massaEspecifica = 750
    vazao = 300
    area = 30
    tempSec = 60
    w = 0.01
    tempo = 0.2
    vespeci = 0.96
    tempM = 40
    h = 0.05
    cs = calculoSecagem(umidade0,massaEspecifica,vazao,area,tempo,w,tempSec,tempM,pa,umidade1,vespeci,h)
    wf = cs.calculoRazaoMisturaAr()
    tempSec = cs.calculoTemperaturaFinais()
    cs.to = tempSec
    cs.w = wf
    p1 = cs.calculoUmidadeRelativaSaida()
    print(p1)

if __name__ == "__main__":
    main()