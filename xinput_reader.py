"""
Xbox 360 Controller XInput Reader
==================================
Reads raw analog stick, trigger, and button values via Windows XInput API.
Uses ctypes to interface directly with the Windows XInput DLL — no external
dependencies required.

Author: Emerson Teles (projeto criado com auxílio do Antigravity)
License: MIT
"""

import ctypes
from ctypes import Structure, c_ushort, c_short, c_ubyte, c_uint, byref
from dataclasses import dataclass
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
XINPUT_MAX_CONTROLLERS = 4
ERROR_SUCCESS = 0
ERROR_DEVICE_NOT_CONNECTED = 1167

# Button bitmasks (XINPUT_GAMEPAD.wButtons)
XINPUT_GAMEPAD_DPAD_UP = 0x0001
XINPUT_GAMEPAD_DPAD_DOWN = 0x0002
XINPUT_GAMEPAD_DPAD_LEFT = 0x0004
XINPUT_GAMEPAD_DPAD_RIGHT = 0x0008
XINPUT_GAMEPAD_START = 0x0010
XINPUT_GAMEPAD_BACK = 0x0020
XINPUT_GAMEPAD_LEFT_THUMB = 0x0040
XINPUT_GAMEPAD_RIGHT_THUMB = 0x0080
XINPUT_GAMEPAD_LEFT_SHOULDER = 0x0100
XINPUT_GAMEPAD_RIGHT_SHOULDER = 0x0200
XINPUT_GAMEPAD_GUIDE = 0x0400
XINPUT_GAMEPAD_A = 0x1000
XINPUT_GAMEPAD_B = 0x2000
XINPUT_GAMEPAD_X = 0x4000
XINPUT_GAMEPAD_Y = 0x8000

ALL_BUTTONS = {
    "A": XINPUT_GAMEPAD_A,
    "B": XINPUT_GAMEPAD_B,
    "X": XINPUT_GAMEPAD_X,
    "Y": XINPUT_GAMEPAD_Y,
    "DPad Up": XINPUT_GAMEPAD_DPAD_UP,
    "DPad Down": XINPUT_GAMEPAD_DPAD_DOWN,
    "DPad Left": XINPUT_GAMEPAD_DPAD_LEFT,
    "DPad Right": XINPUT_GAMEPAD_DPAD_RIGHT,
    "Start": XINPUT_GAMEPAD_START,
    "Back": XINPUT_GAMEPAD_BACK,
    "LB": XINPUT_GAMEPAD_LEFT_SHOULDER,
    "RB": XINPUT_GAMEPAD_RIGHT_SHOULDER,
    "LS": XINPUT_GAMEPAD_LEFT_THUMB,
    "RS": XINPUT_GAMEPAD_RIGHT_THUMB,
    "Guide": XINPUT_GAMEPAD_GUIDE,
}


# ---------------------------------------------------------------------------
# ctypes structures — mirrors the C structs from XInput.h
# ---------------------------------------------------------------------------
class XINPUT_GAMEPAD(Structure):
    _fields_ = [
        ("wButtons", c_ushort),
        ("bLeftTrigger", c_ubyte),
        ("bRightTrigger", c_ubyte),
        ("sThumbLX", c_short),
        ("sThumbLY", c_short),
        ("sThumbRX", c_short),
        ("sThumbRY", c_short),
    ]


class XINPUT_STATE(Structure):
    _fields_ = [
        ("dwPacketNumber", c_uint),
        ("Gamepad", XINPUT_GAMEPAD),
    ]


# ---------------------------------------------------------------------------
# Parsed controller state (nice Python dataclass)
# ---------------------------------------------------------------------------
@dataclass
class ControllerState:
    """Parsed controller state with convenience properties."""

    connected: bool = False

    # Analog sticks (signed 16-bit: −32 768 … 32 767)
    left_stick_x: int = 0
    left_stick_y: int = 0
    right_stick_x: int = 0
    right_stick_y: int = 0

    # Triggers (unsigned 8-bit: 0 … 255)
    left_trigger: int = 0
    right_trigger: int = 0

    # Raw button bitmask
    buttons: int = 0

    # Packet number (useful for detecting state changes)
    packet_number: int = 0

    # ---- helpers ---------------------------------------------------------
    def is_button_pressed(self, button_mask: int) -> bool:
        return bool(self.buttons & button_mask)

    @property
    def button_a(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_A)

    @property
    def button_b(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_B)

    @property
    def button_x(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_X)

    @property
    def button_y(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_Y)

    @property
    def dpad_up(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_DPAD_UP)

    @property
    def dpad_down(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_DPAD_DOWN)

    @property
    def dpad_left(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_DPAD_LEFT)

    @property
    def dpad_right(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_DPAD_RIGHT)

    @property
    def start(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_START)

    @property
    def back(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_BACK)

    @property
    def left_shoulder(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_LEFT_SHOULDER)

    @property
    def right_shoulder(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_RIGHT_SHOULDER)

    @property
    def left_thumb(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_LEFT_THUMB)

    @property
    def right_thumb(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_RIGHT_THUMB)

    @property
    def guide(self) -> bool:
        return self.is_button_pressed(XINPUT_GAMEPAD_GUIDE)

    def get_pressed_buttons(self) -> list[str]:
        """Return a list of names of all currently pressed buttons."""
        return [
            name for name, mask in ALL_BUTTONS.items()
            if self.is_button_pressed(mask)
        ]


# ---------------------------------------------------------------------------
# XInput reader class
# ---------------------------------------------------------------------------
class XInputReader:
    """Reads Xbox 360 controller state via Windows XInput API (ctypes)."""

    def __init__(self):
        # Try DLLs in order of preference (1_4 ships with Win 8+)
        self._xinput = None
        for dll_name in ("xinput1_4", "xinput1_3", "xinput9_1_0"):
            try:
                self._xinput = ctypes.windll.LoadLibrary(dll_name)
                self._dll_name = dll_name
                break
            except OSError:
                continue

        if self._xinput is None:
            raise RuntimeError(
                "Não foi possível carregar nenhuma DLL do XInput.\n"
                "Verifique se você está rodando no Windows e se os drivers "
                "do Xbox 360 estão instalados."
            )

        # Set up function signatures
        self._xinput.XInputGetState.argtypes = [c_uint, ctypes.POINTER(XINPUT_STATE)]
        self._xinput.XInputGetState.restype = c_uint

    @property
    def dll_name(self) -> str:
        """Name of the loaded XInput DLL."""
        return self._dll_name

    def get_state(self, controller_index: int = 0) -> ControllerState:
        """Read the current state of a controller.

        Args:
            controller_index: Controller index (0–3).

        Returns:
            ``ControllerState`` with current raw values.
        """
        if not 0 <= controller_index < XINPUT_MAX_CONTROLLERS:
            raise ValueError(
                f"Índice do controle deve ser 0–{XINPUT_MAX_CONTROLLERS - 1}, "
                f"recebido: {controller_index}"
            )

        state = XINPUT_STATE()
        result = self._xinput.XInputGetState(controller_index, byref(state))

        if result != ERROR_SUCCESS:
            return ControllerState(connected=False)

        gp = state.Gamepad
        return ControllerState(
            connected=True,
            left_stick_x=gp.sThumbLX,
            left_stick_y=gp.sThumbLY,
            right_stick_x=gp.sThumbRX,
            right_stick_y=gp.sThumbRY,
            left_trigger=gp.bLeftTrigger,
            right_trigger=gp.bRightTrigger,
            buttons=gp.wButtons,
            packet_number=state.dwPacketNumber,
        )

    def power_off(self, controller_index: int = 0) -> bool:
        """Send power-off signal to an Xbox 360 wireless controller using XInput ordinal 103.

        Returns True if successful, False otherwise.
        """
        try:
            power_off_func = self._xinput[103]
            power_off_func.argtypes = [c_uint]
            power_off_func.restype = c_uint
            res = power_off_func(controller_index)
            return res == ERROR_SUCCESS
        except Exception:
            return False

    def find_connected_controller(self) -> Optional[int]:
        """Return the index of the first connected controller, or *None*."""
        for i in range(XINPUT_MAX_CONTROLLERS):
            if self.get_state(i).connected:
                return i
        return None
