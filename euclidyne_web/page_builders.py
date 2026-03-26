"""Page-model builders shared by Flask routes and APIs."""

from __future__ import annotations

from typing import Any, Mapping

from .claims import claim_status_counts, list_claims
from .facts import FACTS, facts_for_lab
from .lab_registry import atlas_groups, get_lab, related_labs
from .mathcore import (
    build_centered_euclid_model,
    build_euclid_model,
    build_fibonacci_comparison,
    build_gear_ratio_model,
    build_meshing_model,
    build_quadratic_surd_model,
    build_rational_sky_model,
    build_rectangle_model,
    build_rhythm_model,
)
from .mathcore.euclid import extended_gcd
from .sources import gather_sources, list_sources


def _read_int(
    values: Mapping[str, object],
    name: str,
    default: int,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    raw = str(values.get(name, default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"Use an integer value for {name}.") from exc
    if minimum is not None and value < minimum:
        raise ValueError(f"Use {name} >= {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"Use {name} <= {maximum}.")
    return value


def _read_float(
    values: Mapping[str, object],
    name: str,
    default: float,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    raw = str(values.get(name, default)).strip()
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"Use a numeric value for {name}.") from exc
    if minimum is not None and value < minimum:
        raise ValueError(f"Use {name} >= {minimum}.")
    if maximum is not None and value > maximum:
        raise ValueError(f"Use {name} <= {maximum}.")
    return value


def _assemble_page(slug: str, inputs: dict[str, object], model: dict[str, Any] | None, ui: dict[str, Any]) -> dict[str, Any]:
    lab = get_lab(slug)
    claims = list_claims(slug)
    facts = facts_for_lab(slug)
    source_ids = list(lab["source_ids"])
    for claim in claims:
        source_ids.extend(claim["source_ids"])
    for fact in facts:
        source_ids.append(fact["source_id"])
    return {
        "lab": lab,
        "inputs": inputs,
        "model": model,
        "claims": claims,
        "facts": facts,
        "sources": gather_sources(source_ids),
        "related_labs": related_labs(slug),
        "ui": ui,
    }


def _build_euclid_page(slug: str, values: Mapping[str, object], *, include_geometry: bool = False, include_fibonacci: bool = False) -> dict[str, Any]:
    lab = get_lab(slug)
    default_inputs = lab["default_inputs"]
    a = _read_int(values, "a", int(default_inputs["a"]), minimum=1)
    b = _read_int(values, "b", int(default_inputs["b"]), minimum=1)
    inputs = {"a": a, "b": b}
    ui: dict[str, Any] = {"error": None, "needs_swap": False, "swap_params": None}
    if a < b:
        ui["error"] = "Use a >= b > 0 for this visual model."
        ui["needs_swap"] = True
        ui["swap_params"] = {"a": b, "b": a}
        return _assemble_page(slug, inputs, None, ui)
    model = build_euclid_model(a, b)
    if include_geometry:
        model["geometry"] = build_rectangle_model(a, b)
    if include_fibonacci:
        model = build_fibonacci_comparison(a, b)
    return _assemble_page(slug, inputs, model, ui)


def build_lab_page(slug: str, values: Mapping[str, object]) -> dict[str, Any]:
    """Build a fully-populated lab page payload."""

    if slug == "quick-calculator":
        return _build_euclid_page(slug, values)
    if slug == "algorithm-explorer":
        return _build_euclid_page(slug, values)
    if slug == "rectangle-reactor":
        return _build_euclid_page(slug, values, include_geometry=True)
    if slug == "fibonacci-race":
        return _build_euclid_page(slug, values, include_fibonacci=True)
    if slug == "centered-euclid-race":
        lab = get_lab(slug)
        a = _read_int(values, "a", int(lab["default_inputs"]["a"]), minimum=1)
        b = _read_int(values, "b", int(lab["default_inputs"]["b"]), minimum=1)
        inputs = {"a": a, "b": b}
        ui: dict[str, Any] = {"error": None, "needs_swap": False, "swap_params": None}
        if a < b:
            ui["error"] = "Use a >= b > 0 for this visual model."
            ui["needs_swap"] = True
            ui["swap_params"] = {"a": b, "b": a}
            return _assemble_page(slug, inputs, None, ui)
        return _assemble_page(slug, inputs, build_centered_euclid_model(a, b), ui)
    if slug == "gear-ratio-forge":
        lab = get_lab(slug)
        inputs = {
            "target_num": _read_int(values, "target_num", int(lab["default_inputs"]["target_num"]), minimum=1),
            "target_den": _read_int(values, "target_den", int(lab["default_inputs"]["target_den"]), minimum=1),
            "max_teeth": _read_int(values, "max_teeth", int(lab["default_inputs"]["max_teeth"]), minimum=8, maximum=120),
            "stages": _read_int(values, "stages", int(lab["default_inputs"]["stages"]), minimum=1, maximum=4),
        }
        return _assemble_page(slug, inputs, build_gear_ratio_model(**inputs), {"error": None})
    if slug == "rational-sky":
        lab = get_lab(slug)
        view = str(values.get("view", lab["default_inputs"]["view"])).strip() or "orchard"
        if view not in {"orchard", "farey", "ford", "stern_brocot"}:
            view = "orchard"
        inputs = {
            "max_den": _read_int(values, "max_den", int(lab["default_inputs"]["max_den"]), minimum=2, maximum=16),
            "p": _read_int(values, "p", int(lab["default_inputs"]["p"]), minimum=1),
            "q": _read_int(values, "q", int(lab["default_inputs"]["q"]), minimum=1),
            "view": view,
        }
        ui: dict[str, Any] = {"error": None, "needs_swap": False, "swap_params": None}
        if inputs["p"] > inputs["q"]:
            ui["error"] = "Use 0 < p <= q so the selected rational stays inside the unit interval."
            ui["needs_swap"] = True
            ui["swap_params"] = {
                "max_den": inputs["max_den"],
                "p": inputs["q"],
                "q": inputs["p"],
                "view": view,
            }
            return _assemble_page(slug, inputs, None, ui)
        return _assemble_page(
            slug,
            inputs,
            build_rational_sky_model(inputs["max_den"], inputs["p"], inputs["q"], view),
            ui,
        )
    if slug == "modular-lock-lab":
        lab = get_lab(slug)
        a = _read_int(values, "a", int(lab["default_inputs"]["a"]), minimum=1)
        m = _read_int(values, "m", int(lab["default_inputs"]["m"]), minimum=2)
        g_value, x_value, y_value = extended_gcd(a, m)
        model = {
            "a": a,
            "m": m,
            "gcd": g_value,
            "inverse": x_value % m if g_value == 1 else None,
            "bezout": {"x": x_value, "y": y_value, "identity": f"{a} * ({x_value}) + {m} * ({y_value}) = {g_value}"},
            "locked": g_value != 1,
            "reduced_a": a % m,
        }
        return _assemble_page(slug, {"a": a, "m": m}, model, {"error": None})
    if slug == "rhythm-sequencer":
        lab = get_lab(slug)
        steps = _read_int(values, "steps", int(lab["default_inputs"]["steps"]), minimum=2, maximum=32)
        pulses = _read_int(values, "pulses", int(lab["default_inputs"]["pulses"]), minimum=1, maximum=steps)
        rotation = _read_int(values, "rotation", int(lab["default_inputs"]["rotation"]), minimum=0, maximum=steps - 1)
        bpm = _read_int(values, "bpm", int(lab["default_inputs"]["bpm"]), minimum=40, maximum=220)
        return _assemble_page(
            slug,
            {"steps": steps, "pulses": pulses, "rotation": rotation, "bpm": bpm},
            build_rhythm_model(steps, pulses, rotation, bpm),
            {"error": None},
        )
    if slug == "meshing-reality-check":
        lab = get_lab(slug)
        inputs = {
            "driver_teeth": _read_int(values, "driver_teeth", int(lab["default_inputs"]["driver_teeth"]), minimum=8, maximum=120),
            "follower_teeth": _read_int(values, "follower_teeth", int(lab["default_inputs"]["follower_teeth"]), minimum=8, maximum=120),
            "center_scale": _read_float(values, "center_scale", float(lab["default_inputs"]["center_scale"]), minimum=0.96, maximum=1.15),
        }
        return _assemble_page(slug, inputs, build_meshing_model(**inputs), {"error": None})
    if slug == "quadratic-surd-loop":
        lab = get_lab(slug)
        inputs = {
            "n": _read_int(values, "n", int(lab["default_inputs"]["n"]), minimum=2),
            "terms": _read_int(values, "terms", int(lab["default_inputs"]["terms"]), minimum=6, maximum=32),
        }
        return _assemble_page(slug, inputs, build_quadratic_surd_model(**inputs), {"error": None})
    raise KeyError(f"Unknown lab slug: {slug}")


def build_home_page() -> dict[str, Any]:
    """Build the atlas hub payload."""

    return {
        "atlas_groups": atlas_groups(),
        "claim_status_counts": claim_status_counts(),
    }


def build_references_page() -> dict[str, Any]:
    """Build the references page payload."""

    return {
        "claims": list_claims(),
        "facts": list(FACTS),
        "sources": list_sources(),
        "claim_status_counts": claim_status_counts(),
    }
