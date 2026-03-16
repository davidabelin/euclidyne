from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from euclidorithm.euclidyne_web.content import AUDIT_NOTES, claim_status_counts, list_claims, list_sources
from euclidorithm.euclidyne_web.mathcore import build_euclid_model


main_bp = Blueprint("main", __name__)


PAGE_DEFAULTS = {
    "home": (240, 46),
    "quick": (12082, 5280),
    "explorer": (240, 46),
    "continued_fractions": (55, 34),
    "phase": (55, 34),
}


def _request_values():
    return request.form if request.method == "POST" else request.args


def _parse_visual_inputs(default_a: int, default_b: int) -> dict[str, Any]:
    values = _request_values()
    raw_a = str(values.get("a", default_a)).strip()
    raw_b = str(values.get("b", default_b)).strip()

    context: dict[str, Any] = {
        "a": default_a,
        "b": default_b,
        "error": None,
        "needs_swap": False,
        "swap_pair": None,
        "model": None,
    }

    try:
        a = int(raw_a)
        b = int(raw_b)
    except ValueError:
        context["error"] = "Use integer values for both inputs."
        return context

    context["a"] = a
    context["b"] = b

    if a <= 0 or b <= 0:
        context["error"] = "Use positive integers."
        return context
    if a < b:
        context["needs_swap"] = True
        context["swap_pair"] = {"a": b, "b": a}
        context["error"] = "This visual model expects a >= b > 0."
        return context

    context["model"] = build_euclid_model(a, b)
    return context


def _page_context(page: str) -> dict[str, Any]:
    default_a, default_b = PAGE_DEFAULTS[page]
    context = _parse_visual_inputs(default_a, default_b)
    context["active"] = page
    context["claims"] = list_claims(page)
    context["status_counts"] = claim_status_counts()
    return context


def _redirect_with_pair(endpoint: str):
    values = request.values
    query = {}
    if "a" in values and "b" in values:
        query["a"] = values.get("a", "")
        query["b"] = values.get("b", "")
    return redirect(url_for(endpoint, **query))


@main_bp.route("/", methods=["GET", "POST"])
def home() -> str:
    context = _page_context("home")
    context["featured_pages"] = [
        {
            "title": "Quick Calculator",
            "description": "Preserved CLI-like output for line-by-line verification.",
            "endpoint": "main.quick",
        },
        {
            "title": "Algorithm Explorer",
            "description": "Interactive Euclid and Extended Euclid state table with synced explanations.",
            "endpoint": "main.explorer",
        },
        {
            "title": "Continued Fractions + Geometry",
            "description": "Convergents, quotient structure, and rectangle dissection generated from one model.",
            "endpoint": "main.continued_fractions",
        },
        {
            "title": "Phase Lab",
            "description": "One-step cycle analogy, clearly labeled as analogy rather than proof.",
            "endpoint": "main.phase",
        },
    ]
    return render_template("pages/home.html", **context)


@main_bp.route("/quick", methods=["GET", "POST"])
def quick() -> str:
    return render_template("pages/quick.html", **_page_context("quick"))


@main_bp.route("/explorer", methods=["GET", "POST"])
def explorer() -> str:
    return render_template("pages/explorer.html", **_page_context("explorer"))


@main_bp.route("/continued-fractions", methods=["GET", "POST"])
def continued_fractions() -> str:
    return render_template("pages/continued_fractions.html", **_page_context("continued_fractions"))


@main_bp.route("/phase", methods=["GET", "POST"])
def phase() -> str:
    return render_template("pages/phase.html", **_page_context("phase"))


@main_bp.get("/references")
def references() -> str:
    return render_template(
        "pages/references.html",
        active="references",
        claims=list_claims(),
        sources=list_sources(),
        audit_notes=AUDIT_NOTES,
        status_counts=claim_status_counts(),
    )


@main_bp.route("/table", methods=["GET", "POST"])
@main_bp.route("/extended", methods=["GET", "POST"])
@main_bp.route("/wp", methods=["GET", "POST"])
def legacy_explorer() -> Any:
    return _redirect_with_pair("main.explorer")


@main_bp.route("/gear", methods=["GET", "POST"])
@main_bp.route("/lock", methods=["GET", "POST"])
def legacy_phase() -> Any:
    return _redirect_with_pair("main.phase")


@main_bp.get("/healthz")
def healthz():
    return jsonify({"status": "ok", "service": "euclidyne"})
