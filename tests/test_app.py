from __future__ import annotations

from urllib.parse import parse_qs, urlencode, urlsplit

import pytest

from euclidyne.euclidyne_web.lab_registry import LAB_ENTRIES


def test_primary_pages_load(client):
    cases = [
        ("/", b"Euclidyne"),
        ("/atlas", b"Core Algorithm"),
        ("/references", b"Claim Register"),
        ("/healthz", b'"status":"ok"'),
    ]
    for path, marker in cases:
        response = client.get(path)
        assert response.status_code == 200
        assert marker in response.data


def test_all_lab_pages_load_with_default_inputs(client):
    for lab in LAB_ENTRIES:
        query = urlencode(lab.default_inputs)
        response = client.get(f"{lab.route}?{query}")
        assert response.status_code == 200
        assert lab.title.encode() in response.data


@pytest.mark.parametrize(
    ("path", "marker"),
    [
        ("/quick?a=987&b=610", b"Quick Calculator"),
        ("/explorer?a=987&b=610", b"Algorithm Explorer"),
        ("/rectangle-reactor?a=144&b=89", b"Rectangle Reactor"),
        ("/gear-ratio-forge?target_num=360&target_den=77&max_teeth=60&stages=3", b"Gear Ratio Forge"),
        ("/fibonacci-race?a=34&b=21", b"Fibonacci Race"),
        ("/rational-sky?max_den=10&p=3&q=7&view=ford", b"Rational Sky"),
        ("/modular-lock-lab?a=11&m=26", b"Modular Lock Lab"),
        ("/rhythm-sequencer?steps=13&pulses=5&rotation=2&bpm=110", b"Rhythm Sequencer"),
        ("/centered-euclid-race?a=55&b=34", b"Centered Euclid Race"),
        ("/meshing-reality-check?driver_teeth=24&follower_teeth=40&center_scale=1.05", b"Meshing Reality Check"),
        ("/quadratic-surd-loop?n=23&terms=12", b"Quadratic Surd Loop"),
    ],
)
def test_lab_pages_load_with_non_default_inputs(client, path, marker):
    response = client.get(path)
    assert response.status_code == 200
    assert marker in response.data


def test_invalid_lab_inputs_render_error_state_instead_of_500(client):
    response = client.get("/quadratic-surd-loop?n=16&terms=12")
    assert response.status_code == 200
    assert b"Use a non-square integer so the continued fraction is periodic." in response.data

    response = client.get("/quick?a=bad&b=46")
    assert response.status_code == 200
    assert b"Use an integer value for a." in response.data


def test_aix_chrome_uses_updated_label_and_copyleft_marker(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"AIX Labs" in response.data
    assert b"&#x1F12F;" in response.data
    assert b"2026 AIX Protodyne" in response.data


def test_legacy_routes_redirect_to_new_pages(client):
    cases = [
        ("/table?a=240&b=46", "/explorer?a=240&b=46"),
        ("/extended?a=240&b=46", "/explorer?a=240&b=46"),
        ("/wp?a=240&b=46", "/explorer?a=240&b=46"),
        ("/continued-fractions?a=55&b=34", "/rectangle-reactor?a=55&b=34"),
        ("/phase?target_num=355&target_den=113", "/gear-ratio-forge?target_num=355&target_den=113"),
        ("/gear?driver_teeth=24&follower_teeth=40", "/meshing-reality-check?driver_teeth=24&follower_teeth=40"),
        ("/lock?a=13&m=34", "/modular-lock-lab?a=13&m=34"),
    ]
    for source, target in cases:
        response = client.get(source, follow_redirects=False)
        assert response.status_code == 302
        location = urlsplit(response.headers["Location"])
        expected = urlsplit(target)
        assert location.path == expected.path
        assert parse_qs(location.query) == parse_qs(expected.query)
