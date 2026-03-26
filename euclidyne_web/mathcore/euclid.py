"""Euclidean-algorithm builders and related helpers."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from .common import (
    continued_fraction_notation,
    fraction_payload,
    to_payload,
)


STEP_COLORS = [
    "#0f7b6d",
    "#c0822b",
    "#22577a",
    "#8f4f4f",
    "#5e548e",
    "#2d6a4f",
    "#a44a3f",
    "#4c6e91",
]


@dataclass(frozen=True)
class EuclidStep:
    """One standard Euclidean division step."""

    index: int
    dividend: int
    divisor: int
    quotient: int
    remainder: int
    color: str


@dataclass(frozen=True)
class ExtendedRow:
    """One row of the Extended Euclid recurrence table."""

    index: int
    quotient: int | None
    remainder: int
    s: int
    t: int
    remainder_expression: str | None
    s_expression: str | None
    t_expression: str | None
    identity: str
    color: str
    is_gcd_row: bool
    is_stop_row: bool


@dataclass(frozen=True)
class Convergent:
    """A finite continued-fraction convergent."""

    index: int
    quotient: int
    numerator: int
    denominator: int
    decimal: float
    error_decimal: float


@dataclass(frozen=True)
class CenteredStep:
    """One least-absolute-remainder Euclid step."""

    index: int
    dividend: int
    divisor: int
    quotient: int
    remainder: int
    next_divisor: int
    color: str


def _color(index: int) -> str:
    return STEP_COLORS[index % len(STEP_COLORS)]


def build_division_steps(a: int, b: int) -> list[EuclidStep]:
    """Return standard Euclidean division steps for a >= b > 0."""

    if a <= 0 or b <= 0:
        raise ValueError("Use positive integers.")
    if a < b:
        raise ValueError("Use a >= b > 0 for the visual model.")

    steps: list[EuclidStep] = []
    dividend = a
    divisor = b
    index = 1
    while divisor != 0:
        quotient, remainder = divmod(dividend, divisor)
        steps.append(
            EuclidStep(
                index=index,
                dividend=dividend,
                divisor=divisor,
                quotient=quotient,
                remainder=remainder,
                color=_color(index - 1),
            )
        )
        dividend, divisor = divisor, remainder
        index += 1
    return steps


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return g, x, y such that a*x + b*y = g."""

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t


def build_extended_rows(a: int, b: int, steps: list[EuclidStep]) -> list[ExtendedRow]:
    """Build the Extended Euclid table corresponding to forward division steps."""

    quotients = [step.quotient for step in steps]
    remainders = [a, b]
    s_values = [1, 0]
    t_values = [0, 1]

    for step in steps:
        remainders.append(step.remainder)
        s_values.append(s_values[-2] - step.quotient * s_values[-1])
        t_values.append(t_values[-2] - step.quotient * t_values[-1])

    gcd_index = len(remainders) - 2
    stop_index = len(remainders) - 1
    rows: list[ExtendedRow] = []
    for index, remainder in enumerate(remainders):
        quotient = quotients[index - 2] if index >= 2 else None
        remainder_expression = None
        s_expression = None
        t_expression = None
        if index >= 2:
            remainder_expression = (
                f"{remainders[index - 2]} - {quotients[index - 2]} * {remainders[index - 1]}"
            )
            s_expression = f"{s_values[index - 2]} - {quotients[index - 2]} * {s_values[index - 1]}"
            t_expression = f"{t_values[index - 2]} - {quotients[index - 2]} * {t_values[index - 1]}"
        rows.append(
            ExtendedRow(
                index=index,
                quotient=quotient,
                remainder=remainder,
                s=s_values[index],
                t=t_values[index],
                remainder_expression=remainder_expression,
                s_expression=s_expression,
                t_expression=t_expression,
                identity=f"{a} * ({s_values[index]}) + {b} * ({t_values[index]}) = {remainder}",
                color=_color(index),
                is_gcd_row=index == gcd_index,
                is_stop_row=index == stop_index,
            )
        )
    return rows


def build_convergents(target: Fraction, quotients: list[int]) -> list[Convergent]:
    """Build convergents for a continued-fraction quotient list."""

    p_minus_2, p_minus_1 = 0, 1
    q_minus_2, q_minus_1 = 1, 0
    convergents: list[Convergent] = []
    for index, quotient in enumerate(quotients, start=1):
        p_value = quotient * p_minus_1 + p_minus_2
        q_value = quotient * q_minus_1 + q_minus_2
        value = Fraction(p_value, q_value)
        convergents.append(
            Convergent(
                index=index,
                quotient=quotient,
                numerator=p_value,
                denominator=q_value,
                decimal=round(float(value), 8),
                error_decimal=round(float(target - value), 8),
            )
        )
        p_minus_2, p_minus_1 = p_minus_1, p_value
        q_minus_2, q_minus_1 = q_minus_1, q_value
    return convergents


def build_phase_subpanel(dividend: int, divisor: int) -> dict[str, Any]:
    """Build the one-step full-turn plus residual-phase analogy payload."""

    ratio = Fraction(dividend, divisor)
    whole_turns = dividend // divisor
    remainder = dividend % divisor
    return {
        "dividend": dividend,
        "divisor": divisor,
        "ratio": fraction_payload(ratio),
        "whole_turns": whole_turns,
        "remainder": remainder,
        "summary": (
            f"One full driver turn yields {whole_turns} full follower turns "
            f"and a residual phase of {remainder}/{divisor}."
        ),
    }


def is_fibonacci_pair(a: int, b: int) -> bool:
    """Return whether a and b are consecutive Fibonacci numbers."""

    high, low = max(a, b), min(a, b)
    if low <= 0:
        return False
    sequence = [1, 1]
    while sequence[-1] < high:
        sequence.append(sequence[-1] + sequence[-2])
    return high in sequence and low in sequence and abs(sequence.index(high) - sequence.index(low)) == 1


def _is_fibonacci_like_quotients(quotients: list[int]) -> bool:
    if not quotients:
        return False
    if len(quotients) == 1:
        return quotients[0] == 1
    return all(value == 1 for value in quotients[:-1]) and quotients[-1] in {1, 2}


def build_euclid_model(a: int, b: int) -> dict[str, Any]:
    """Build the canonical Euclid payload for a >= b > 0."""

    steps = build_division_steps(a, b)
    quotients = [step.quotient for step in steps]
    extended_rows = build_extended_rows(a, b, steps)
    target = Fraction(a, b)
    convergents = build_convergents(target, quotients)
    gcd_value = steps[-1].divisor if steps[-1].remainder == 0 else steps[-1].remainder
    gcd_row = next(row for row in extended_rows if row.is_gcd_row)

    return {
        "input": {"a": a, "b": b, "ratio": fraction_payload(target)},
        "gcd": gcd_value,
        "step_count": len(steps),
        "steps": to_payload(steps),
        "rows": to_payload(extended_rows),
        "bezout": {
            "x": gcd_row.s,
            "y": gcd_row.t,
            "identity": gcd_row.identity,
            "inverse_mod_b": gcd_row.s % b if gcd_value == 1 else None,
        },
        "continued_fraction": {
            "quotients": quotients,
            "notation": continued_fraction_notation(quotients),
            "convergents": to_payload(convergents),
        },
        "phase": build_phase_subpanel(a, b),
        "sequences": {
            "remainders": [a, b] + [step.remainder for step in steps],
            "quotients": quotients,
        },
        "properties": {
            "coprime": gcd_value == 1,
            "fibonacci_pair": is_fibonacci_pair(a, b),
            "fibonacci_like_quotients": _is_fibonacci_like_quotients(quotients),
        },
    }


def build_centered_euclid_model(a: int, b: int) -> dict[str, Any]:
    """Build a side-by-side comparison between standard and centered Euclid."""

    standard = build_euclid_model(a, b)
    dividend = a
    divisor = b
    steps: list[CenteredStep] = []
    index = 1
    while divisor != 0:
        quotient = (dividend + divisor // 2) // divisor
        remainder = dividend - quotient * divisor
        next_divisor = abs(remainder)
        steps.append(
            CenteredStep(
                index=index,
                dividend=dividend,
                divisor=divisor,
                quotient=quotient,
                remainder=remainder,
                next_divisor=next_divisor,
                color=_color(index - 1),
            )
        )
        dividend, divisor = divisor, next_divisor
        index += 1

    return {
        "input": standard["input"],
        "gcd": standard["gcd"],
        "standard": {
            "step_count": standard["step_count"],
            "steps": standard["steps"],
            "quotients": standard["continued_fraction"]["quotients"],
        },
        "centered": {
            "step_count": len(steps),
            "steps": to_payload(steps),
        },
        "comparison": {
            "saved_steps": standard["step_count"] - len(steps),
            "winner": "centered" if len(steps) < standard["step_count"] else "tie_or_standard",
        },
    }


def build_fibonacci_comparison(a: int, b: int) -> dict[str, Any]:
    """Build a comparison between an input pair and a Fibonacci worst-case benchmark."""

    actual = build_euclid_model(a, b)
    fibs = [1, 1]
    while fibs[-1] <= max(a, b) * 2:
        fibs.append(fibs[-1] + fibs[-2])
    pair = (2, 1)
    for index in range(1, len(fibs)):
        if fibs[index - 1] <= b:
            pair = (fibs[index], fibs[index - 1])
        else:
            break
    benchmark = build_euclid_model(pair[0], pair[1])
    return {
        "actual": actual,
        "benchmark": benchmark,
        "comparison": {
            "actual_steps": actual["step_count"],
            "benchmark_steps": benchmark["step_count"],
            "actual_is_fibonacci_pair": actual["properties"]["fibonacci_pair"],
            "step_gap": benchmark["step_count"] - actual["step_count"],
        },
    }
