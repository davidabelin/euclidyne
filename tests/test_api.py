from __future__ import annotations


def test_api_v1_euclid_still_returns_v2_page_shape(client):
    response = client.get("/api/v1/euclid?a=240&b=46")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["ok"] is True
    assert payload["lab"]["slug"] == "algorithm-explorer"
    assert payload["model"]["gcd"] == 2
    assert payload["model"]["continued_fraction"]["quotients"] == [5, 4, 1, 1, 2]


def test_api_v2_euclid_rejects_reversed_pair_with_swap_hint(client):
    response = client.get("/api/v2/euclid?a=46&b=240")
    payload = response.get_json()
    assert response.status_code == 400
    assert payload["ok"] is False
    assert payload["needs_swap"] is True
    assert payload["swap_params"] == {"a": 240, "b": 46}


def test_api_v2_centered_euclid_payload(client):
    response = client.get("/api/v2/centered-euclid?a=55&b=34")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["lab"]["slug"] == "centered-euclid-race"
    assert payload["model"]["comparison"]["winner"] == "centered"
    assert payload["model"]["comparison"]["saved_steps"] == 3


def test_api_v2_gear_ratio_payload(client):
    response = client.get("/api/v2/gear-ratio?target_num=360&target_den=77&max_teeth=60&stages=3")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["lab"]["slug"] == "gear-ratio-forge"
    assert payload["model"]["candidates"]["selected"]["kind"] == "compound"
    assert payload["model"]["candidates"]["compound"]["label"] == "45:11 x 8:7"


def test_api_v2_rational_sky_payload(client):
    response = client.get("/api/v2/rational-sky?max_den=8&p=5&q=8&view=ford")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["lab"]["slug"] == "rational-sky"
    assert payload["model"]["selected"]["label"] == "5/8"
    assert any(circle["is_selected"] for circle in payload["model"]["ford"]["circles"])


def test_api_v2_rational_sky_rejects_fraction_above_one_with_swap_hint(client):
    response = client.get("/api/v2/rational-sky?max_den=8&p=9&q=7&view=ford")
    payload = response.get_json()
    assert response.status_code == 400
    assert payload["ok"] is False
    assert payload["needs_swap"] is True
    assert payload["swap_params"] == {"max_den": 8, "p": 7, "q": 9, "view": "ford"}


def test_api_v2_modular_lock_payload(client):
    response = client.get("/api/v2/modular-lock?a=13&m=34")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["lab"]["slug"] == "modular-lock-lab"
    assert payload["model"]["inverse"] == 21
    assert payload["model"]["locked"] is False


def test_api_v2_rhythm_payload(client):
    response = client.get("/api/v2/rhythm?steps=13&pulses=5&rotation=2&bpm=110")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["lab"]["slug"] == "rhythm-sequencer"
    assert payload["model"]["notation"] == ".x..x..x.x..x"
    assert payload["model"]["hit_count"] == 5


def test_api_v2_meshing_payload(client):
    response = client.get("/api/v2/meshing?driver_teeth=24&follower_teeth=40&center_scale=1.05")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["lab"]["slug"] == "meshing-reality-check"
    assert payload["model"]["state"] == "looser"
    assert payload["model"]["ratio"] == {"numerator": 3, "denominator": 5, "decimal": 0.6}


def test_api_v2_quadratic_surd_payload(client):
    response = client.get("/api/v2/quadratic-surd?n=23&terms=12")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["lab"]["slug"] == "quadratic-surd-loop"
    assert payload["model"]["period"] == [1, 3, 1, 8]
    assert payload["model"]["pell_hint"] == {"x": 24, "y": 5}


def test_api_v2_quadratic_surd_validation_error(client):
    response = client.get("/api/v2/quadratic-surd?n=16&terms=12")
    payload = response.get_json()
    assert response.status_code == 400
    assert payload["ok"] is False
    assert payload["error"] == "Use a non-square integer so the continued fraction is periodic."
