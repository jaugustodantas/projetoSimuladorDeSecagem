#pressao atmosferica santa helena 101.325 Kpa
from psicometria import psicometria
def main ():
    ur = 70
    temp = 25
    pa = 101.325
    p = psicometria(temp,ur,pa)
    print(p.razaoMistura())

if __name__ == "__main__":
    main()