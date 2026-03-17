from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from euclidyne.euclidyne_web.page_builders import (
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
    try:
        page = build_lab_page(slug, request.values)
    except ValueError as exc:
        page = build_lab_page(slug, {})
        page["ui"]["error"] = str(exc)
    return render_template(LAB_TEMPLATE_BY_SLUG[slug], page=page, active=slug)


@main_bp.route("/", methods=["GET", "POST"])
def home() -> str:
    return render_template("pages/home.html", page=build_home_page(), active="home")


@main_bp.route("/atlas", methods=["GET", "POST"])
def atlas() -> str:
    return render_template("pages/home.html", page=build_home_page(), active="atlas")


@main_bp.route("/quick", methods=["GET", "POST"])
def quick() -> str:
    return _render_lab("quick-calculator")


@main_bp.route("/explorer", methods=["GET", "POST"])
def explorer() -> str:
    return _render_lab("algorithm-explorer")


@main_bp.route("/rectangle-reactor", methods=["GET", "POST"])
def rectangle_reactor() -> str:
    return _render_lab("rectangle-reactor")


@main_bp.route("/gear-ratio-forge", methods=["GET", "POST"])
def gear_ratio_forge() -> str:
    return _render_lab("gear-ratio-forge")


@main_bp.route("/fibonacci-race", methods=["GET", "POST"])
def fibonacci_race() -> str:
    return _render_lab("fibonacci-race")


@main_bp.route("/rational-sky", methods=["GET", "POST"])
def rational_sky() -> str:
    return _render_lab("rational-sky")


@main_bp.route("/modular-lock-lab", methods=["GET", "POST"])
def modular_lock_lab() -> str:
    return _render_lab("modular-lock-lab")


@main_bp.route("/rhythm-sequencer", methods=["GET", "POST"])
def rhythm_sequencer() -> str:
    return _render_lab("rhythm-sequencer")


@main_bp.route("/centered-euclid-race", methods=["GET", "POST"])
def centered_euclid_race() -> str:
    return _render_lab("centered-euclid-race")


@main_bp.route("/meshing-reality-check", methods=["GET", "POST"])
def meshing_reality_check() -> str:
    return _render_lab("meshing-reality-check")


@main_bp.route("/quadratic-surd-loop", methods=["GET", "POST"])
def quadratic_surd_loop() -> str:
    return _render_lab("quadratic-surd-loop")


@main_bp.get("/references")
def references() -> str:
    return render_template("pages/references.html", page=build_references_page(), active="references")


def _redirect_with_pair(endpoint: str) -> Any:
    values = request.values
    query = {key: values.get(key, "") for key in values.keys()}
    return redirect(url_for(endpoint, **query))


@main_bp.route("/continued-fractions", methods=["GET", "POST"])
def legacy_continued_fractions() -> Any:
    return _redirect_with_pair("main.rectangle_reactor")


@main_bp.route("/phase", methods=["GET", "POST"])
def legacy_phase() -> Any:
    return _redirect_with_pair("main.gear_ratio_forge")


@main_bp.route("/table", methods=["GET", "POST"])
@main_bp.route("/extended", methods=["GET", "POST"])
@main_bp.route("/wp", methods=["GET", "POST"])
def legacy_explorer() -> Any:
    return _redirect_with_pair("main.explorer")


@main_bp.route("/gear", methods=["GET", "POST"])
def legacy_gear() -> Any:
    return _redirect_with_pair("main.meshing_reality_check")


@main_bp.route("/lock", methods=["GET", "POST"])
def legacy_lock() -> Any:
    return _redirect_with_pair("main.modular_lock_lab")


@main_bp.get("/healthz")
def healthz():
    return jsonify({"status": "ok", "service": "euclidyne"})
