"""Fun fact registry for Euclidyne labs."""

from __future__ import annotations


FACTS = [
    {
        "id": "fact-oldest-algorithm",
        "lab_slugs": ["quick-calculator", "algorithm-explorer", "home"],
        "title": "Ancient, Still Useful",
        "body": "Euclid's algorithm is one of the oldest named algorithms that is still used directly in modern software.",
        "source_id": "euclid_book_vii",
        "illustration": {"kind": "medallion", "label": "c. 300 BCE"},
    },
    {
        "id": "fact-lame",
        "lab_slugs": ["fibonacci-race", "centered-euclid-race", "home"],
        "title": "Lamé's 1844 Result",
        "body": "Gabriel Lamé's Euclid analysis is a classic early complexity result: Fibonacci pairs force the slowest standard run.",
        "source_id": "mathworld_euclidean_algorithm",
        "illustration": {"kind": "banner", "label": "1844"},
    },
    {
        "id": "fact-brocot",
        "lab_slugs": ["gear-ratio-forge", "rational-sky", "home"],
        "title": "A Clockmaker's Tree",
        "body": "Achille Brocot was a clockmaker. The Stern-Brocot tree has real gear-ratio history, not just abstract number theory.",
        "source_id": "mathworld_stern_brocot",
        "illustration": {"kind": "gear", "label": "Brocot"},
    },
    {
        "id": "fact-ford",
        "lab_slugs": ["rational-sky"],
        "title": "Not That Ford",
        "body": "Ford circles are named after Lester Ford, the mathematician, not Henry Ford.",
        "source_id": "mathworld_ford",
        "illustration": {"kind": "orbit", "label": "Ford"},
    },
    {
        "id": "fact-visible-points",
        "lab_slugs": ["rational-sky"],
        "title": "Coprime Means Visible",
        "body": "A lattice point is visible from the origin exactly when its coordinates share no common factor.",
        "source_id": "mathworld_orchard",
        "illustration": {"kind": "grid", "label": "gcd=1"},
    },
    {
        "id": "fact-rhythms",
        "lab_slugs": ["rhythm-sequencer", "home"],
        "title": "Math That You Can Hear",
        "body": "Euclidean rhythm patterns show up in multiple traditional musical families because they spread beats as evenly as possible.",
        "source_id": "toussaint_rhythms",
        "illustration": {"kind": "pulse", "label": "x..x.."},
    },
    {
        "id": "fact-golden-special",
        "lab_slugs": ["rectangle-reactor", "quadratic-surd-loop"],
        "title": "Special, Not Generic",
        "body": "The golden spiral story depends on self-similarity. Arbitrary Euclidean rectangle cuts do not automatically inherit it.",
        "source_id": "golden_rectangle",
        "illustration": {"kind": "spiral", "label": "phi"},
    },
    {
        "id": "fact-katex-ready",
        "lab_slugs": ["quadratic-surd-loop", "algorithm-explorer"],
        "title": "Fast Math Rendering",
        "body": "Typeset equations help when the same integer process is shown as division, continued fractions, and recurrences.",
        "source_id": "bell",
        "illustration": {"kind": "formula", "label": "[a0;a1,...]"},
    },
]


def facts_for_lab(lab_slug: str) -> list[dict[str, object]]:
    """Return the facts associated with a lab or page."""

    return [fact for fact in FACTS if lab_slug in fact["lab_slugs"]]


def primary_fact(lab_slug: str) -> dict[str, object] | None:
    """Return the first available fact for a lab, if any."""

    matches = facts_for_lab(lab_slug)
    return matches[0] if matches else None
