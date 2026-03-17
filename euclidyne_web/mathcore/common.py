"""Shared math and serialization helpers for Euclidyne."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from fractions import Fraction
from math import isqrt
from typing import Any


def to_payload(value: Any) -> Any:
    """Recursively convert dataclasses, fractions, and containers to JSON-safe payloads."""

    if is_dataclass(value):
        return {field.name: to_payload(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Fraction):
        return fraction_payload(value)
    if isinstance(value, dict):
        return {key: to_payload(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_payload(item) for item in value]
    return value


def fraction_payload(value: Fraction, digits: int = 8) -> dict[str, Any]:
    """Serialize a fraction with both exact and decimal views."""

    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": round(float(value), digits),
    }


def continued_fraction_notation(quotients: list[int]) -> str:
    """Return a compact continued-fraction notation string."""

    if not quotients:
        return "[]"
    first = quotients[0]
    rest = ", ".join(str(item) for item in quotients[1:])
    if not rest:
        return f"[{first}]"
    return f"[{first}; {rest}]"


def is_perfect_square(value: int) -> bool:
    """Return whether a positive integer is a perfect square."""

    if value < 0:
        return False
    root = isqrt(value)
    return root * root == value
