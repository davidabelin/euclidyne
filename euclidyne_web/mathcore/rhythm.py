"""Euclidean rhythm builders."""

from __future__ import annotations

from typing import Any


def _euclidean_pattern(steps: int, pulses: int) -> list[int]:
    bucket = 0
    pattern: list[int] = []
    for _ in range(steps):
        bucket += pulses
        if bucket >= steps:
            bucket -= steps
            pattern.append(1)
        else:
            pattern.append(0)
    return pattern


def _rotate_pattern(pattern: list[int], rotation: int) -> list[int]:
    if not pattern:
        return []
    amount = rotation % len(pattern)
    return pattern[-amount:] + pattern[:-amount] if amount else list(pattern)


def build_rhythm_model(steps: int, pulses: int, rotation: int, bpm: int) -> dict[str, Any]:
    """Build the Euclidean rhythm lab payload."""

    pattern = _rotate_pattern(_euclidean_pattern(steps, pulses), rotation)
    step_duration = round((4 * 60 / bpm) / steps, 6)
    events = [
        {
            "index": index,
            "active": bool(active),
            "angle_deg": round(index * (360 / steps), 4),
            "time_seconds": round(index * step_duration, 6),
            "label": "x" if active else ".",
        }
        for index, active in enumerate(pattern)
    ]
    return {
        "steps": steps,
        "pulses": pulses,
        "rotation": rotation % steps,
        "bpm": bpm,
        "pattern": pattern,
        "notation": "".join("x" if step else "." for step in pattern),
        "events": events,
        "hit_count": sum(pattern),
        "rest_count": steps - sum(pattern),
        "audio": {
            "step_duration": step_duration,
            "total_duration": round(step_duration * steps, 6),
        },
    }
