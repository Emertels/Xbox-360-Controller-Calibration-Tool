# AGENTS.md — System Architecture & Engineering Guide for AI Agents and Developers

This document serves as the canonical engineering specification for autonomous AI agents, LLMs, and developers maintaining, debugging, testing, or extending the **Xbox 360 Controller Calibration Tool**.

---

## 📌 System Overview

- **Project Name:** Xbox 360 Controller Calibration Tool
- **Version:** 1.0.0 (Official Release)
- **Language:** Python 3.10+ (developed and validated on Python 3.12 64-bit on Windows 11)
- **UI Framework:** Standard Python `tkinter` + `ttk` (zero heavy external GUI dependencies like PyQt or Electron)
- **Hardware Interface:** Direct Windows XInput API via `ctypes` (`xinput1_4.dll` ➔ `xinput1_3.dll` ➔ `xinput9_1_0.dll`), with controller shutdown support via ordinal 103
- **Virtual Emulation:** `vgamepad` on top of the kernel-level `ViGEmBus` driver
- **Persistence:** Versioned atomic JSON profiles in local `profiles/` folder
- **Localization:** Comprehensive i18n engine in `i18n.py` supporting 10 languages (pt, en, es, fr, de, it, ja, zh, ru, ko) with instant runtime combobox switching
- **Hardware Supported:** Wireless Xbox 360 controllers (via PC USB Wireless Gaming Receiver, with or without affordable USB Play & Charge cables from AliExpress/Shopee/Amazon) and native wired USB Xbox 360 controllers (OEM or clones).

---

## ⚠️ Experimental Nature & Physical Limitations

This utility operates as a software-level calibration layer:
1. **Not 100% Perfect:** The software compensates for center offsets, electrical noise, and outer bounds by calculating mathematical offsets in real time. Minor rounding quirks or game-engine-specific polling thresholds may still occur.
2. **Does Not Replace Physical Repairs:** If an analog gimbal is physically shattered, return springs are detached, or the potentiometer carbon tracks are completely worn through, physical hardware maintenance is required (soldering fresh Alps 10kΩ potentiometers).

---

## 🎯 Architectural Rationale

1. **XInput Protocol is Read-Only:** Microsoft's XInput API exposes only read queries (`XInputGetState`) and rumble actuation (`XInputSetState`). The protocol contains no command to write deadzones or calibration offsets into the physical controller's internal MCU EEPROM.
2. **Wireless Receiver Abstracts USB Descriptors:** WebUSB and WebHID tools (e.g., DriftGuard) require direct raw USB endpoint descriptors of native wired controllers. On wireless setups, the receiver hardware abstracts and masks low-level firmware endpoints.
3. **Play & Charge Cable Only Carries Power:** The data lines (D+ and D-) are not wired to the MCU on wireless controllers; only 5V power rails connect to the battery charging circuit. Therefore, affordable USB Play & Charge cables provide continuous power while the wireless receiver handles input transmissions.
4. **Software Injection Bridge:** This tool runs a ~16ms/60fps polling loop, applies double-precision mathematical transformations, and injects clean gamepad states into an emulated virtual Xbox 360 device via ViGEmBus.

---

## 🏗️ Module Topology

```
C:\Projetos\Calibration_Controle_Xbox_360\
│
├── INICIAR_SEM_CMD.vbs         # Silent launcher via WScript (zero console window)
├── INICIAR.bat                 # Portable batch launcher with smart Python discovery
├── INSTALAR_DEPENDENCIAS.bat   # Portable pip dependency installer
├── main.py                     # Entry point, Tkinter GUI, 60fps render loop
├── i18n.py                     # Multilingual localization engine (10 native languages)
├── xinput_reader.py            # ctypes binding to native XInput DLLs (zero 3rd-party dependencies)
├── calibration.py              # Pure math pipeline: EMA filters, Hermite deadzone, curves, range
├── virtual_gamepad.py          # Resilient wrapper for vgamepad / ViGEmBus (graceful degradation)
├── profiles.py                 # Atomic JSON profile serialization
├── requirements.txt            # Optional external dependencies: vgamepad>=0.1.0
├── README.md                   # Documentation in Portuguese (PT-BR)
├── README.en.md                # Documentation in English (EN)
├── AGENTS.md                   # Engineering guide in Portuguese
├── AGENTS.en.md                # This file (Engineering guide in English)
└── profiles/                   # Directory where portable JSON calibration profiles reside
```

---

## 🔄 Data Flow per Frame (`App._tick` every ~16ms)

```
[Hardware XInput]
       │
       ▼
XInputReader.get_state(idx)
       │
       ├─► ControllerState (dataclass containing raw axes & button bitmask)
       │
       ▼
NoiseFilter.apply(raw_x, raw_y, strength, anti_jitter)
       │
       ├─► (filt_x, filt_y) [Attenuated signal via Exponential Moving Average]
       │
       ▼
apply_stick_calibration(filt_x, filt_y, stick_settings)
       │
       ├─ 1. Subtract center offset (median computed during Auto-Center)
       ├─ 2. Apply polarity inversion (invert_x, invert_y if toggled)
       ├─ 3. Calculate polar magnitude: r = sqrt(dx² + dy²)
       ├─ 4. Apply Smooth Hermite Radial Deadzone:
       │     If r <= deadzone: return (0, 0)
       │     If r < deadzone + transition: interpolate cubic Hermite: t = t*t*(3 - 2t)
       ├─ 5. Apply Selected Response Curve:
       │     Linear: y = x
       │     Smooth: y = x² (quadratic)
       │     Aggressive: y = sqrt(x)
       │     Extra Smooth: y = x³ (cubic)
       ├─ 6. Scale by Auto-Range factor and clamp inside [-32768, 32767]
       │
       ▼
apply_trigger_deadzone(raw_trigger, deadzone)
       │
       ▼
StickCanvas.update() / TriggerUnit.update() / ControllerPanel.update()  [Screen render]
       │
       ▼
VirtualGamepad.update(...)  [Inject packet into ViGEmBus driver for games]
```

---

## 📦 Component Implementation Details

### 1. `xinput_reader.py`
- **Purpose:** Read physical controller state without external library bloat.
- **Implementation:** Leverages `ctypes.WinDLL`, cascading through:
  1. `xinput1_4.dll` (Windows 8 / 10 / 11 native)
  2. `xinput1_3.dll` (DirectX June 2010 redist)
  3. `xinput9_1_0.dll` (Legacy Windows 7/Vista)
- **C Structs:**
  - `XINPUT_GAMEPAD`: mirrors C types (`wButtons` ushort, triggers ubyte, axes short).
  - `XINPUT_STATE`: wraps `dwPacketNumber` and the gamepad struct.
- **Key Methods:**
  - `find_connected_controller() -> int | None`: probes player slots 0 through 3.
  - `get_state(player_index: int) -> ControllerState`: queries state with sub-0.05ms overhead.
  - `power_off(controller_index: int) -> bool`: invokes undocumented XInput ordinal 103 to send radio power-off packets to wireless controllers.

### 2. `calibration.py`
- **Purpose:** Pure mathematical calibration logic decoupled from GUI state.
- **Data Structures:**
  - `StickCalibration`: dataclass holding `center_x`, `center_y`, `deadzone`, `range_scale`, `invert_x`, `invert_y`, `response_curve`, `noise_filter`, `anti_jitter`.
  - `CalibrationSettings`: bundles `left_stick`, `right_stick`, `left_trigger_deadzone`, `right_trigger_deadzone`.
  - `NoiseFilter`: stateful EMA filter with micro-jitter cutoff.
- **Key Functions:**
  - `apply_stick_calibration(raw_x, raw_y, cal) -> tuple[int, int]`: complete pipeline with smooth radial Hermite deadzone.
  - `apply_trigger_deadzone(raw, deadzone) -> int`: maps range `[deadzone, 255]` linearly to `[0, 255]`.

### 3. `i18n.py`
- **Purpose:** Centralized multilingual engine supporting 10 languages (`pt`, `en`, `es`, `fr`, `de`, `it`, `ja`, `zh`, `ru`, `ko`).
- **Key Functions:**
  - `T(key: str, **kwargs) -> str`: string retrieval with `.format()` parameter interpolation.
  - `set_language(lang: str) -> None`: updates active language.
  - `get_languages() -> list[tuple[str, str]]`: lists language codes and display names with flags.
  - `get_curve_labels()`, `curve_label_to_key()`, `curve_key_to_label()`: safe mapping between UI display strings and internal algorithmic identifiers.

### 4. `virtual_gamepad.py`
- **Purpose:** Provides virtual controller output via ViGEmBus.
- **Graceful Degradation:**
  - If `vgamepad` is missing, `VGAMEPAD_AVAILABLE = False`.
  - The tool launches cleanly in **diagnostic/monitor mode** without crashing.
  - The UI button displays a notification guiding the user to run `INSTALAR_DEPENDENCIAS.bat`.
- **Exception Interception:**
  - If `vgamepad` Python package exists but the ViGEmBus kernel driver is uninstalled, catches `RuntimeError` and displays direct download links.

### 5. `profiles.py`
- **Purpose:** JSON persistence of stick calibration and deadzone parameters.
- **Location:** Portable `profiles/` directory relative to script root.

### 6. `main.py`
- **Purpose:** Responsive Tkinter GUI with dark visual styling and live telemetry.
- **Custom Widgets:**
  - `StickCanvas`: polar radar displaying 25%, 50%, 75%, 100% circles, raw vector (red), and calibrated vector (green).
  - `TriggerUnit` / `TriggerBar`: pressure gauges (0-255 byte scale and percentage) with dedicated interactive `[ LT ]` and `[ RT ]` trigger buttons that illuminate and sink on squeeze.
  - `ControllerPanel`: unified dashboard reproducing physical Xbox 360 controller ergonomics: triggers/bumpers on top (`LT/LB` & `RT/RB`), center cluster (`Back`, `⨂ Xbox`, `Start`), left wing (`LS` & 4-way D-Pad cross), and right wing (diamond `ABXY` & `RS`).
  - `StickCalibrationPanel`: Auto-Center (median), Auto-Range (circular trajectory), fine sliders, and curve selector.
  - `TriggersTab`: trigger deadzones and response curve documentation.
  - `HelpTab`: Hall Effect vs. Potentiometer troubleshooting guide.
  - `VirtualGuideTab`: virtual gamepad usage tips and HidHide tutorial.

---

## 🛠️ Code Conventions & Guidelines

1. **Language Split:**
   - Code logic, class names, method signatures, variables, and docstrings: **English**.
   - User-facing UI labels and descriptions: **Delegated to `i18n.py` via `T("key")`**.
2. **Ranges & Formats:**
   - Analog sticks: signed 16-bit integer (`-32768` to `32767`), nominal resting center is `0`.
   - Triggers: unsigned 8-bit integer (`0` to `255`).
3. **Deadzone Geometry:**
   - **Always radial (polar)**, never axial/square. Axial deadzones warp diagonal trajectory in modern PC games.

---

## 🚀 Standalone Executable Packaging (`.exe`)

To package this application as a standalone executable without requiring Python on client machines:

1. Install PyInstaller:
   ```powershell
   py -3 -m pip install pyinstaller
   ```
2. Compile from script directory:
   ```powershell
   py -3 -m PyInstaller --onefile --noconsole --name "Xbox360_Calibration_Tool" main.py
   ```
3. Standalone binary output: `dist\Xbox360_Calibration_Tool.exe`.
