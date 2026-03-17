from __future__ import annotations

import math
import random

from euclidyne.euclidyne_web.mathcore import (
    build_centered_euclid_model,
    build_euclid_model,
    build_fibonacci_comparison,
    build_gear_ratio_model,
    build_meshing_model,
    build_quadratic_surd_model,
    build_rational_sky_model,
    build_rectangle_model,
    build_rhythm_model,
)


def test_known_euclid_model_values():
    model = build_euclid_model(240, 46)
    assert model["gcd"] == 2
    assert model["step_count"] == 5
    assert model["continued_fraction"]["quotients"] == [5, 4, 1, 1, 2]
    assert model["bezout"]["x"] == -9
    assert model["bezout"]["y"] == 47
    assert model["bezout"]["inverse_mod_b"] is None
    assert model["phase"]["remainder"] == 10


def test_rectangle_model_matches_euclid_quotients_and_flags_golden_case():
    euclid = build_euclid_model(55, 34)
    rectangle = build_rectangle_model(55, 34)
    geometry_quotients = [stage["quotient"] for stage in rectangle["stages"]]
    assert geometry_quotients == euclid["continued_fraction"]["quotients"]
    assert rectangle["golden_special"]["enabled"] is True


def test_centered_euclid_can_save_steps_on_fibonacci_pair():
    model = build_centered_euclid_model(55, 34)
    assert model["gcd"] == 1
    assert model["standard"]["step_count"] == 8
    assert model["centered"]["step_count"] == 5
    assert model["comparison"]["saved_steps"] == 3
    assert model["comparison"]["winner"] == "centered"


def test_fibonacci_comparison_uses_a_worst_case_benchmark():
    model = build_fibonacci_comparison(55, 34)
    assert model["actual"]["properties"]["fibonacci_pair"] is True
    assert model["benchmark"]["properties"]["fibonacci_pair"] is True
    assert model["comparison"]["benchmark_steps"] >= model["comparison"]["actual_steps"]


def test_gear_ratio_model_exposes_simple_and_compound_candidates():
    model = build_gear_ratio_model(360, 77, 60, 3)
    assert model["continued_fraction"]["quotients"] == [4, 1, 2, 12, 2]
    assert model["candidates"]["selected"]["kind"] == "compound"
    assert model["candidates"]["compound"]["label"] == "45:11 x 8:7"
    assert model["candidates"]["compound"]["exact"] is True


def test_rational_sky_marks_visible_points_and_stern_brocot_moves():
    model = build_rational_sky_model(8, 5, 8, "ford")
    assert model["selected"]["label"] == "5/8"
    assert any(point["visible"] for point in model["orchard"]["points"])
    assert any(circle["is_selected"] for circle in model["ford"]["circles"])
    assert model["stern_brocot"]["moves"] == "LRLR"


def test_rhythm_model_counts_hits_and_rotation():
    model = build_rhythm_model(13, 5, 2, 110)
    assert model["notation"] == ".x..x..x.x..x"
    assert model["hit_count"] == 5
    assert model["rest_count"] == 8
    assert model["events"][1]["active"] is True


def test_meshing_model_keeps_ratio_constant_while_pressure_angle_moves():
    model = build_meshing_model(24, 40, 1.05)
    assert model["ratio"] == {"numerator": 3, "denominator": 5, "decimal": 0.6}
    assert model["state"] == "looser"
    assert model["pressure_angle"]["working_deg"] > model["pressure_angle"]["standard_deg"]


def test_quadratic_surd_model_has_period_and_pell_hint():
    model = build_quadratic_surd_model(23, 12)
    assert model["notation"] == "[4; (1, 3, 1, 8)]"
    assert model["period"] == [1, 3, 1, 8]
    assert model["period_length"] == 4
    assert model["pell_hint"] == {"x": 24, "y": 5}


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
