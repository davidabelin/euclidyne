"""Site-wide claim registry for Euclidyne."""

from __future__ import annotations

from collections import Counter


CLAIMS = [
    {
        "id": "verified-euclid-cf",
        "status": "verified",
        "statement": "Running the Euclidean algorithm on positive integers yields the finite continued fraction of a/b.",
        "lab_slugs": [
            "quick-calculator",
            "algorithm-explorer",
            "rectangle-reactor",
            "fibonacci-race",
            "quadratic-surd-loop",
        ],
        "source_ids": ["bell", "euclid_book_vii"],
    },
    {
        "id": "verified-bezout",
        "status": "verified",
        "statement": "Extended Euclid produces coefficients x and y with a*x + b*y = gcd(a, b).",
        "lab_slugs": ["quick-calculator", "algorithm-explorer", "modular-lock-lab"],
        "source_ids": ["bell"],
    },
    {
        "id": "verified-mod-inverse",
        "status": "verified",
        "statement": "If gcd(a, b) = 1, the x coefficient from extended Euclid gives the inverse of a modulo b.",
        "lab_slugs": ["algorithm-explorer", "modular-lock-lab"],
        "source_ids": ["bell", "mathworld_mod_inverse"],
    },
    {
        "id": "verified-rectangle",
        "status": "verified",
        "statement": "Rectangle-to-squares dissection follows the same quotient sequence as the Euclidean algorithm.",
        "lab_slugs": ["rectangle-reactor", "fibonacci-race"],
        "source_ids": ["bell"],
    },
    {
        "id": "verified-golden-special",
        "status": "verified",
        "statement": "The logarithmic-spiral story belongs to the special golden-rectangle case, not to every Euclidean rectangle dissection.",
        "lab_slugs": ["rectangle-reactor", "fibonacci-race", "quadratic-surd-loop"],
        "source_ids": ["golden_rectangle", "golden_spiral"],
    },
    {
        "id": "verified-gear-design",
        "status": "verified",
        "statement": "Continued fractions are a valid way to design good rational gear ratios; the resulting gear train then realizes the chosen fixed ratio.",
        "lab_slugs": ["gear-ratio-forge", "rational-sky"],
        "source_ids": ["globalspec_gears", "mathworld_stern_brocot"],
    },
    {
        "id": "verified-visible-coprime",
        "status": "verified",
        "statement": "Visible lattice points from the origin correspond to coprime integer pairs.",
        "lab_slugs": ["rational-sky"],
        "source_ids": ["mathworld_orchard", "euclid_book_vii"],
    },
    {
        "id": "verified-rhythms",
        "status": "verified",
        "statement": "Euclidean rhythm constructions distribute pulses as evenly as possible across a cycle and connect directly to the Euclidean algorithm.",
        "lab_slugs": ["rhythm-sequencer"],
        "source_ids": ["toussaint_rhythms"],
    },
    {
        "id": "analogy-phase",
        "status": "analogy_only",
        "statement": "A single division step can be visualized as q full turns plus a residual phase r/b, but that is an analogy rather than a full autonomous machine.",
        "lab_slugs": ["algorithm-explorer", "gear-ratio-forge"],
        "source_ids": ["bell", "cambridge_gears"],
    },
    {
        "id": "analogy-automatic-gears",
        "status": "analogy_only",
        "statement": "Automatic compound-gear or sliding-gear Euclid machines remain a conceptual analogy unless sensing, control, and reconfiguration are added beyond a simple gear train.",
        "lab_slugs": ["gear-ratio-forge", "meshing-reality-check"],
        "source_ids": ["cambridge_gears", "globalspec_gears"],
    },
    {
        "id": "false-center-shift-remainder",
        "status": "false",
        "statement": "Changing the center distance of involute gears does not make the shift itself equal the integer remainder.",
        "lab_slugs": ["meshing-reality-check"],
        "source_ids": ["cambridge_gears"],
    },
    {
        "id": "false-generic-spiral",
        "status": "false",
        "statement": "Generic inward-spiral or logarithmic-spiral claims for arbitrary gear or rectangle models are not valid in general.",
        "lab_slugs": ["rectangle-reactor", "meshing-reality-check"],
        "source_ids": ["golden_rectangle", "golden_spiral"],
    },
    {
        "id": "false-historical-gear-euclid",
        "status": "false",
        "statement": "Historical compound gear trains did not themselves implement Euclid as an exact iterative algorithm on arbitrary inputs.",
        "lab_slugs": ["gear-ratio-forge", "meshing-reality-check"],
        "source_ids": ["globalspec_gears"],
    },
]


def list_claims(lab_slug: str | None = None) -> list[dict[str, object]]:
    """Return all claims, or only the claims relevant to one lab."""

    if lab_slug is None:
        return list(CLAIMS)
    return [claim for claim in CLAIMS if lab_slug in claim["lab_slugs"]]


def claim_status_counts() -> dict[str, int]:
    """Count claims by visible site status."""

    counts = Counter(claim["status"] for claim in CLAIMS)
    return dict(counts)
