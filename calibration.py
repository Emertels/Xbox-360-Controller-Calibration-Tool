"""
Calibration Logic (v2)
======================
Handles center offset correction, radial deadzone with smooth transition,
range scaling, response curves, and noise filtering for Xbox 360 analog
sticks and triggers.

Pipeline per stick:

    raw → noise filter → subtract center → invert → smooth deadzone → response curve → scale → clamp

New in v2:
  - Smooth deadzone (no "jump" at boundary)
  - Response curves (linear, smooth, aggressive)
  - Noise filter (exponential moving average)
  - Per-axis range info

Author: Emerson Teles (projeto criado com auxilio do Antigravity)
License: MIT
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum

# Full range of a signed 16-bit axis
STICK_MAX = 32767
STICK_MIN = -32768


class ResponseCurve(Enum):
    """How stick displacement maps to output."""
    LINEAR = "linear"          # 1:1 — raw proportional
    SMOOTH = "smooth"          # Quadratic — gentle near center, fast at edges
    AGGRESSIVE = "aggressive"  # Square root — fast near center, slow at edges
    EXTRA_SMOOTH = "extra_smooth"  # Cubic — very gentle near center


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class StickCalibration:
    """Calibration parameters for a single analog stick."""

    # Center offset — the raw (X, Y) reading when the stick is at rest.
    center_x: float = 0.0
    center_y: float = 0.0

    # Inner deadzone as a percentage of the full range (0–50).
    deadzone: float = 5.0

    # Maximum range the stick physically reaches, as a percentage of the
    # theoretical maximum (50–150).
    range_scale: float = 100.0

    # Axis inversion flags.
    invert_x: bool = False
    invert_y: bool = False

    # Response curve type.
    response_curve: str = "linear"

    # Noise filter strength (0.0 = no filter, 1.0 = maximum smoothing).
    # Recommended: 0.15 for pots, 0.05 for Hall Effect.
    noise_filter: float = 0.15

    # Anti-jitter threshold — raw axis changes smaller than this are ignored.
    anti_jitter: int = 80


@dataclass
class CalibrationSettings:
    """Complete calibration settings for a controller."""

    left_stick: StickCalibration = field(default_factory=StickCalibration)
    right_stick: StickCalibration = field(default_factory=StickCalibration)

    # Trigger deadzones (0–255 scale)
    left_trigger_deadzone: int = 0
    right_trigger_deadzone: int = 0

    # -- serialisation -------------------------------------------------------
    def to_dict(self) -> dict:
        def _stick(s: StickCalibration) -> dict:
            return {
                "center_x": round(s.center_x, 2),
                "center_y": round(s.center_y, 2),
                "deadzone": round(s.deadzone, 2),
                "range_scale": round(s.range_scale, 2),
                "invert_x": s.invert_x,
                "invert_y": s.invert_y,
                "response_curve": s.response_curve,
                "noise_filter": round(s.noise_filter, 3),
                "anti_jitter": s.anti_jitter,
            }
        return {
            "left_stick": _stick(self.left_stick),
            "right_stick": _stick(self.right_stick),
            "left_trigger_deadzone": self.left_trigger_deadzone,
            "right_trigger_deadzone": self.right_trigger_deadzone,
        }

    @classmethod
    def from_dict(cls, data: dict) -> CalibrationSettings:
        def _stick(d: dict) -> StickCalibration:
            return StickCalibration(
                center_x=d.get("center_x", 0.0),
                center_y=d.get("center_y", 0.0),
                deadzone=d.get("deadzone", 5.0),
                range_scale=d.get("range_scale", 100.0),
                invert_x=d.get("invert_x", False),
                invert_y=d.get("invert_y", False),
                response_curve=d.get("response_curve", "linear"),
                noise_filter=d.get("noise_filter", 0.15),
                anti_jitter=d.get("anti_jitter", 80),
            )
        settings = cls()
        if "left_stick" in data:
            settings.left_stick = _stick(data["left_stick"])
        if "right_stick" in data:
            settings.right_stick = _stick(data["right_stick"])
        settings.left_trigger_deadzone = data.get("left_trigger_deadzone", 0)
        settings.right_trigger_deadzone = data.get("right_trigger_deadzone", 0)
        return settings


# ---------------------------------------------------------------------------
# Noise filter (exponential moving average)
# ---------------------------------------------------------------------------
class NoiseFilter:
    """Exponential moving average filter for reducing analog stick jitter.

    Lower alpha = more smoothing (more lag).
    Higher alpha = less smoothing (more responsive).
    """

    def __init__(self) -> None:
        self._prev_x: float | None = None
        self._prev_y: float | None = None

    def apply(self, raw_x: int, raw_y: int, strength: float, anti_jitter: int) -> tuple[int, int]:
        """Filter raw values. strength is 0.0 (no filter) to 1.0 (max smooth)."""
        if strength <= 0.001:
            self._prev_x = float(raw_x)
            self._prev_y = float(raw_y)
            return (raw_x, raw_y)

        # Alpha: low strength → alpha close to 1 (responsive)
        #        high strength → alpha close to 0 (smooth)
        alpha = max(0.05, 1.0 - strength)

        if self._prev_x is None:
            self._prev_x = float(raw_x)
            self._prev_y = float(raw_y)
            return (raw_x, raw_y)

        # Anti-jitter: ignore tiny changes
        dx = abs(raw_x - self._prev_x)
        dy = abs(raw_y - self._prev_y)

        if dx < anti_jitter and dy < anti_jitter:
            # Movement too small — keep previous value (eliminates jitter)
            return (int(round(self._prev_x)), int(round(self._prev_y)))

        # Apply EMA
        self._prev_x = alpha * raw_x + (1.0 - alpha) * self._prev_x
        self._prev_y = alpha * raw_y + (1.0 - alpha) * self._prev_y

        return (int(round(self._prev_x)), int(round(self._prev_y)))

    def reset(self) -> None:
        self._prev_x = None
        self._prev_y = None


# ---------------------------------------------------------------------------
# Response curves
# ---------------------------------------------------------------------------
def _apply_response_curve(normalized: float, curve: str) -> float:
    """Apply a response curve to a normalized [0, 1] magnitude.

    Args:
        normalized: Input magnitude from 0.0 to 1.0.
        curve:      One of 'linear', 'smooth', 'aggressive', 'extra_smooth'.

    Returns:
        Transformed magnitude from 0.0 to 1.0.
    """
    if curve == "smooth":
        # Quadratic — gentle near center, accelerates toward edge
        return normalized * normalized
    elif curve == "aggressive":
        # Square root — fast response near center
        return math.sqrt(normalized)
    elif curve == "extra_smooth":
        # Cubic — very gentle near center
        return normalized * normalized * normalized
    else:  # linear
        return normalized


# ---------------------------------------------------------------------------
# Core calibration functions
# ---------------------------------------------------------------------------
def apply_stick_calibration(
    raw_x: int,
    raw_y: int,
    cal: StickCalibration,
) -> tuple[int, int]:
    """Apply the full calibration pipeline to a pair of raw stick readings.

    Pipeline:
        raw → subtract center → invert → smooth radial deadzone →
        response curve → scale → clamp

    Args:
        raw_x: Raw X-axis value (−32 768 … 32 767).
        raw_y: Raw Y-axis value (−32 768 … 32 767).
        cal:   Calibration parameters to apply.

    Returns:
        ``(calibrated_x, calibrated_y)`` clamped to −32 768 … 32 767.
    """
    # 1) Subtract center offset
    cx = raw_x - cal.center_x
    cy = raw_y - cal.center_y

    # 2) Optional axis inversion
    if cal.invert_x:
        cx = -cx
    if cal.invert_y:
        cy = -cy

    # 3) Compute polar magnitude
    magnitude = math.hypot(cx, cy)
    if magnitude < 0.001:
        return (0, 0)

    # Unit direction
    nx = cx / magnitude
    ny = cy / magnitude

    # 4) Smooth radial deadzone
    deadzone_abs = (cal.deadzone / 100.0) * STICK_MAX
    max_range = STICK_MAX * (cal.range_scale / 100.0)
    magnitude = min(magnitude, max_range)

    if magnitude <= deadzone_abs:
        return (0, 0)

    # Smooth transition zone (10% of deadzone width, min 50 units)
    # This prevents the "jump" when exiting the deadzone
    transition = max(50.0, deadzone_abs * 0.1)
    effective = max_range - deadzone_abs
    if effective < 1.0:
        effective = 1.0

    # Remap [deadzone, max_range] → [0, 1]
    normalized = (magnitude - deadzone_abs) / effective
    normalized = max(0.0, min(1.0, normalized))

    # Smooth ramp at the deadzone boundary
    if magnitude < deadzone_abs + transition and transition > 0:
        t = (magnitude - deadzone_abs) / transition
        # Smooth step (Hermite interpolation)
        t = t * t * (3.0 - 2.0 * t)
        normalized *= t

    # 5) Apply response curve
    normalized = _apply_response_curve(normalized, cal.response_curve)

    # 6) Scale back to integer range
    scaled = normalized * STICK_MAX

    out_x = int(round(nx * scaled))
    out_y = int(round(ny * scaled))
    out_x = max(STICK_MIN, min(STICK_MAX, out_x))
    out_y = max(STICK_MIN, min(STICK_MAX, out_y))

    return (out_x, out_y)


def apply_trigger_deadzone(raw_value: int, deadzone: int) -> int:
    """Apply a simple deadzone to a trigger reading.

    Args:
        raw_value: Raw trigger value (0–255).
        deadzone:  Deadzone threshold (0–255).

    Returns:
        Calibrated trigger value remapped to 0–255.
    """
    if raw_value <= deadzone:
        return 0
    effective = 255 - deadzone
    if effective < 1:
        return 255
    return max(0, min(255, int(((raw_value - deadzone) / effective) * 255)))
