"""Quadratic-surd continued-fraction builders."""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from typing import Any

from .common import is_perfect_square


def _convergents(terms: list[int]) -> list[dict[str, Any]]:
    p_minus_2, p_minus_1 = 0, 1
    q_minus_2, q_minus_1 = 1, 0
    convergents: list[dict[str, Any]] = []
    for index, term in enumerate(terms, start=1):
        p_value = term * p_minus_1 + p_minus_2
        q_value = term * q_minus_1 + q_minus_2
        value = Fraction(p_value, q_value)
        convergents.append(
            {
                "index": index,
                "term": term,
                "numerator": p_value,
                "denominator": q_value,
                "decimal": round(float(value), 8),
            }
        )
        p_minus_2, p_minus_1 = p_minus_1, p_value
        q_minus_2, q_minus_1 = q_minus_1, q_value
    return convergents


def build_quadratic_surd_model(n: int, terms: int) -> dict[str, Any]:
    """Build a periodic continued-fraction payload for sqrt(n)."""

    if n <= 0:
        raise ValueError("Use a positive integer n.")
    if is_perfect_square(n):
        raise ValueError("Use a non-square integer so the continued fraction is periodic.")
    a0 = isqrt(n)
    m = 0
    d = 1
    a = a0
    period: list[int] = []
    states: list[dict[str, int]] = []
    seen: set[tuple[int, int, int]] = set()
    while True:
        m = d * a - m
        d = (n - m * m) // d
        a = (a0 + m) // d
        state = (m, d, a)
        if state in seen:
            break
        seen.add(state)
        states.append({"m": m, "d": d, "a": a})
        period.append(a)
    repeated_terms = [a0]
    for index in range(max(1, terms - 1)):
        repeated_terms.append(period[index % len(period)])
    convergents = _convergents(repeated_terms)
    pell_hint = None
    for convergent in convergents:
        x_value = convergent["numerator"]
        y_value = convergent["denominator"]
        if x_value * x_value - n * y_value * y_value == 1:
            pell_hint = {"x": x_value, "y": y_value}
            break
    return {
        "n": n,
        "a0": a0,
        "period": period,
        "period_length": len(period),
        "states": states,
        "terms": repeated_terms,
        "notation": f"[{a0}; ({', '.join(str(item) for item in period)})]",
        "convergents": convergents,
        "pell_hint": pell_hint,
    }
