"""Canonical Euclidean-algorithm model for Euclidyne."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import Any


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
    index: int
    dividend: int
    divisor: int
    quotient: int
    remainder: int
    color: str


@dataclass(frozen=True)
class ExtendedRow:
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
    index: int
    quotient: int
    numerator: int
    denominator: int
    decimal: float
    error_decimal: float


@dataclass(frozen=True)
class RectangleStage:
    index: int
    width: int
    height: int
    quotient: int
    remainder: int
    orientation: str
    square_size: int
    color: str


@dataclass(frozen=True)
class RectangleSquare:
    order: int
    stage_index: int
    x: int
    y: int
    size: int
    color: str
    arc_hint: str


def _color(index: int) -> str:
    return STEP_COLORS[index % len(STEP_COLORS)]


def _fraction_payload(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": round(float(value), 8),
    }


def build_euclid_model(a: int, b: int) -> dict[str, Any]:
    if a <= 0 or b <= 0:
        raise ValueError("Use positive integers.")
    if a < b:
        raise ValueError("Use a >= b > 0 for the visual model.")

    steps = _build_steps(a, b)
    extended = _build_extended_rows(a, b, steps)
    convergents = _build_convergents(a, b, steps)
    geometry = _build_geometry(a, b)
    gcd_value = steps[-1].divisor if steps[-1].remainder == 0 else steps[-1].remainder
    gcd_row = next(row for row in extended if row.is_gcd_row)
    phase = _build_phase_model(steps[0])

    return {
        "input": {
            "a": a,
            "b": b,
            "ratio": _fraction_payload(Fraction(a, b)),
        },
        "gcd": gcd_value,
        "step_count": len(steps),
        "steps": [asdict(step) for step in steps],
        "rows": [asdict(row) for row in extended],
        "bezout": {
            "x": gcd_row.s,
            "y": gcd_row.t,
            "identity": gcd_row.identity,
            "inverse_mod_b": gcd_row.s % b if gcd_value == 1 else None,
        },
        "continued_fraction": {
            "quotients": [step.quotient for step in steps],
            "notation": "[" + ", ".join(str(step.quotient) for step in steps) + "]",
            "convergents": [asdict(item) for item in convergents],
        },
        "geometry": geometry,
        "phase": phase,
    }


def _build_steps(a: int, b: int) -> list[EuclidStep]:
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


def _build_extended_rows(a: int, b: int, steps: list[EuclidStep]) -> list[ExtendedRow]:
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


def _build_convergents(a: int, b: int, steps: list[EuclidStep]) -> list[Convergent]:
    target = Fraction(a, b)
    p_minus_2, p_minus_1 = 0, 1
    q_minus_2, q_minus_1 = 1, 0
    convergents: list[Convergent] = []
    for index, step in enumerate(steps, start=1):
        p_value = step.quotient * p_minus_1 + p_minus_2
        q_value = step.quotient * q_minus_1 + q_minus_2
        value = Fraction(p_value, q_value)
        convergents.append(
            Convergent(
                index=index,
                quotient=step.quotient,
                numerator=p_value,
                denominator=q_value,
                decimal=round(float(value), 8),
                error_decimal=round(float(target - value), 8),
            )
        )
        p_minus_2, p_minus_1 = p_minus_1, p_value
        q_minus_2, q_minus_1 = q_minus_1, q_value
    return convergents


def _build_geometry(a: int, b: int) -> dict[str, Any]:
    width = a
    height = b
    x = 0
    y = 0
    stage_index = 1
    square_order = 0
    stages: list[RectangleStage] = []
    squares: list[RectangleSquare] = []
    arc_cycle = ["east", "south", "west", "north"]

    while width > 0 and height > 0:
        color = _color(stage_index - 1)
        if width >= height:
            quotient, remainder = divmod(width, height)
            stages.append(
                RectangleStage(
                    index=stage_index,
                    width=width,
                    height=height,
                    quotient=quotient,
                    remainder=remainder,
                    orientation="horizontal",
                    square_size=height,
                    color=color,
                )
            )
            for offset in range(quotient):
                squares.append(
                    RectangleSquare(
                        order=square_order,
                        stage_index=stage_index,
                        x=x + offset * height,
                        y=y,
                        size=height,
                        color=color,
                        arc_hint=arc_cycle[square_order % len(arc_cycle)],
                    )
                )
                square_order += 1
            x += quotient * height
            width = remainder
        else:
            quotient, remainder = divmod(height, width)
            stages.append(
                RectangleStage(
                    index=stage_index,
                    width=width,
                    height=height,
                    quotient=quotient,
                    remainder=remainder,
                    orientation="vertical",
                    square_size=width,
                    color=color,
                )
            )
            for offset in range(quotient):
                squares.append(
                    RectangleSquare(
                        order=square_order,
                        stage_index=stage_index,
                        x=x,
                        y=y + offset * width,
                        size=width,
                        color=color,
                        arc_hint=arc_cycle[square_order % len(arc_cycle)],
                    )
                )
                square_order += 1
            y += quotient * width
            height = remainder
        stage_index += 1

    return {
        "bounding_box": {"width": a, "height": b},
        "stages": [asdict(stage) for stage in stages],
        "squares": [asdict(square) for square in squares],
        "show_arc_note": "Quarter-circle overlays are optional visual guides; they are not generally logarithmic.",
    }


def _build_phase_model(step: EuclidStep) -> dict[str, Any]:
    full_ratio = Fraction(step.dividend, step.divisor)
    residual_ratio = Fraction(step.remainder, step.divisor)
    return {
        "dividend": step.dividend,
        "divisor": step.divisor,
        "quotient": step.quotient,
        "remainder": step.remainder,
        "driver_turns": 1,
        "follower_turns": _fraction_payload(full_ratio),
        "whole_turns": step.quotient,
        "residual_turn": {
            "numerator": step.remainder,
            "denominator": step.divisor,
            "decimal": round(float(residual_ratio), 8),
        },
        "summary": (
            f"One full driver turn yields {step.quotient} full follower turns "
            f"and a residual phase of {step.remainder}/{step.divisor}."
        ),
    }

