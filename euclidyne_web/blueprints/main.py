"""HTML routes and compatibility redirects for Euclidyne."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from ..page_builders import (
    build_home_page,
    build_lab_page,
    build_references_page,
)


main_bp = Blueprint("main", __name__)


LAB_TEMPLATE_BY_SLUG = {
    "quick-calculator": "pages/quick_calculator.html",
    "algorithm-explorer": "pages/algorithm_explorer.html",
    "rectangle-reactor": "pages/rectangle_reactor.html",
    "gear-ratio-forge": "pages/gear_ratio_forge.html",
    "fibonacci-race": "pages/fibonacci_race.html",
    "rational-sky": "pages/rational_sky.html",
    "modular-lock-lab": "pages/modular_lock_lab.html",
    "rhythm-sequencer": "pages/rhythm_sequencer.html",
    "centered-euclid-race": "pages/centered_euclid_race.html",
    "meshing-reality-check": "pages/meshing_reality_check.html",
    "quadratic-surd-loop": "pages/quadratic_surd_loop.html",
}


def _render_lab(slug: str) -> str:
    """Render one lab page, preserving validation errors in the UI model."""

    try:
        page = build_lab_page(slug, request.values)
    except ValueError as exc:
        page = build_lab_page(slug, {})
        page["ui"]["error"] = str(exc)
    return render_template(LAB_TEMPLATE_BY_SLUG[slug], page=page, active=slug)


@main_bp.route("/", methods=["GET", "POST"])
def home() -> str:
    """Render the Euclidyne atlas landing page."""

    return render_template("pages/home.html", page=build_home_page(), active="home")


@main_bp.route("/atlas", methods=["GET", "POST"])
def atlas() -> str:
    """Render the atlas view using the same payload as the landing page."""

    return render_template("pages/home.html", page=build_home_page(), active="atlas")


@main_bp.route("/quick", methods=["GET", "POST"])
def quick() -> str:
    """Render the quick-calculator lab."""

    return _render_lab("quick-calculator")


@main_bp.route("/explorer", methods=["GET", "POST"])
def explorer() -> str:
    """Render the algorithm-explorer lab."""

    return _render_lab("algorithm-explorer")


@main_bp.route("/rectangle-reactor", methods=["GET", "POST"])
def rectangle_reactor() -> str:
    """Render the rectangle-reactor lab."""

    return _render_lab("rectangle-reactor")


@main_bp.route("/gear-ratio-forge", methods=["GET", "POST"])
def gear_ratio_forge() -> str:
    """Render the gear-ratio-forge lab."""

    return _render_lab("gear-ratio-forge")


@main_bp.route("/fibonacci-race", methods=["GET", "POST"])
def fibonacci_race() -> str:
    """Render the fibonacci-race lab."""

    return _render_lab("fibonacci-race")


@main_bp.route("/rational-sky", methods=["GET", "POST"])
def rational_sky() -> str:
    """Render the rational-sky lab."""

    return _render_lab("rational-sky")


@main_bp.route("/modular-lock-lab", methods=["GET", "POST"])
def modular_lock_lab() -> str:
    """Render the modular-lock lab."""

    return _render_lab("modular-lock-lab")


@main_bp.route("/rhythm-sequencer", methods=["GET", "POST"])
def rhythm_sequencer() -> str:
    """Render the rhythm-sequencer lab."""

    return _render_lab("rhythm-sequencer")


@main_bp.route("/centered-euclid-race", methods=["GET", "POST"])
def centered_euclid_race() -> str:
    """Render the centered-Euclid lab."""

    return _render_lab("centered-euclid-race")


@main_bp.route("/meshing-reality-check", methods=["GET", "POST"])
def meshing_reality_check() -> str:
    """Render the meshing-reality-check lab."""

    return _render_lab("meshing-reality-check")


@main_bp.route("/quadratic-surd-loop", methods=["GET", "POST"])
def quadratic_surd_loop() -> str:
    """Render the quadratic-surd-loop lab."""

    return _render_lab("quadratic-surd-loop")


@main_bp.get("/references")
def references() -> str:
    """Render the references and claims register page."""

    return render_template("pages/references.html", page=build_references_page(), active="references")


def _redirect_with_pair(endpoint: str) -> Any:
    """Redirect a legacy route while preserving the current query string."""

    values = request.values
    query = {key: values.get(key, "") for key in values.keys()}
    return redirect(url_for(endpoint, **query))


@main_bp.route("/continued-fractions", methods=["GET", "POST"])
def legacy_continued_fractions() -> Any:
    """Redirect the legacy continued-fractions route to rectangle-reactor."""

    return _redirect_with_pair("main.rectangle_reactor")


@main_bp.route("/phase", methods=["GET", "POST"])
def legacy_phase() -> Any:
    """Redirect the legacy phase route to gear-ratio-forge."""

    return _redirect_with_pair("main.gear_ratio_forge")


@main_bp.route("/table", methods=["GET", "POST"])
@main_bp.route("/extended", methods=["GET", "POST"])
@main_bp.route("/wp", methods=["GET", "POST"])
def legacy_explorer() -> Any:
    """Redirect legacy explorer aliases to the canonical explorer route."""

    return _redirect_with_pair("main.explorer")


@main_bp.route("/gear", methods=["GET", "POST"])
def legacy_gear() -> Any:
    """Redirect the legacy gear route to meshing-reality-check."""

    return _redirect_with_pair("main.meshing_reality_check")


@main_bp.route("/lock", methods=["GET", "POST"])
def legacy_lock() -> Any:
    """Redirect the legacy lock route to modular-lock-lab."""

    return _redirect_with_pair("main.modular_lock_lab")


@main_bp.get("/healthz")
def healthz():
    """Return a lightweight health payload for uptime checks."""

    return jsonify({"status": "ok", "service": "euclidyne"})
