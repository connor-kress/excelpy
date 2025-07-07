from math import log as ln, exp
from currency import Currency
from percent import Percent
from util import number


def mulp(i: number | Percent, j: number | Percent) -> Percent:
    i = Percent(i)
    j = Percent(j)
    return (1+i).mul(1+j) - 1


def divp(i: number | Percent, j: number | Percent) -> Percent:
    i = Percent(i)
    j = Percent(j)
    return Percent((1+i).div(1+j) - 1)


def PV(
    i: number | Percent,
    nper: number,
    fv: number | Currency,
) -> Currency:
    fv = Currency(fv)
    i = Percent(i)
    return fv / (1+i)**nper

    
def FV(
    i: number | Percent,
    nper: number,
    pv: number | Currency,
) -> Currency:
    i = Percent(i)
    pv = Currency(pv)
    return pv * (1+i)**nper


def NPER(
    i: number | Percent,
    pv: number | Currency,
    fv: number | Currency,
) -> float:
    i = Percent(i)
    pv = Currency(pv)
    fv = Currency(fv)
    return ln(fv.div(pv)) / ln((1+i).value)


def RATE(
    nper: number,
    pv: number | Currency,
    fv: number | Currency,
) -> float:
    pv = Currency(pv)
    fv = Currency(fv)
    return exp(ln(fv.div(pv)) / nper) - 1
