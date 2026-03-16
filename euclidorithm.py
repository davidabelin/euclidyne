#!/usr/bin/env python3
"""Deprecated archive of the pre-Euclidyne Euclidorithm engine.

This file is retained only as an archival reference.

Current runtime
---------------
The active Flask app now lives in ``euclidorithm.euclidyne:app``.

Archive scope
-------------
The earlier ``euclidA.py`` and ``euclidB.py`` helpers have been folded into this
single module so the useful CLI-era Euclidean routines stay available without
remaining part of the deployed application surface.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List, Tuple


LEGACY_NOTES = [
    "The original single-file Flask app has been retired in favor of Euclidyne.",
    "This module remains for archival CLI reference only.",
]


@dataclass(frozen=True)
class DivStep:
    dividend: int
    divisor: int
    quotient: int
    remainder: int


def euclid_div_steps(a: int, b: int) -> Tuple[int, List[DivStep]]:
    """Return gcd and the forward division steps dividend = divisor*q + remainder."""

    if a == 0 and b == 0:
        raise ValueError("gcd(0, 0) is undefined.")
    steps: List[DivStep] = []
    dividend, divisor = a, b
    while divisor != 0:
        quotient, remainder = divmod(dividend, divisor)
        steps.append(
            DivStep(
                dividend=dividend,
                divisor=divisor,
                quotient=quotient,
                remainder=remainder,
            )
        )
        dividend, divisor = divisor, remainder
    return dividend, steps


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Return (g, x, y) such that a*x + b*y = g."""

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t


def print_forward(steps: List[DivStep]) -> None:
    for step in steps:
        print(f"{step.dividend} = {step.divisor} * {step.quotient} + {step.remainder}")


def reverse_expansion(a: int, b: int, steps: List[DivStep]) -> List[str]:
    """Produce a reverse substitution trace ending with a*x + b*y = gcd."""

    if not steps:
        g, x, y = extended_gcd(a, b)
        return [f"{a}*{x} + {b}*{y} = {g}"]

    r_vals = [steps[0].dividend, steps[0].divisor] + [step.remainder for step in steps]
    expr = {0: "a", 1: "b"}
    lines: List[str] = []
    for offset, step in enumerate(steps):
        index = offset + 2
        expr[index] = f"({expr[index - 2]}) - {step.quotient}*({expr[index - 1]})"
        if index != len(r_vals) - 1:
            lines.append(
                f"{r_vals[index]} = {r_vals[index - 2]} - {step.quotient}*{r_vals[index - 1]} = {expr[index]}"
            )

    g, x, y = extended_gcd(a, b)
    lines.append(f"{a}*{x} + {b}*{y} = {g}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Legacy Euclidorithm CLI archive.")
    parser.add_argument("a", type=int)
    parser.add_argument("b", type=int)
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Also print reverse expanded substitutions.",
    )
    args = parser.parse_args()

    gcd_value, steps = euclid_div_steps(args.a, args.b)
    _, x, y = extended_gcd(args.a, args.b)

    print_forward(steps)
    print()
    print(f"Steps taken     =      {len(steps)}")
    print(f"GCD({args.a}, {args.b}) = {gcd_value}")
    print(f"Bezout coefficients: x={x}, y={y} (so {args.a}*{x} + {args.b}*{y} = {gcd_value})")

    if args.reverse:
        print()
        for line in reverse_expansion(args.a, args.b, steps):
            print(line)


if __name__ == "__main__":
    main()

