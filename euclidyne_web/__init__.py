"""Flask application factory for Euclidyne."""

from __future__ import annotations

import os
from urllib.parse import urljoin

from flask import Flask

from euclidyne.euclidyne_web.lab_registry import top_nav_labs


def _normalize_base_url(value: str) -> str:
    raw = str(value or "").strip()
    return raw or "/"


def _aix_page_url(base_url: str, path: str) -> str:
    base = _normalize_base_url(base_url)
    if base == "/":
        return path
    return urljoin(base.rstrip("/") + "/", path.lstrip("/"))


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY", "euclidyne-dev-key"),
        APP_DISPLAY_NAME="Euclidyne",
        APP_TAGLINE="Instrument-Lab Explorations into Euclid, Ratios, and Rhythm",
        AIX_HUB_URL=os.getenv("AIX_HUB_URL", "/"),
    )
    if config:
        app.config.update(config)

    from euclidyne.euclidyne_web.blueprints.api import api_bp
    from euclidyne.euclidyne_web.blueprints.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def inject_template_globals() -> dict:
        hub_url = _normalize_base_url(app.config.get("AIX_HUB_URL", "/"))
        return {
            "aix_hub_url": hub_url,
            "aix_contact_url": _aix_page_url(hub_url, "/contact"),
            "aix_privacy_url": _aix_page_url(hub_url, "/privacy"),
            "aix_toc_url": _aix_page_url(hub_url, "/toc"),
            "app_display_name": str(app.config.get("APP_DISPLAY_NAME", "Euclidyne")),
            "app_tagline": str(
                app.config.get(
                    "APP_TAGLINE",
                    "Instrument-Lab Explorations into Euclid, Ratios, and Rhythm",
                )
            ),
            "top_nav_labs": top_nav_labs(),
        }

    return app
