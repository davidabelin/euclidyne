"""Gear-ratio design and gear-meshing builders."""

from __future__ import annotations

from fractions import Fraction
from math import acos, cos, degrees, radians
from typing import Any

from euclidyne.euclidyne_web.mathcore.common import continued_fraction_notation, fraction_payload
from euclidyne.euclidyne_web.mathcore.euclid import build_convergents, build_phase_subpanel


def _continued_fraction_for_fraction(value: Fraction) -> list[int]:
    quotients: list[int] = []
    numerator = value.numerator
    denominator = value.denominator
    while denominator != 0:
        quotient, remainder = divmod(numerator, denominator)
        quotients.append(quotient)
        numerator, denominator = denominator, remainder
    return quotients


def _prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    candidate = 2
    remainder = value
    while candidate * candidate <= remainder:
        while remainder % candidate == 0:
            factors.append(candidate)
            remainder //= candidate
        candidate += 1
    if remainder > 1:
        factors.append(remainder)
    return factors


def _pack_factors(factors: list[int], max_groups: int, max_value: int) -> list[int] | None:
    groups: list[int] = [1]
    for factor in sorted(factors, reverse=True):
        placed = False
        for index in sorted(range(len(groups)), key=lambda item: groups[item]):
            if groups[index] * factor <= max_value:
                groups[index] *= factor
                placed = True
                break
        if placed:
            continue
        if len(groups) >= max_groups or factor > max_value:
            return None
        groups.append(factor)
    return sorted(groups, reverse=True)


def _simple_candidates(target: Fraction, max_teeth: int) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for driver_teeth in range(1, max_teeth + 1):
        for follower_teeth in range(1, max_teeth + 1):
            realized = Fraction(driver_teeth, follower_teeth)
            error = abs(float(realized - target))
            candidates.append(
                {
                    "kind": "simple",
                    "label": f"{driver_teeth}:{follower_teeth}",
                    "stages": [
                        {
                            "driver_teeth": driver_teeth,
                            "follower_teeth": follower_teeth,
                            "ratio": fraction_payload(realized),
                        }
                    ],
                    "realized_ratio": fraction_payload(realized),
                    "error_decimal": round(error, 8),
                    "exact": realized == target,
                    "total_teeth": driver_teeth + follower_teeth,
                }
            )
    candidates.sort(key=lambda item: (item["error_decimal"], item["total_teeth"]))
    return candidates[:8]


def _compound_candidate(target: Fraction, max_teeth: int, stages: int) -> dict[str, Any] | None:
    numerator_factors = _prime_factors(target.numerator)
    denominator_factors = _prime_factors(target.denominator)
    packed_numerator = _pack_factors(numerator_factors, stages, max_teeth)
    packed_denominator = _pack_factors(denominator_factors, stages, max_teeth)
    if packed_numerator is None or packed_denominator is None:
        return None
    stage_count = max(len(packed_numerator), len(packed_denominator))
    if stage_count > stages:
        return None
    while len(packed_numerator) < stage_count:
        packed_numerator.append(1)
    while len(packed_denominator) < stage_count:
        packed_denominator.append(1)
    stage_payload = []
    for numerator, denominator in zip(packed_numerator, packed_denominator, strict=True):
        stage_ratio = Fraction(numerator, denominator)
        stage_payload.append(
            {
                "driver_teeth": numerator,
                "follower_teeth": denominator,
                "ratio": fraction_payload(stage_ratio),
            }
        )
    return {
        "kind": "compound",
        "label": " x ".join(f"{stage['driver_teeth']}:{stage['follower_teeth']}" for stage in stage_payload),
        "stages": stage_payload,
        "realized_ratio": fraction_payload(target),
        "error_decimal": 0.0,
        "exact": True,
        "total_teeth": sum(stage["driver_teeth"] + stage["follower_teeth"] for stage in stage_payload),
    }


def build_gear_ratio_model(target_num: int, target_den: int, max_teeth: int, stages: int) -> dict[str, Any]:
    """Build a gear-ratio design payload using continued fractions and bounded tooth counts."""

    reduced = Fraction(target_num, target_den)
    quotients = _continued_fraction_for_fraction(reduced)
    convergents = build_convergents(reduced, quotients)
    simple_candidates = _simple_candidates(reduced, max_teeth)
    compound = _compound_candidate(reduced, max_teeth, stages)
    exact_simple = next((candidate for candidate in simple_candidates if candidate["exact"]), None)
    selected = exact_simple or compound or simple_candidates[0]
    return {
        "target": fraction_payload(reduced),
        "continued_fraction": {
            "quotients": quotients,
            "notation": continued_fraction_notation(quotients),
            "convergents": [
                {
                    "index": item.index,
                    "numerator": item.numerator,
                    "denominator": item.denominator,
                    "decimal": item.decimal,
                    "error_decimal": item.error_decimal,
                }
                for item in convergents
            ],
        },
        "candidates": {
            "simple": simple_candidates,
            "compound": compound,
            "selected": selected,
        },
        "phase_analogy": build_phase_subpanel(reduced.numerator, reduced.denominator),
        "notes": {
            "design_direction": "Continued fractions help choose good fixed gear ratios. The chosen train then realizes that ratio.",
            "warning": "This lab does not claim that a fixed gear train autonomously executes Euclid's full quotient-and-remainder recursion.",
        },
    }


def build_meshing_model(driver_teeth: int, follower_teeth: int, center_scale: float) -> dict[str, Any]:
    """Build a simple involute-gear meshing payload."""

    module = 6.0
    pressure_angle_deg = 20.0
    pressure_angle_rad = radians(pressure_angle_deg)
    driver_pitch_radius = driver_teeth * module / 2
    follower_pitch_radius = follower_teeth * module / 2
    standard_center_distance = driver_pitch_radius + follower_pitch_radius
    working_center_distance = standard_center_distance * center_scale
    base_sum = standard_center_distance * cos(pressure_angle_rad)
    if working_center_distance <= base_sum:
        raise ValueError("Use a larger center scale so the working pressure-angle model stays valid.")
    working_pressure_angle = acos(base_sum / working_center_distance)
    working_pressure_angle_deg = round(degrees(working_pressure_angle), 4)
    ratio = Fraction(driver_teeth, follower_teeth)
    state = "nominal"
    if center_scale < 0.995:
        state = "tighter"
    elif center_scale > 1.005:
        state = "looser"
    return {
        "driver": {
            "teeth": driver_teeth,
            "pitch_radius": round(driver_pitch_radius, 4),
        },
        "follower": {
            "teeth": follower_teeth,
            "pitch_radius": round(follower_pitch_radius, 4),
        },
        "ratio": fraction_payload(ratio),
        "center_scale": round(center_scale, 4),
        "center_distance": {
            "standard": round(standard_center_distance, 4),
            "working": round(working_center_distance, 4),
        },
        "pressure_angle": {
            "standard_deg": pressure_angle_deg,
            "working_deg": working_pressure_angle_deg,
            "delta_deg": round(working_pressure_angle_deg - pressure_angle_deg, 4),
        },
        "state": state,
        "notes": {
            "ratio_constant": f"The speed ratio stays {driver_teeth}/{follower_teeth} while the operating pressure angle shifts.",
            "contact_warning": "Changing center distance affects engagement conditions; it does not turn the shift into a discrete integer remainder.",
        },
    }
