"""Normalized citation registry for Euclidyne."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SourceEntry:
    """A stable source identifier and its public citation metadata."""

    id: str
    title: str
    url: str
    note: str


SOURCE_ENTRIES = [
    SourceEntry(
        id="bell",
        title="Jordan Bell, The Euclidean algorithm and finite continued fractions",
        url="https://jordanbell.info/LaTeX/euclideanalgorithm/euclideanalgorithm.pdf",
        note="Primary reference for Euclid, continued fractions, and convergents.",
    ),
    SourceEntry(
        id="euclid_book_vii",
        title="Clark University, Euclid's Elements, Book VII",
        url="http://aleph0.clarku.edu/~djoyce/elements/bookVII/bookVII.html",
        note="Readable translation of Euclid's arithmetic algorithm setting.",
    ),
    SourceEntry(
        id="cambridge_gears",
        title="Cambridge DANotes, Gear Meshing",
        url="https://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/DAN/gears/meshing/meshing.html",
        note="Mechanical grounding for what actual involute gears do and do not compute.",
    ),
    SourceEntry(
        id="golden_rectangle",
        title="The Mathematical Gazette, Golden rectangles and the logarithmic spiral",
        url="https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8B3A00A26C1E9FF5CB8A4D9340D87EBD/S0008439500004603a.pdf/div-classtitleGolden-rectangles-and-the-logarithmic-spiraldiv.pdf",
        note="Reference for the special golden-rectangle/logarithmic-spiral case.",
    ),
    SourceEntry(
        id="golden_spiral",
        title="G. S. Chirikjian, The Golden Spiral",
        url="https://link.springer.com/chapter/10.1007/978-3-662-68931-8_8",
        note="Clarifies the special self-similar spiral construction.",
    ),
    SourceEntry(
        id="globalspec_gears",
        title="GlobalSpec, Graphical method of using continued fractions to find the best gear ratio",
        url="https://www.globalspec.com/reference/68680/203279/graphical-method-of-using-continued-fractions-to-find-the-best-gear-ratio",
        note="Historical engineering direction: Euclid and continued fractions help design gear trains.",
    ),
    SourceEntry(
        id="toussaint_rhythms",
        title="Godfried Toussaint, The Euclidean Algorithm Generates Traditional Musical Rhythms",
        url="https://archive.bridgesmathart.org/2005/bridges2005-47.html",
        note="Foundational source for Euclidean rhythms.",
    ),
    SourceEntry(
        id="mathworld_euclidean_algorithm",
        title="Wolfram MathWorld, Euclidean Algorithm",
        url="https://mathworld.wolfram.com/EuclideanAlgorithm.html",
        note="Compact reference for Lamé, Fibonacci worst cases, and algorithm variants.",
    ),
    SourceEntry(
        id="mathworld_farey",
        title="Wolfram MathWorld, Farey Sequence",
        url="https://mathworld.wolfram.com/FareySequence.html",
        note="Reference for Farey neighbors and rational ordering.",
    ),
    SourceEntry(
        id="mathworld_ford",
        title="Wolfram MathWorld, Ford Circle",
        url="https://mathworld.wolfram.com/FordCircle.html",
        note="Reference for Ford-circle geometry.",
    ),
    SourceEntry(
        id="mathworld_orchard",
        title="Wolfram MathWorld, Euclid's Orchard",
        url="https://mathworld.wolfram.com/EuclidsOrchard.html",
        note="Reference for visible lattice points and orchard geometry.",
    ),
    SourceEntry(
        id="mathworld_stern_brocot",
        title="Wolfram MathWorld, Stern-Brocot Tree",
        url="https://mathworld.wolfram.com/Stern-BrocotTree.html",
        note="Reference for the mediant tree and gear-ratio history.",
    ),
    SourceEntry(
        id="mathworld_mod_inverse",
        title="Wolfram MathWorld, Modular Inverse",
        url="https://mathworld.wolfram.com/ModularInverse.html",
        note="Reference for modular inversion and coprime gating.",
    ),
    SourceEntry(
        id="mathworld_periodic_cf",
        title="Wolfram MathWorld, Periodic Continued Fraction",
        url="https://mathworld.wolfram.com/PeriodicContinuedFraction.html",
        note="Reference for periodic continued fractions of quadratic surds.",
    ),
    SourceEntry(
        id="mathworld_lagrange_cf",
        title="Wolfram MathWorld, Lagrange's Continued Fraction Theorem",
        url="https://mathworld.wolfram.com/LagrangesContinuedFractionTheorem.html",
        note="Reference for eventual periodicity of quadratic surds.",
    ),
]


SOURCES_BY_ID = {entry.id: entry for entry in SOURCE_ENTRIES}


def get_source(source_id: str) -> dict[str, str]:
    """Return a serialized source entry by id."""

    return asdict(SOURCES_BY_ID[source_id])


def list_sources() -> list[dict[str, str]]:
    """Return the full source registry as serialized dictionaries."""

    return [asdict(entry) for entry in SOURCE_ENTRIES]


def gather_sources(source_ids: list[str]) -> list[dict[str, str]]:
    """Return unique serialized sources preserving first-seen order."""

    seen: set[str] = set()
    gathered: list[dict[str, str]] = []
    for source_id in source_ids:
        if source_id in seen:
            continue
        seen.add(source_id)
        gathered.append(get_source(source_id))
    return gathered
