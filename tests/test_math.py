from __future__ import annotations

import math
import random

from euclidorithm.euclidyne_web.mathcore import build_euclid_model


def test_known_model_values():
    model = build_euclid_model(240, 46)
    assert model["gcd"] == 2
    assert model["step_count"] == 5
    assert model["continued_fraction"]["quotients"] == [5, 4, 1, 1, 2]
    assert model["bezout"]["x"] == -9
    assert model["bezout"]["y"] == 47
    assert model["bezout"]["inverse_mod_b"] is None


def test_modular_inverse_and_geometry_match_quotients():
    model = build_euclid_model(55, 34)
    assert model["gcd"] == 1
    assert model["bezout"]["inverse_mod_b"] == 13
    geometry_quotients = [stage["quotient"] for stage in model["geometry"]["stages"]]
    assert geometry_quotients == model["continued_fraction"]["quotients"]


def test_randomized_pairs_match_gcd_and_bezout_identity():
    rng = random.Random(7)
    for _ in range(20):
        a = rng.randint(5, 400)
        b = rng.randint(1, a)
        model = build_euclid_model(a, b)
        assert model["gcd"] == math.gcd(a, b)
        x = model["bezout"]["x"]
        y = model["bezout"]["y"]
        assert a * x + b * y == model["gcd"]

