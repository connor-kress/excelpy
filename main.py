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
    rate: number | Percent,
    nper: number,
    pmt: number | Currency = 0,
    fv: number | Currency = 0,
) -> Currency:
    rate = Percent(rate)
    pmt = Currency(pmt)
    fv = Currency(fv)
    total_fv = fv + pmt * ((1+rate)**nper - 1)/rate
    return -total_fv / (1+rate)**nper

    
def FV(
    rate: number | Percent,
    nper: number,
    pmt: number | Currency = 0,
    pv: number | Currency = 0,
) -> Currency:
    rate = Percent(rate)
    pmt = Currency(pmt)
    pv = Currency(pv)
    pmt_part = pmt * ((1+rate)**nper - 1)/rate
    pv_part = pv * (1+rate)**nper
    return -pmt_part - pv_part


# TODO: add PMT
def NPER(
    rate: number | Percent,
    pv: number | Currency,
    fv: number | Currency,
) -> float:
    rate = Percent(rate)
    pv = Currency(pv)
    fv = Currency(fv)
    if rate.value == 0:
        if pv.value == fv.value:
            return 0
        raise ValueError("rate must be non-zero")
    return ln(fv.div(pv)) / ln((1+rate).value)


def PMT(
    rate: number | Percent,
    nper: number,
    pv: number | Currency = 0,
    fv: number | Currency = 0,
) -> Currency:
    rate = Percent(rate)
    fv = Currency(fv)
    pv = Currency(pv)
    if (pv + fv).value == 0:
        return Currency(0)
    if nper <= 0:
        raise ValueError("nper must be greater than 0")
    if rate.value == 0:
        return -(pv + fv) / nper
    total_fv = fv + pv * (1+rate)**nper
    return -total_fv * rate/((1+rate)**nper - 1)


# TODO: add PMT
def RATE(
    nper: number,
    pv: number | Currency,
    fv: number | Currency,
) -> float:
    pv = Currency(pv)
    fv = Currency(fv)
    return exp(ln(fv.div(pv)) / nper) - 1
