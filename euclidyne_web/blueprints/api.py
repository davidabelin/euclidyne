from __future__ import annotations

from flask import Blueprint, jsonify, request

from euclidorithm.euclidyne_web.content import explanation_meta
from euclidorithm.euclidyne_web.mathcore import build_euclid_model


api_bp = Blueprint("api", __name__)


def _parse_api_inputs():
    raw_a = str(request.args.get("a", "")).strip()
    raw_b = str(request.args.get("b", "")).strip()
    if not raw_a or not raw_b:
        return None, None, "Provide integer query parameters a and b."
    try:
        a = int(raw_a)
        b = int(raw_b)
    except ValueError:
        return None, None, "Use integer values for a and b."
    return a, b, None


@api_bp.get("/api/v1/euclid")
def euclid_api():
    a, b, error = _parse_api_inputs()
    if error is not None:
        return jsonify({"ok": False, "error": error}), 400
    if a <= 0 or b <= 0:
        return jsonify({"ok": False, "error": "Use positive integers for a and b."}), 400
    if a < b:
        return (
            jsonify(
                {
                    "ok": False,
                    "error": "Use a >= b > 0 for the visual model.",
                    "needs_swap": True,
                    "swap_pair": {"a": b, "b": a},
                }
            ),
            400,
        )

    model = build_euclid_model(a, b)
    model["ok"] = True
    model["explanation_meta"] = explanation_meta()
    return jsonify(model)

