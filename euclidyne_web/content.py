"""Compatibility helpers retained for the v2 content split."""

from __future__ import annotations

from typing import Any

from euclidyne.euclidyne_web.claims import claim_status_counts, list_claims
from euclidyne.euclidyne_web.sources import list_sources


AUDIT_NOTES: list[str] = [
    "Verified claims, analogy-only stories, and false claims stay visually distinct.",
    "Gear content now treats continued fractions as a ratio-design tool rather than as an unsupported autonomous Euclid machine.",
    "Fun facts, sources, and related labs are attached to each page rather than hidden in one references screen.",
]


def explanation_meta() -> dict[str, Any]:
    """Return broad topic groupings used by API clients and tests."""

    return {
        "verified_topics": [
            "euclidean_algorithm",
            "extended_euclid",
            "continued_fractions",
            "rectangle_dissections",
            "modular_inverse",
            "euclidean_rhythms",
            "rational_landscapes",
        ],
        "analogy_topics": ["phase_lab", "automatic_gears"],
        "false_topics": ["sliding_center_remainder", "generic_spiral_claims", "historical_gear_machine"],
    }
