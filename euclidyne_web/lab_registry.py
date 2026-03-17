"""Single source of truth for Euclidyne lab metadata."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from euclidyne.euclidyne_web.facts import primary_fact


@dataclass(frozen=True)
class LabEntry:
    """Metadata for one public lab or page."""

    slug: str
    route: str
    title: str
    subtitle: str
    summary: str
    group: str
    nav_label: str | None
    controller: str | None
    api_path: str | None
    claim_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    default_inputs: dict[str, object]
    related_labs: tuple[str, ...]
    status: str = "verified"


LAB_GROUPS = [
    {
        "id": "core-algorithm",
        "title": "Core Algorithm",
        "description": "The exact arithmetic backbone: Euclid, Bézout, inverses, and step-count behavior.",
    },
    {
        "id": "ratios-and-geometry",
        "title": "Ratios and Geometry",
        "description": "Continued fractions, dissections, rational landscapes, and gear-ratio design.",
    },
    {
        "id": "applications-and-reality-checks",
        "title": "Applications and Reality Checks",
        "description": "Locks, rhythms, and the mechanical claims that survive contact with the evidence.",
    },
]


LAB_ENTRIES = [
    LabEntry(
        slug="quick-calculator",
        route="/quick",
        title="Quick Calculator",
        subtitle="Fast Euclid Output for Trustworthy Spot Checks",
        summary="The preserved exact-text fast path for Euclid, Bézout, and modular inverse results.",
        group="core-algorithm",
        nav_label="Quick Calculator",
        controller=None,
        api_path="/api/v2/euclid",
        claim_ids=("verified-euclid-cf", "verified-bezout", "verified-mod-inverse"),
        source_ids=("bell", "euclid_book_vii"),
        default_inputs={"a": 12082, "b": 5280},
        related_labs=("algorithm-explorer", "centered-euclid-race", "modular-lock-lab"),
    ),
    LabEntry(
        slug="algorithm-explorer",
        route="/explorer",
        title="Algorithm Explorer",
        subtitle="Scrub Euclid Steps, Bézout Rows, and the One-Step Phase Analogy",
        summary="Interactive Euclid and Extended Euclid tables with synced equations and callouts.",
        group="core-algorithm",
        nav_label="Algorithm Explorer",
        controller="algorithm-explorer",
        api_path="/api/v2/euclid",
        claim_ids=("verified-euclid-cf", "verified-bezout", "verified-mod-inverse", "analogy-phase"),
        source_ids=("bell", "euclid_book_vii", "cambridge_gears"),
        default_inputs={"a": 240, "b": 46},
        related_labs=("quick-calculator", "rectangle-reactor", "modular-lock-lab"),
    ),
    LabEntry(
        slug="rectangle-reactor",
        route="/rectangle-reactor",
        title="Rectangle Reactor",
        subtitle="Continued Fractions, Square Cuts, and the Golden-Only Spiral Story",
        summary="A dissection lab that keeps the geometry true and labels the golden special case correctly.",
        group="ratios-and-geometry",
        nav_label=None,
        controller="rectangle-reactor",
        api_path="/api/v2/euclid",
        claim_ids=("verified-euclid-cf", "verified-rectangle", "verified-golden-special", "false-generic-spiral"),
        source_ids=("bell", "golden_rectangle", "golden_spiral"),
        default_inputs={"a": 55, "b": 34},
        related_labs=("algorithm-explorer", "fibonacci-race", "quadratic-surd-loop"),
    ),
    LabEntry(
        slug="gear-ratio-forge",
        route="/gear-ratio-forge",
        title="Gear Ratio Forge",
        subtitle="Design Fixed Ratios with Continued Fractions",
        summary="A gear-design lab that uses Euclid-style reduction honestly: for choosing ratios, not pretending the train runs Euclid by itself.",
        group="ratios-and-geometry",
        nav_label=None,
        controller="gear-ratio-forge",
        api_path="/api/v2/gear-ratio",
        claim_ids=("verified-gear-design", "analogy-phase", "analogy-automatic-gears", "false-historical-gear-euclid"),
        source_ids=("globalspec_gears", "cambridge_gears", "mathworld_stern_brocot"),
        default_inputs={"target_num": 355, "target_den": 113, "max_teeth": 60, "stages": 2},
        related_labs=("rational-sky", "meshing-reality-check", "algorithm-explorer"),
    ),
    LabEntry(
        slug="fibonacci-race",
        route="/fibonacci-race",
        title="Fibonacci Race",
        subtitle="Why Consecutive Fibonacci Numbers Drag Euclid Out the Longest",
        summary="A side-by-side comparison between your input and Fibonacci worst-case behavior.",
        group="core-algorithm",
        nav_label=None,
        controller="fibonacci-race",
        api_path="/api/v2/euclid",
        claim_ids=("verified-euclid-cf", "verified-rectangle", "verified-golden-special"),
        source_ids=("bell", "mathworld_euclidean_algorithm", "golden_rectangle"),
        default_inputs={"a": 89, "b": 55},
        related_labs=("rectangle-reactor", "centered-euclid-race", "quadratic-surd-loop"),
    ),
    LabEntry(
        slug="rational-sky",
        route="/rational-sky",
        title="Rational Sky",
        subtitle="One Map for Euclid's Orchard, Farey Rows, Ford Circles, and Stern-Brocot Paths",
        summary="A shared rational-data playground with multiple visual lenses on the same reduced fractions.",
        group="ratios-and-geometry",
        nav_label=None,
        controller="rational-sky",
        api_path="/api/v2/rational-sky",
        claim_ids=("verified-visible-coprime", "verified-gear-design"),
        source_ids=("mathworld_orchard", "mathworld_farey", "mathworld_ford", "mathworld_stern_brocot"),
        default_inputs={"max_den": 8, "p": 5, "q": 8, "view": "orchard"},
        related_labs=("gear-ratio-forge", "rectangle-reactor", "quadratic-surd-loop"),
    ),
    LabEntry(
        slug="modular-lock-lab",
        route="/modular-lock-lab",
        title="Modular Lock Lab",
        subtitle="When the Key Exists, Extended Euclid Finds It",
        summary="A lock-and-key view of modular inverses with coprime gating.",
        group="applications-and-reality-checks",
        nav_label=None,
        controller="modular-lock-lab",
        api_path="/api/v2/modular-lock",
        claim_ids=("verified-bezout", "verified-mod-inverse"),
        source_ids=("bell", "mathworld_mod_inverse"),
        default_inputs={"a": 13, "m": 34},
        related_labs=("algorithm-explorer", "quick-calculator", "centered-euclid-race"),
    ),
    LabEntry(
        slug="rhythm-sequencer",
        route="/rhythm-sequencer",
        title="Rhythm Sequencer",
        subtitle="Euclid, but You Can Hear It",
        summary="A pulse-distribution lab with transport controls and an audible Euclidean pattern.",
        group="applications-and-reality-checks",
        nav_label=None,
        controller="rhythm-sequencer",
        api_path="/api/v2/rhythm",
        claim_ids=("verified-rhythms",),
        source_ids=("toussaint_rhythms",),
        default_inputs={"steps": 16, "pulses": 5, "rotation": 0, "bpm": 112},
        related_labs=("algorithm-explorer", "fibonacci-race", "modular-lock-lab"),
    ),
    LabEntry(
        slug="centered-euclid-race",
        route="/centered-euclid-race",
        title="Centered Euclid Race",
        subtitle="Standard Remainders Versus Least-Absolute Remainders",
        summary="A comparison lab for two Euclid variants and how quickly they shrink the same pair.",
        group="core-algorithm",
        nav_label=None,
        controller="centered-euclid-race",
        api_path="/api/v2/centered-euclid",
        claim_ids=("verified-euclid-cf",),
        source_ids=("mathworld_euclidean_algorithm", "bell"),
        default_inputs={"a": 240, "b": 46},
        related_labs=("quick-calculator", "algorithm-explorer", "fibonacci-race"),
    ),
    LabEntry(
        slug="meshing-reality-check",
        route="/meshing-reality-check",
        title="Meshing Reality Check",
        subtitle="What Center-Distance Changes Really Do in an Involute Pair",
        summary="A debunk lab showing that the ratio stays fixed while contact conditions change.",
        group="applications-and-reality-checks",
        nav_label=None,
        controller="meshing-reality-check",
        api_path="/api/v2/meshing",
        claim_ids=(
            "analogy-automatic-gears",
            "false-center-shift-remainder",
            "false-generic-spiral",
            "false-historical-gear-euclid",
        ),
        source_ids=("cambridge_gears", "globalspec_gears"),
        default_inputs={"driver_teeth": 24, "follower_teeth": 40, "center_scale": 1.0},
        related_labs=("gear-ratio-forge", "rectangle-reactor", "algorithm-explorer"),
        status="debunk",
    ),
    LabEntry(
        slug="quadratic-surd-loop",
        route="/quadratic-surd-loop",
        title="Quadratic Surd Loop",
        subtitle="Periodic Continued Fractions for sqrt(n)",
        summary="A quadratic-irrational lab with period loops, convergents, and a Pell teaser.",
        group="ratios-and-geometry",
        nav_label=None,
        controller="quadratic-surd-loop",
        api_path="/api/v2/quadratic-surd",
        claim_ids=("verified-euclid-cf", "verified-golden-special"),
        source_ids=("mathworld_periodic_cf", "mathworld_lagrange_cf", "bell"),
        default_inputs={"n": 19, "terms": 16},
        related_labs=("rectangle-reactor", "fibonacci-race", "rational-sky"),
    ),
]


LABS_BY_SLUG = {entry.slug: entry for entry in LAB_ENTRIES}


def get_lab(slug: str) -> dict[str, object]:
    """Return serialized lab metadata for a slug."""

    return asdict(LABS_BY_SLUG[slug])


def related_labs(slug: str) -> list[dict[str, object]]:
    """Return serialized related lab metadata for one lab."""

    lab = LABS_BY_SLUG[slug]
    return [get_lab(related_slug) for related_slug in lab.related_labs]


def top_nav_labs() -> list[dict[str, object]]:
    """Return the compact top-nav lab set."""

    chosen = ["quick-calculator", "algorithm-explorer"]
    return [get_lab(slug) for slug in chosen]


def atlas_groups() -> list[dict[str, object]]:
    """Return the atlas layout with labs and one seed fact per group."""

    groups: list[dict[str, object]] = []
    for group in LAB_GROUPS:
        items = [entry for entry in LAB_ENTRIES if entry.group == group["id"]]
        fact = None
        for item in items:
            fact = primary_fact(item.slug)
            if fact is not None:
                break
        groups.append(
            {
                **group,
                "labs": [asdict(item) for item in items],
                "fact": fact,
            }
        )
    return groups
