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
   #umidade1 = 16.67
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
    incremento = 1 /h
    cs = calculoSecagem(umidade0,massaEspecifica,vazao,area,tempo,w,tempSec,tempM,pa,umidade1,vespeci,h)
    for x in range(int(incremento)):
        wf = cs.calculoRazaoMisturaAr()
        tempSec = cs.calculoTemperaturaFinais()
        umidade3 = cs.calculoUmidadeAposIncremeto()
        cs.to = tempSec
        cs.w = wf
        p1 = cs.calculoUmidadeRelativaSaida()
        print(f"A umidade da massa na altura {h:.2f} é de {(umidade3 * 100):.2f} e a temperatura ficou em {tempSec:.2f} e a umidade relativa de saida foi {p1:.2f}")
        h=h+0.05
        #cs.h=h


if __name__ == "__main__":
    main()