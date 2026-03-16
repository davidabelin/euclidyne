"""Curated sources and claim registry for Euclidyne."""

from __future__ import annotations

from collections import Counter
from typing import Any


SOURCES: dict[str, dict[str, str]] = {
    "bell": {
        "id": "bell",
        "title": "Jordan Bell, The Euclidean algorithm and finite continued fractions",
        "url": "https://jordanbell.info/LaTeX/euclideanalgorithm/euclideanalgorithm.pdf",
        "note": "Primary math reference for Euclid, finite continued fractions, and quotient structure.",
    },
    "euclid_book_vii": {
        "id": "euclid_book_vii",
        "title": "Clark University, Euclid's Elements, Book VII",
        "url": "http://aleph0.clarku.edu/~djoyce/elements/bookVII/bookVII.html",
        "note": "Readable translation of the arithmetic Euclidean-algorithm setting.",
    },
    "cambridge_gears": {
        "id": "cambridge_gears",
        "title": "Cambridge DANotes, Gear Meshing",
        "url": "https://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/DAN/gears/meshing/meshing.html",
        "note": "Engineering reference for what actual meshed gears do and do not compute directly.",
    },
    "golden_rectangle": {
        "id": "golden_rectangle",
        "title": "The Mathematical Gazette, Golden rectangles and the logarithmic spiral",
        "url": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8B3A00A26C1E9FF5CB8A4D9340D87EBD/S0008439500004603a.pdf/div-classtitleGolden-rectangles-and-the-logarithmic-spiraldiv.pdf",
        "note": "Reference for the special golden-rectangle/logarithmic-spiral case.",
    },
}


CLAIMS: list[dict[str, Any]] = [
    {
        "id": "verified-euclid-cf",
        "status": "verified",
        "pages": ["home", "explorer", "continued_fractions", "references"],
        "statement": "Running the Euclidean algorithm on positive integers yields the finite continued fraction of a/b.",
        "source_ids": ["bell", "euclid_book_vii"],
    },
    {
        "id": "verified-bezout",
        "status": "verified",
        "pages": ["home", "explorer", "quick", "references"],
        "statement": "Extended Euclid produces coefficients x and y with a*x + b*y = gcd(a, b).",
        "source_ids": ["bell"],
    },
    {
        "id": "verified-mod-inverse",
        "status": "verified",
        "pages": ["explorer", "references"],
        "statement": "If gcd(a, b) = 1, the x coefficient from extended Euclid gives the inverse of a modulo b.",
        "source_ids": ["bell"],
    },
    {
        "id": "verified-rectangle",
        "status": "verified",
        "pages": ["home", "continued_fractions", "references"],
        "statement": "Rectangle-to-squares dissection follows the same quotient sequence as the Euclidean algorithm.",
        "source_ids": ["bell"],
    },
    {
        "id": "verified-golden-special",
        "status": "verified",
        "pages": ["continued_fractions", "references"],
        "statement": "The logarithmic-spiral story belongs to the special golden-rectangle case, not to every Euclidean rectangle dissection.",
        "source_ids": ["golden_rectangle"],
    },
    {
        "id": "analogy-phase",
        "status": "analogy",
        "pages": ["home", "phase", "references"],
        "statement": "A single division step can be visualized as q full turns plus a residual phase r/b, but that is an analogy, not a complete autonomous machine.",
        "source_ids": ["cambridge_gears", "bell"],
    },
    {
        "id": "deferred-gear-machine",
        "status": "deferred",
        "pages": ["home", "references"],
        "statement": "Automatic compound-gear or sliding-gear Euclid machines are deferred because the underlying claims were not strong enough to ship as verified mechanics.",
        "source_ids": ["cambridge_gears"],
    },
    {
        "id": "deferred-spiral",
        "status": "deferred",
        "pages": ["home", "references"],
        "statement": "Generic inward-spiral or logarithmic-spiral claims for all gear or rectangle models are deferred; only the golden special case is retained.",
        "source_ids": ["golden_rectangle"],
    },
]


AUDIT_NOTES: list[str] = [
    "Verified math claims drive the app; analogy and deferred claims are visibly labeled instead of blended together.",
    "The new Phase Lab keeps the one-step cycle intuition while dropping unsupported multi-stage gear automation.",
    "The geometry view uses generated rectangle/square diagrams instead of imported spiral imagery.",
]


def list_sources() -> list[dict[str, str]]:
    return [SOURCES[key] for key in sorted(SOURCES)]


def list_claims(page: str | None = None) -> list[dict[str, Any]]:
    claims = CLAIMS
    if page is not None:
        claims = [claim for claim in CLAIMS if page in claim["pages"]]
    return claims


def claim_status_counts() -> dict[str, int]:
    counts = Counter(claim["status"] for claim in CLAIMS)
    return dict(counts)


def explanation_meta() -> dict[str, Any]:
    return {
        "verified_topics": [
            "euclidean_algorithm",
            "extended_euclid",
            "continued_fractions",
            "rectangle_dissections",
            "modular_inverse",
        ],
        "analogy_topics": ["phase_lab"],
        "deferred_topics": ["compound_gears", "sliding_gears", "generic_spiral_claims"],
    }

