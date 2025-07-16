from math import log as ln, exp
from typing import Iterable
from currency import Currency
from percent import Percent
from util import get_value, number
from span import Span, Value
from table import Table


def NPV(
    rate: number | Percent,
    values: Span | Iterable[Value],
    legacy: bool = False,
) -> Currency:
    offset = 1 if legacy else 0
    return -Currency(sum((
        PV(rate, i+offset, fv=value)
        for i, value in enumerate(Span(values).iter_currency())
    )))


def mulp(i__: number | Percent, j__: number | Percent) -> Percent:
    i = get_value(i__)
    j = get_value(j__)
    return Percent((1+i)*(1+j) - 1)


def divp(i__: number | Percent, j__: number | Percent) -> Percent:
    i = get_value(i__)
    j = get_value(j__)
    return Percent((1+i)/(1+j) - 1)


def PV(
    rate: number | Percent,
    nper: number,
    pmt: number | Currency = 0,
    fv: number | Currency = 0,
) -> Currency:
    i = get_value(rate)
    pmt = get_value(pmt)
    fv = get_value(fv)
    total_fv = fv + pmt * ((1+i)**nper - 1)/i
    pv = -total_fv / (1+i)**nper
    return Currency(pv)

    
def FV(
    rate: number | Percent,
    nper: number,
    pmt: number | Currency = 0,
    pv: number | Currency = 0,
) -> Currency:
    i = get_value(rate)
    pmt = get_value(pmt)
    pv = get_value(pv)
    pmt_part = pmt * ((1+i)**nper - 1)/i
    pv_part = pv * (1+i)**nper
    fv = -(pmt_part + pv_part)
    return Currency(fv)


def NPER(
    rate: number | Percent,
    pmt: number | Currency,
    pv: number | Currency = 0,
    fv: number | Currency = 0,
) -> float:
    i = get_value(rate)
    pmt = get_value(pmt)
    pv = get_value(pv)
    fv = get_value(fv)
    if i == 0:
        if pmt == 0:
            raise ValueError("rate and pmt cannot both be zero")
        return -(pv + fv) / pmt
    # (1+i)^n = (pmt - fv*i) / (pmt + pv*i)
    # n = ln((pmt - fv*i)/(pmt + pv*i)) / ln(1+i)
    num = pmt - fv * i
    den = pmt + pv * i
    if num / den <= 0 or 1 + i <= 0:
        raise ValueError("Invalid input: log argument must be positive")
    return ln(num / den) / ln(1 + i)


def PMT(
    rate: number | Percent,
    nper: number,
    pv: number | Currency = 0,
    fv: number | Currency = 0,
) -> Currency:
    i = get_value(rate)
    fv = get_value(fv)
    pv = get_value(pv)
    if pv + fv == 0:
        return Currency(0)
    if nper <= 0:
        raise ValueError("nper must be greater than 0")
    if i == 0:
        return Currency(-(pv + fv) / nper)
    total_fv = fv + pv * (1+i)**nper
    pmt = -total_fv * i/((1+i)**nper - 1)
    return Currency(pmt)


def RATE(
    nper: number,
    pmt: number | Currency = 0,
    pv: number | Currency = 0,
    fv: number | Currency = 0,
    guess: number | Percent = 0.1,
    tol: float = 1e-6,
    maxiter: int = 100,
) -> Percent:
    """ Solve for interest rate i per period that satisfies
        PV*(1+i)^nper + pmt*((1+i)^nper - 1)/i + FV = 0

    Payments are assumed at period's end.
    """
    n = nper
    if n <= 0:
        raise ValueError("nper must be greater than 0")
    pmt = get_value(pmt)
    pv = get_value(pv)
    fv = get_value(fv)
    i = get_value(guess)

    # no payment -> (1+i)^n = -fv/pv
    if abs(pmt) < tol:
        if abs(pv) < tol:
            raise ValueError("pmt and pv cannot both be zero")
        ratio = -fv / pv
        if ratio <= 0:
            raise ValueError("Invalid inputs: -fv/pv must be > 0")
        return Percent(exp(ln(ratio) / nper) - 1)

    # avoid zero‐divide in the iteration
    if abs(i) < tol:
        i = tol

    # Newton-Raphson iteration
    for _ in range(maxiter):
        v1 = (1 + i) ** n
        # f(i)
        f = pv * v1 + pmt * (v1 - 1) / i + fv
        # f'(i) = pv*n*(1+i)^(n-1) + p*[i*n*(1+i)^(n-1) - (v1-1)]/i^2
        df = pv * n * (1 + i) ** (n - 1) \
           + pmt * (n * (1 + i) ** (n - 1) * i - (v1 - 1)) / (i ** 2)
        old_i = i
        i -= f / df
        if abs(i - old_i) < tol:
            return Percent(i)

    raise ValueError("Rate calculation did not converge")
