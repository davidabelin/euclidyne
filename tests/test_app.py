from __future__ import annotations

from euclidorithm.euclidyne import app


def test_primary_pages_load():
    client = app.test_client()
    cases = [
        ("/", b"Euclidyne"),
        ("/quick?a=12082&b=5280", b"Quick Calculator"),
        ("/explorer?a=240&b=46", b"Algorithm Explorer"),
        ("/continued-fractions?a=55&b=34", b"Continued Fractions + Geometry"),
        ("/phase?a=55&b=34", b"Phase Lab"),
        ("/references", b"Claim Register"),
        ("/healthz", b'"status":"ok"'),
    ]
    for path, marker in cases:
        response = client.get(path)
        assert response.status_code == 200
        assert marker in response.data


def test_api_returns_canonical_model():
    client = app.test_client()
    response = client.get("/api/v1/euclid?a=240&b=46")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["ok"] is True
    assert payload["gcd"] == 2
    assert payload["continued_fraction"]["quotients"] == [5, 4, 1, 1, 2]


def test_api_rejects_reversed_pair_with_swap_hint():
    client = app.test_client()
    response = client.get("/api/v1/euclid?a=46&b=240")
    payload = response.get_json()
    assert response.status_code == 400
    assert payload["needs_swap"] is True
    assert payload["swap_pair"] == {"a": 240, "b": 46}


def test_legacy_routes_redirect_to_new_pages():
    client = app.test_client()
    response = client.get("/table?a=240&b=46", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/explorer?a=240&b=46")

    response = client.get("/gear?a=55&b=34", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/phase?a=55&b=34")
