"""
Virtual Gamepad (ViGEmBus)
==========================
Creates a virtual Xbox 360 controller that receives the calibrated values
and forwards them to Windows so that games see a perfectly calibrated pad.

Requires:
    - ``pip install vgamepad``
    - ViGEmBus driver installed (https://github.com/nefarius/ViGEmBus/releases)

If vgamepad is not installed the rest of the tool still works — only the
virtual-controller feature is disabled.

Author: Emerson Teles (projeto criado com auxílio do Antigravity)
License: MIT
"""

from __future__ import annotations

try:
    import vgamepad as vg

    VGAMEPAD_AVAILABLE = True
except ImportError:
    vg = None  # type: ignore[assignment]
    VGAMEPAD_AVAILABLE = False

from xinput_reader import (
    XINPUT_GAMEPAD_A,
    XINPUT_GAMEPAD_B,
    XINPUT_GAMEPAD_X,
    XINPUT_GAMEPAD_Y,
    XINPUT_GAMEPAD_DPAD_UP,
    XINPUT_GAMEPAD_DPAD_DOWN,
    XINPUT_GAMEPAD_DPAD_LEFT,
    XINPUT_GAMEPAD_DPAD_RIGHT,
    XINPUT_GAMEPAD_START,
    XINPUT_GAMEPAD_BACK,
    XINPUT_GAMEPAD_LEFT_SHOULDER,
    XINPUT_GAMEPAD_RIGHT_SHOULDER,
    XINPUT_GAMEPAD_LEFT_THUMB,
    XINPUT_GAMEPAD_RIGHT_THUMB,
    XINPUT_GAMEPAD_GUIDE,
    ControllerState,
)

# Lazy-initialised mapping from our XInput masks → vgamepad enum values.
_BUTTON_MAP: dict[int, object] | None = None


def _ensure_button_map() -> dict[int, object]:
    global _BUTTON_MAP
    if _BUTTON_MAP is not None:
        return _BUTTON_MAP

    if not VGAMEPAD_AVAILABLE:
        _BUTTON_MAP = {}
        return _BUTTON_MAP

    _BUTTON_MAP = {
        XINPUT_GAMEPAD_A: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
        XINPUT_GAMEPAD_B: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
        XINPUT_GAMEPAD_X: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
        XINPUT_GAMEPAD_Y: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        XINPUT_GAMEPAD_DPAD_UP: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
        XINPUT_GAMEPAD_DPAD_DOWN: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
        XINPUT_GAMEPAD_DPAD_LEFT: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
        XINPUT_GAMEPAD_DPAD_RIGHT: vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
        XINPUT_GAMEPAD_START: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
        XINPUT_GAMEPAD_BACK: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
        XINPUT_GAMEPAD_LEFT_SHOULDER: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
        XINPUT_GAMEPAD_RIGHT_SHOULDER: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
        XINPUT_GAMEPAD_LEFT_THUMB: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
        XINPUT_GAMEPAD_RIGHT_THUMB: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
        XINPUT_GAMEPAD_GUIDE: vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
    }
    return _BUTTON_MAP


class VirtualGamepad:
    """Manages a virtual Xbox 360 controller via the ViGEmBus driver."""

    def __init__(self) -> None:
        if not VGAMEPAD_AVAILABLE:
            raise RuntimeError(
                "A biblioteca 'vgamepad' não está instalada.\n"
                "Instale com:  pip install vgamepad\n"
                "E instale o driver ViGEmBus:\n"
                "  https://github.com/nefarius/ViGEmBus/releases"
            )
        self._gamepad: vg.VX360Gamepad | None = None
        self._active: bool = False

    # -- properties ----------------------------------------------------------
    @property
    def is_active(self) -> bool:
        return self._active

    # -- lifecycle -----------------------------------------------------------
    def activate(self) -> None:
        """Plug in the virtual controller."""
        if self._active:
            return
        try:
            self._gamepad = vg.VX360Gamepad()
            self._active = True
        except Exception as exc:
            raise RuntimeError(
                f"Não foi possível criar o controle virtual: {exc}\n"
                "Verifique se o ViGEmBus Driver está instalado:\n"
                "  https://github.com/nefarius/ViGEmBus/releases"
            ) from exc

    def deactivate(self) -> None:
        """Unplug the virtual controller, resetting all inputs first."""
        if not self._active:
            return
        try:
            if self._gamepad is not None:
                self._gamepad.reset()
                self._gamepad.update()
        except Exception:
            pass
        finally:
            self._gamepad = None
            self._active = False

    # -- update --------------------------------------------------------------
    def update(
        self,
        state: ControllerState,
        cal_lx: int,
        cal_ly: int,
        cal_rx: int,
        cal_ry: int,
        cal_lt: int,
        cal_rt: int,
    ) -> None:
        """Push a full frame of calibrated input to the virtual pad.

        Args:
            state:  Raw ``ControllerState`` (used for button pass-through).
            cal_lx: Calibrated left-stick X  (−32 768 … 32 767).
            cal_ly: Calibrated left-stick Y  (−32 768 … 32 767).
            cal_rx: Calibrated right-stick X (−32 768 … 32 767).
            cal_ry: Calibrated right-stick Y (−32 768 … 32 767).
            cal_lt: Calibrated left trigger   (0 … 255).
            cal_rt: Calibrated right trigger  (0 … 255).
        """
        if not self._active or self._gamepad is None:
            return

        gp = self._gamepad
        gp.reset()

        # Buttons (pass-through from physical controller)
        btn_map = _ensure_button_map()
        for xinput_mask, vg_button in btn_map.items():
            if state.buttons & xinput_mask:
                gp.press_button(button=vg_button)

        # Sticks
        gp.left_joystick(x_value=cal_lx, y_value=cal_ly)
        gp.right_joystick(x_value=cal_rx, y_value=cal_ry)

        # Triggers
        gp.left_trigger(value=cal_lt)
        gp.right_trigger(value=cal_rt)

        gp.update()
