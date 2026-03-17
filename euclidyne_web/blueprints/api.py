from __future__ import annotations

from flask import Blueprint, jsonify, request

from euclidyne.euclidyne_web.content import explanation_meta
from euclidyne.euclidyne_web.page_builders import build_lab_page


api_bp = Blueprint("api", __name__)


def _payload(slug: str, *, status_on_error: int = 400):
    try:
        page = build_lab_page(slug, request.args)
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), status_on_error
    error = page["ui"].get("error")
    if error:
        response = {
            "ok": False,
            "error": error,
            "inputs": page["inputs"],
        }
        if page["ui"].get("needs_swap"):
            response["needs_swap"] = True
            response["swap_params"] = page["ui"].get("swap_params")
        return jsonify(response), status_on_error
    page["ok"] = True
    page["explanation_meta"] = explanation_meta()
    return jsonify(page)


@api_bp.get("/api/v1/euclid")
def euclid_api_v1():
    return _payload("algorithm-explorer")


@api_bp.get("/api/v2/euclid")
def euclid_api_v2():
    return _payload("algorithm-explorer")


@api_bp.get("/api/v2/centered-euclid")
def centered_euclid_api():
    return _payload("centered-euclid-race")


@api_bp.get("/api/v2/gear-ratio")
def gear_ratio_api():
    return _payload("gear-ratio-forge")


@api_bp.get("/api/v2/rational-sky")
def rational_sky_api():
    return _payload("rational-sky")


@api_bp.get("/api/v2/modular-lock")
def modular_lock_api():
    return _payload("modular-lock-lab")


@api_bp.get("/api/v2/rhythm")
def rhythm_api():
    return _payload("rhythm-sequencer")


@api_bp.get("/api/v2/meshing")
def meshing_api():
    return _payload("meshing-reality-check")


@api_bp.get("/api/v2/quadratic-surd")
def quadratic_surd_api():
    return _payload("quadratic-surd-loop")
