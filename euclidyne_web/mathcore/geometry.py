"""Geometry-oriented Euclid builders."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Any

from .common import to_payload
from .euclid import (
    STEP_COLORS,
    build_convergents,
    build_division_steps,
    is_fibonacci_pair,
)


@dataclass(frozen=True)
class RectangleStage:
    """One rectangle-dissection stage."""

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
    """One square produced during the rectangle dissection."""

    order: int
    stage_index: int
    x: int
    y: int
    size: int
    color: str
    arc_hint: str


def build_rectangle_model(a: int, b: int) -> dict[str, Any]:
    """Build Euclidean rectangle-dissection geometry."""

    steps = build_division_steps(a, b)
    target = Fraction(a, b)
    width = a
    height = b
    x = 0
    y = 0
    square_order = 0
    stage_index = 1
    arc_cycle = ["east", "south", "west", "north"]
    stages: list[RectangleStage] = []
    squares: list[RectangleSquare] = []

    while width > 0 and height > 0:
        color = STEP_COLORS[(stage_index - 1) % len(STEP_COLORS)]
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

    quotients = [step.quotient for step in steps]
    convergents = build_convergents(target, quotients)
    golden_special = is_fibonacci_pair(a, b)
    return {
        "bounding_box": {"width": a, "height": b},
        "stages": to_payload(stages),
        "squares": to_payload(squares),
        "continued_fraction": {
            "quotients": quotients,
            "convergents": to_payload(convergents),
        },
        "golden_special": {
            "enabled": golden_special,
            "label": "Fibonacci approximation to the golden-ratio dissection" if golden_special else "No golden special case for this integer pair",
        },
        "notes": {
            "arc_overlay": "Quarter-circle guides are available for the golden-special case. They are not a generic logarithmic spiral proof.",
        },
    }


def _farey_sequence(order: int) -> list[Fraction]:
    values = {
        Fraction(numerator, denominator)
        for denominator in range(1, order + 1)
        for numerator in range(0, denominator + 1)
        if gcd(numerator, denominator) == 1
    }
    return sorted(values)


def _stern_brocot_path(numerator: int, denominator: int) -> list[dict[str, Any]]:
    left_num, left_den = 0, 1
    right_num, right_den = 1, 0
    path: list[dict[str, Any]] = []
    while True:
        mediant_num = left_num + right_num
        mediant_den = left_den + right_den
        node = {
            "left": f"{left_num}/{left_den}",
            "right": f"{right_num}/{right_den}",
            "mediant": f"{mediant_num}/{mediant_den}",
            "value": round(mediant_num / mediant_den, 8),
        }
        if mediant_num == numerator and mediant_den == denominator:
            node["move"] = "hit"
            path.append(node)
            break
        if numerator * mediant_den < denominator * mediant_num:
            node["move"] = "L"
            right_num, right_den = mediant_num, mediant_den
        else:
            node["move"] = "R"
            left_num, left_den = mediant_num, mediant_den
        path.append(node)
    return path


def build_rational_sky_model(max_den: int, p: int, q: int, view: str) -> dict[str, Any]:
    """Build shared rational data for orchard, Farey, Ford-circle, and Stern-Brocot views."""

    farey = _farey_sequence(max_den)
    selected = Fraction(p, q)
    orchard_points = [
        {
            "x": x,
            "y": y,
            "visible": gcd(x, y) == 1,
            "slope": round(y / x, 8),
            "label": f"{y}/{x}",
        }
        for x in range(1, max_den + 1)
        for y in range(1, max_den + 1)
    ]
    farey_payload = [
        {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "label": f"{value.numerator}/{value.denominator}",
            "decimal": round(float(value), 8),
            "is_selected": value == selected,
        }
        for value in farey
    ]
    ford_circles = [
        {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "x": round(float(value), 8),
            "radius": round(1 / (2 * value.denominator * value.denominator), 8),
            "label": f"{value.numerator}/{value.denominator}",
            "is_selected": value == selected,
        }
        for value in farey
    ]
    stern_brocot = _stern_brocot_path(selected.numerator, selected.denominator)
    return {
        "selected": {
            "numerator": selected.numerator,
            "denominator": selected.denominator,
            "label": f"{selected.numerator}/{selected.denominator}",
            "decimal": round(float(selected), 8),
        },
        "max_den": max_den,
        "view": view,
        "orchard": {
            "limit": max_den,
            "points": orchard_points,
            "visible_count": sum(1 for point in orchard_points if point["visible"]),
        },
        "farey": {"order": max_den, "fractions": farey_payload},
        "ford": {"circles": ford_circles},
        "stern_brocot": {
            "path": stern_brocot,
            "moves": "".join(node["move"] for node in stern_brocot if node["move"] in {"L", "R"}),
        },
    }
