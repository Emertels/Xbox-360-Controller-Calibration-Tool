# 🎮 Xbox 360 Controller Calibration Tool (v1.0.0)

[![Português](https://img.shields.io/badge/Idioma-Portugu%C3%AAs_(Brasil)-green.svg)](README.md)
[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.en.md)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows_10%2F11-0078D6?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e)
![Version](https://img.shields.io/badge/Version-1.0.0_Official-blueviolet)

Professional, lightweight, and open-source software calibration tool for **Xbox 360** analog sticks, pressure triggers, and buttons on Windows.

Specifically engineered to fix center offsets, stick drift, and DIY component replacements (aftermarket analog sticks, soldering offset, residual drift, or retrofits).

---

> [!WARNING]
> ### ⚠️ Important Notice: Experimental Tool & Precision Disclaimer
> This tool is an **experimental, open-source software project created for the community**.
> - **Not 100% Perfect:** Operating via real-time software mathematical emulation (Windows XInput and ViGEmBus), slight rounding differences, game-specific deadzone engine quirks, or edge-case deviations may occur.
> - **Physical Limitations:** While this tool compensates for stick drift, electrical noise, and center offsets through software, **it cannot physically repair broken hardware**. If a mechanical return spring is broken, a gimbal axis is physically loose, or the potentiometer carbon track is completely stripped, physical repair or component replacement is still required.

> [!TIP]
> ### 🔌 USB Cable & Play & Charge Kit Compatibility (AliExpress / Shopee / Amazon)
> You can easily use your controller with affordable USB cables:
> - **Wireless Controller with Play & Charge Cable:** Works seamlessly powered by a standard **USB Play & Charge cable** (the affordable kit widely available on **AliExpress, Shopee, Amazon, or eBay**). The cable supplies continuous 5V power to the controller battery compartment, allowing you to play continuously on PC without draining disposable AA batteries. Gameplay inputs are transmitted wirelessly to your **PC Wireless Gaming Receiver** (original Microsoft or compatible clone from AliExpress).
> - **Native Wired USB Controllers (OEM or AliExpress Clones):** Controllers with an integrated native USB cable (whether official Microsoft OEM or budget third-party clones from AliExpress) connect directly and are recognized immediately by the Windows standard XInput driver.

---

## 📋 Table of Contents

1. [The Problem: Why does this tool exist?](#-the-problem-why-does-this-tool-exist)
2. [Architecture & How It Works](#-architecture--how-it-works)
3. [Key Features (v1.0.0)](#-key-features-v100)
4. [Technical Diagnosis: Hall Effect vs. Potentiometers on Xbox 360](#-technical-diagnosis-hall-effect-vs-potentiometers-on-xbox-360)
5. [Prerequisites & Quick Setup](#-prerequisites--quick-setup)
6. [Step-by-Step Usage Guide](#-step-by-step-usage-guide)
7. [Pro Tip: How to Prevent Duplicate Controller Input with HidHide](#-pro-tip-how-to-prevent-duplicate-controller-input-with-hidhide)
8. [Repository Structure](#-repository-structure)
9. [Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
10. [Useful References & Links](#-useful-references--links)
11. [License & Credits](#-license--credits)

---

## 🧐 The Problem: Why does this tool exist?

The **Xbox 360 controller** (especially the wireless model paired with the PC Wireless Gaming Receiver) is one of the most iconic gamepads in gaming history, but faces severe modern software limitations:

- ❌ **No native calibration in modern Windows:** The official *Xbox Accessories* app only supports Xbox One and Xbox Series X|S controllers. The Xbox 360 was phased out with zero factory software calibration tools on modern Windows.
- ❌ **The XInput API is Read-Only:** The standard Windows XInput API allows reading axis states and setting rumble motors, but **provides no command to write or flash calibration offsets onto the controller hardware MCU**.
- ❌ **DriftGuard and WebHID tools do not support the Wireless Receiver:** Web browser tools require direct WebUSB communication with the gamepad microcontroller. When paired via a PC wireless gaming receiver, the receiver chip abstracts low-level descriptors.
- ❌ **The Play & Charge cable only transfers power:** The wireless Xbox 360 Play & Charge cable only carries 5V power wires to recharge the battery pack. Input commands are always transmitted over the 2.4 GHz wireless radio.

### The Solution: Real-Time Software Layer Calibration
This tool acts as a transparent, ultra-fast calibration bridge: it reads raw stick coordinates with maximum precision via `ctypes` directly from native Windows DLLs (`xinput1_4.dll`), processes the signals through a multi-stage mathematical pipeline, and feeds the corrected state to a clean virtual Xbox 360 controller (via ViGEmBus) recognized natively by all PC games (Steam, Epic, Game Pass, emulators, etc.).

---

## ⚙️ Architecture & How It Works

```
┌──────────────────────────────────────┐
│  🎮 Physical Controller              │
│  Xbox 360 Wireless / USB             │
│  (Wireless Receiver / AliExpress USB)│
└──────────────────┬───────────────────┘
                   │ 1. Raw read (~0.1ms via ctypes -> xinput1_4.dll)
                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  📊 Calibration Tool (Python 3.10+ + Tkinter / ~60-120 FPS)                 │
│                                                                             │
│  [Per-Stick Mathematical Pipeline]:                                         │
│   Raw Signal ➔ Anti-Noise Filter (EMA) ➔ Anti-Jitter Filter                 │
│   ➔ Center Subtraction (Median) ➔ Axis Inversion (X/Y)                      │
│   ➔ Smooth Radial Deadzone (Hermite) ➔ Response Curve (Linear/Smooth)       │
│   ➔ Outer Boundary Scaling (Auto-Range) ➔ Safe Clamping & Guard             │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ 2. Corrected state injection
                                       ▼
                         ┌───────────────────────────┐
                         │  🕹️ Virtual Gamepad       │
                         │  Xbox 360 (ViGEmBus)      │
                         └─────────────┬─────────────┘
                                       │ 3. Clean input device
                                       ▼
                         ┌───────────────────────────┐
                         │  🎯 PC Games (Steam,      │
                         │  Epic, Game Pass, etc.)   │
                         │  100% Calibrated Signal!  │
                         └───────────────────────────┘
```

---

## ✨ Key Features (v1.0.0)

| Feature | Description |
|---|---|
| **🌐 10 Native Languages** | Seamless on-the-fly language selector: **English, Português (Brasil), Español, Français, Deutsch, Italiano, 日本語, 简体中文, Русский, and 한국어**. |
| **🎮 Authentic Physical Layout** | Unified central dashboard mirroring the real Xbox 360 controller geometry: triggers and bumpers on top (**LT/LB** and **RT/RB**), center menu (**Back**, **Xbox Guide**, **Start**), left wing with stick (**LS**) and **4-way D-Pad cross**, and right wing with diamond **ABXY** and stick (**RS**). |
| **🎯 Dedicated 0-255 Analog Triggers** | Dedicated buttons for **LT** and **RT** with independent left and right analog pressure bars (0 to 255 continuous standard byte readout and dynamic percentage). |
| **⏻ Controller Power-Off Button** | Shuts down wireless Xbox 360 controllers instantly from software using native XInput radio command (ordinal 103)—no need to pop off the battery pack! |
| **⊕ Statistical Median Auto-Center** | 2-second automatic center calibration calculating sample medians (immune to stray noise spikes and outliers). |
| **◎ Circular Auto-Range Calibration** | Rotate the stick in complete circles for 3 seconds to measure physical outer boundaries, ensuring full 100% sprint/look speed in games. |
| **〰️ Smooth Hermite Radial Deadzone** | Cubic Hermite curve transition at deadzone exit. Eliminates the abrupt 'jump' typical of basic square/axial deadzones. |
| **🛡️ Anti-Noise & Anti-Jitter Filtering** | Exponential Moving Average (EMA) filter + micro-jitter threshold to stabilize worn potentiometers and electrical signal hum. |
| **📈 Selectable Response Curves** | **Linear** (1:1), **Smooth** (quadratic, ideal for FPS precision aiming), **Aggressive** (square root, great for racing games), and **Extra Smooth** (cubic sniper mode). |
| **🔄 Axis Inversion (Inv. X / Inv. Y)** | Independent axis inversion toggles in case replacement stick modules were soldered in reversed orientation. |
| **⚡ Trigger Deadzone Tuning (LT / RT)** | Configurable initial deadzone for analog triggers to prevent accidental acceleration or firing. |
| **💾 Portable JSON Profiles** | Save and load custom profiles for various games or distinct controllers in the `profiles/` directory. |
| **🎮 ViGEmBus Virtual Controller** | Direct integration with `vgamepad` to feed calibrated states into Windows games. |
| **🚀 Silent Background Launch** | Bundled `INICIAR_SEM_CMD.vbs` launcher opens the tool with zero black CMD console popup. |

---

## 🧲 Technical Diagnosis: Hall Effect vs. Potentiometers on Xbox 360

If you have replaced or are planning to replace the analog sticks on an Xbox 360 controller, keep this engineering diagnosis in mind:

### 1. Traditional Potentiometers (Alps RKJXV 10kΩ — OEM Standard)
- **How they work:** Resistive voltage dividers. The Xbox 360 MCU supplies 3.3V across the outer terminals and samples voltage on the center wiper.
- **Verdict for Xbox 360:** **The Best Choice (Plug & Play).**
- **Advantage with this tool:** Slight mechanical soldering misalignments are no longer a concern. The **Auto-Center** feature in this software perfectly zeroes the center offset at (0, 0), completely eliminating the need to solder physical calibration trim pots.

### 2. Hall Effect Sensor Modules (Magnetic Retrofits)
- **Why does Axis Y frequently lock at 32767 on Xbox 360?**
  - Hall Effect sensors measure magnetic field intensity from tiny neodymium magnets.
  - The Xbox 360 controller **lacks internal MCU firmware calibration routines** (unlike modern DualSense or Xbox Series controllers where firmware recalibrates the non-linear magnetic curve).
  - Without MCU calibration, small angular deviations cause the sensor output to hit 3.3V (ADC rail saturation) before the stick reaches physical housing limits, locking the reading at **+32,767**.
- **Recommended steps if dealing with Hall Effect issues:**
  1. Try enabling the **Invert Y Axis** toggle in the tool to check if the axis responds in the proper direction.
  2. If the stick feels stiff or rubs against the casing, the gimbal frame is physically misaligned with the PCB.
  3. **Most reliable long-term solution:** Desolder problematic Hall Effect modules and install high-quality **traditional 10kΩ potentiometers**. This software tool will take care of zeroing center drift and smoothing the signal!

---

## 📦 Prerequisites & Quick Setup

> [!IMPORTANT]
> ### 🚨 Essential Requirements Before Using:
> 1. **Python 3 installed on Windows:** When running the Python installer, **make sure to check the "Add python.exe to PATH" checkbox** on the first setup screen.
> 2. **Run the dependency installer:** Before opening the tool for the first time, double-click **`INSTALAR_DEPENDENCIAS.bat`** to automatically download and configure all necessary libraries.

### System Requirements:
- **Windows 10** or **Windows 11** (64-bit)
- **Python 3.10 or higher** ([Download from python.org](https://www.python.org/downloads/) — **check *"Add python.exe to PATH"*** during installation)
- **PC Wireless Gaming Receiver** (for wireless controllers) or **USB Cable / Play & Charge**
- **ViGEmBus Driver** (required to generate the calibrated virtual controller in games)

### Step-by-Step Installation (Under 2 minutes):

1. **Download the Release:**
   - Grab `Xbox360_Calibration_Tool_v1.0.0.zip` from the [Releases](https://github.com/Emertels/Xbox-360-Controller-Calibration-Tool/releases) tab and extract it to any folder on your PC.

2. **Install Dependencies (Mandatory on first run):**
   - Double-click:
     ```cmd
     INSTALAR_DEPENDENCIAS.bat
     ```
   - A command prompt will open, detect Python automatically, and install `vgamepad`. Once complete, press any key to close.

3. **Install ViGEmBus Driver (Required for in-game use):**
   - Download and run the official ViGEmBus `.msi` installer:
     👉 [Download ViGEmBus Driver (GitHub Releases)](https://github.com/nefarius/ViGEmBus/releases)
   - Standard setup: click *Next → Next → Install*.

4. **Launch the Tool:**
   - **Silent Mode (No black console window, Recommended):** Double-click **`INICIAR_SEM_CMD.vbs`**.
   - **Batch script:** Double-click **`INICIAR.bat`**.

---

## 🕹️ Step-by-Step Usage Guide

```
1. Connect Controller ➔ 2. Auto-Center ➔ 3. Auto-Range ➔ 4. Save Profile ➔ 5. Activate Virtual
```

1. **Turn on the controller:** Press the Xbox Guide button or plug in the USB cable. The top header will turn green: `✅ Controller connected — Player 1`.
2. **Auto-Center:**
   - **Release both analog sticks completely** (leave them at neutral resting position).
   - Click **⊕ Auto-Center** on the Left Stick calibration card. Wait 2 seconds without touching the stick.
   - Repeat for the Right Stick.
   - The green calibrated dot (**Cal**) will lock dead center at (0, 0).
3. **Auto-Range (Outer Boundary Calibration):**
   - Click **◎ Auto-Range** and rotate the stick in full smooth circles rubbing against the plastic bezel for 3 seconds.
   - The boundary scale will automatically adapt so that 100% sprint/look velocity is reached in all directions.
4. **Fine-Tuning Noise & Deadzone:**
   - If the green dot trembles slightly due to potentiometer electrical noise, increase the **Anti-Noise Filter** (e.g., 15%) and **Anti-Jitter** (e.g., 80).
   - If mechanical return spring slack remains, raise the **Deadzone** slider to 5% – 8%.
5. **Save Profile:**
   - Click **💾 Save Profile** to store your calibrated values into a portable `.json` file.
6. **Play Games:**
   - Click **▶ Activate Virtual Gamepad**.
   - The virtual driver creates a clean Xbox 360 controller forwarding 100% calibrated inputs to your games!

---

## 💡 Pro Tip: How to Prevent Duplicate Controller Input with HidHide

Certain PC games, simulators, and emulators detect both the physical Xbox 360 controller (Player 1) and the virtual gamepad generated by ViGEmBus (Player 2), causing double-input conflicts.

To solve this completely:

1. Download **HidHide** (free, official utility maintained by the Nefarius team):
   👉 [Download HidHide Installer](https://github.com/nefarius/HidHide/releases)
2. Open the HidHide Configuration Client:
   - On the **Applications** tab, add `python.exe` and `pythonw.exe` to the whitelist.
   - On the **Devices** tab, check the box next to your physical **Xbox 360 Wireless Receiver / Controller** to hide it from all other software.
3. Enable the **Enable device hiding** toggle.
4. **Result:** Your PC games will exclusively recognize the calibrated virtual controller, completely avoiding duplicate input!

---

## 📁 Repository Structure

```
Xbox-360-Controller-Calibration-Tool/
│
├── INICIAR_SEM_CMD.vbs         # Silent launcher (100% no console window)
├── INICIAR.bat                 # Portable batch launcher with smart Python discovery
├── INSTALAR_DEPENDENCIAS.bat   # Automated dependency installer via pip
├── main.py                     # Main Tkinter GUI application (~60-120fps)
├── i18n.py                     # Multilingual localization engine (10 native languages)
├── xinput_reader.py            # High-performance ctypes wrapper for xinput1_4.dll
├── calibration.py              # Mathematical engine: Hermite deadzone, EMA, curves, range
├── virtual_gamepad.py          # Virtual gamepad emulator via ViGEmBus (vgamepad)
├── profiles.py                 # JSON profile serialization manager
├── requirements.txt            # Python dependencies (vgamepad)
├── README.md                   # Documentation in Portuguese (PT-BR)
├── README.en.md                # Documentation in English (EN)
├── AGENTS.md                   # System Architecture & Technical Guide in Portuguese
├── AGENTS.en.md                # System Architecture & Technical Guide in English
└── profiles/                   # Portable folder where JSON calibration profiles reside
```

---

## ❓ Frequently Asked Questions (FAQ)

#### Does the tool need to remain running while I play?
Yes! Because the physical Xbox 360 controller hardware cannot store calibration offsets internally, this software acts as a lightweight, real-time background translator with negligible CPU usage (< 0.5%).

#### What is the Response Curve and which one should I pick?
- **Linear (1:1):** Standard direct mapping.
- **Smooth (Quadratic):** Dampens center sensitivity for surgical micro-aiming while preserving fast turns on outer edges. Highly recommended for FPS titles (Halo, Call of Duty, Battlefield).
- **Aggressive (Square Root):** Instant snap response with small stick movements. Excellent for racing and fighting games.
- **Extra Smooth (Cubic):** Ultra-stable sniper mode.

#### My left stick has Y locked at 32767. Can this software fix it?
If the value remains frozen at 32,767 even when moving the stick in all directions, the sensor is not outputting voltage changes (frequent with misaligned Hall Effect modules on the 360). Check the [Technical Diagnosis](#-technical-diagnosis-hall-effect-vs-potentiometers-on-xbox-360) section for root causes and physical solutions.

---

## 🔗 Useful References & Links

- **ViGEmBus (Virtual Gamepad Emulation Framework):** https://github.com/nefarius/ViGEmBus
- **HidHide (Input Device Hiding Filter Driver):** https://github.com/nefarius/HidHide
- **vgamepad (Python Bindings for ViGEm):** https://pypi.org/project/vgamepad/
- **Microsoft XInput API Documentation:** https://learn.microsoft.com/en-us/windows/win32/xinput/getting-started-with-xinput
- **Gamepad Tester Online:** https://hardwaretester.com/gamepad

---

## 📄 License & Credits

Distributed under the **MIT License**. You are free to use, modify, study, and distribute this project.

Developed by **Emerson Teles** ([@Emertels](https://github.com/Emertels)) with the assistance of **Google Antigravity**.
