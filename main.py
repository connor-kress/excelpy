from math import log as ln, exp


def pper(i: float) -> None:
    print(f"{i*100:.2f}%")


def mul_i(i: float, j: float) -> float:
    return (i+1)*(j+1) - 1


def div_i(i: float, j: float) -> float:
    return (i+1)/(j+1) - 1


def PV(i: float, nper: float, fv: float) -> float:
    return fv / (1+i)**nper

    
def FV(i: float, nper: float, pv: float) -> float:
    return pv * (1+i)**nper


def NPER(i: float, pv: float, fv: float) -> float:
    return ln(fv/pv) / ln(1+i)


def RATE(nper: float, pv: float, fv: float) -> float:
    return exp(ln(fv/pv) / nper) - 1
