"""
Xbox 360 Controller Calibration Tool — Main GUI (v1.0.0)
=========================================================
Ferramenta profissional e de código aberto para calibração de analógicos e gatilhos para Xbox 360 via software.

Funcionalidades:
  - Layout unificado com a geometria física oficial do controle Xbox 360
  - Suporte a 10 idiomas nativos (pt, en, es, fr, de, it, ja, zh, ru, ko)
  - Botão de desligar controle sem fio instantâneo (via XInput ordinal 103)
  - Gatilhos analógicos com botões dedicados LT e RT e barras de pressão (0-255)
  - Diamante ABXY nas cores autênticas e D-Pad em cruz com setas direcionais
  - Auto-Center por mediana estatística e Auto-Range circular contínuo
  - Deadzone radial suave com interpolação Hermite e filtros Anti-Ruído/Anti-Jitter
  - Curvas de resposta configuráveis (Linear, Suave/FPS, Agressivo/Corrida, Extra Suave)
  - Compatibilidade com receptores wireless, cabos Play & Charge USB e controles com fio
  - Integração com ViGEmBus para controle virtual calibrado nos jogos

Author: Emerson Teles (projeto criado com auxilio do Antigravity)
License: MIT
"""

from __future__ import annotations

import math
import statistics
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable

from xinput_reader import XInputReader, ControllerState, ALL_BUTTONS
from calibration import (
    STICK_MAX,
    CalibrationSettings,
    StickCalibration,
    NoiseFilter,
    apply_stick_calibration,
    apply_trigger_deadzone,
)
from virtual_gamepad import VirtualGamepad, VGAMEPAD_AVAILABLE
from profiles import save_profile, load_profile, list_profiles, get_profile_dir
from i18n import (
    T, set_language, get_language, get_languages, toggle_language,
    get_curve_labels, curve_label_to_key, curve_key_to_label, CURVE_KEYS,
)

# ---------------------------------------------------------------------------
# Theme Colors & Styles
# ---------------------------------------------------------------------------
BG_DARK = "#0a0a14"
BG_CARD = "#121224"
BG_PANEL = "#17172f"
BG_CANVAS = "#0c0c1a"
BG_HEADER = "#101026"
BG_TAB = "#15152c"
BG_BTN_DEFAULT = "#222248"
BG_BTN_HOVER = "#323264"

FG_TEXT = "#eaeaf5"
FG_DIM = "#7e7ea8"
FG_ACCENT = "#38bdf8"
FG_GREEN = "#4ade80"
FG_RED = "#f87171"
FG_YELLOW = "#facc15"
FG_ORANGE = "#fb923c"
FG_PURPLE = "#c084fc"

GRID_COLOR = "#1f1f3d"
DEADZONE_COLOR = "#383868"

FONT_APP_TITLE = ("Segoe UI", 10, "bold")
FONT_STICK_TITLE = ("Segoe UI", 11, "bold")
FONT_SECTION = ("Segoe UI", 9, "bold")
FONT_LABEL = ("Segoe UI", 9)
FONT_VALUE = ("Consolas", 10, "bold")
FONT_SMALL = ("Segoe UI", 8)
FONT_TINY = ("Segoe UI", 7)
FONT_BUTTON = ("Segoe UI", 9, "bold")
FONT_HELP_TITLE = ("Segoe UI", 11, "bold")
FONT_HELP_BODY = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 9)

UPDATE_MS = 16
AUTOCENTER_SAMPLES = 120
AUTORANGE_SAMPLES = 180


# ---------------------------------------------------------------------------
# StickCanvas — High Precision Visualisation
# ---------------------------------------------------------------------------
class StickCanvas:
    """Draws a radar-style circular viewport showing raw vs calibrated stick position."""

    def __init__(self, parent: tk.Widget, title_key: str, size: int = 210) -> None:
        self.size = size
        self.half = size // 2
        self.title_key = title_key

        self.frame = tk.Frame(parent, bg=BG_CARD, padx=8, pady=8,
                              highlightthickness=1, highlightbackground="#25254d")

        self.title_label = tk.Label(
            self.frame, text=T(title_key), font=FONT_STICK_TITLE,
            bg=BG_CARD, fg=FG_ACCENT,
        )
        self.title_label.pack(pady=(0, 4))

        self.canvas = tk.Canvas(
            self.frame, width=size, height=size,
            bg=BG_CANVAS, highlightthickness=1, highlightbackground="#26264e",
        )
        self.canvas.pack()

        info = tk.Frame(self.frame, bg=BG_CARD)
        info.pack(fill="x", pady=(6, 0))

        self.raw_label = tk.Label(info, text="Bruto:  X=     0  Y=     0",
                                  font=FONT_VALUE, bg=BG_CARD, fg=FG_RED, anchor="w")
        self.raw_label.pack(fill="x")

        self.cal_label = tk.Label(info, text="Calib:  X=     0  Y=     0",
                                  font=FONT_VALUE, bg=BG_CARD, fg=FG_GREEN, anchor="w")
        self.cal_label.pack(fill="x")

        self.mag_label = tk.Label(info, text="Magnitude: 0%", font=FONT_SMALL,
                                  bg=BG_CARD, fg=FG_DIM, anchor="w")
        self.mag_label.pack(fill="x")

        self._draw_base()

    def _draw_base(self) -> None:
        cx = cy = self.half
        for pct, lbl in [(0.25, "25%"), (0.50, "50%"), (0.75, "75%"), (1.00, "")]:
            r = int(pct * (self.half - 8))
            outline = "#343468" if pct == 1.0 else GRID_COLOR
            width = 2 if pct == 1.0 else 1
            self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                    outline=outline, width=width)
            if lbl:
                self.canvas.create_text(cx + r - 2, cy - 7, text=lbl,
                                        fill="#3e3e70", font=FONT_TINY, anchor="e")

        self.canvas.create_line(0, cy, self.size, cy, fill=GRID_COLOR)
        self.canvas.create_line(cx, 0, cx, self.size, fill=GRID_COLOR)

    def update(self, raw_x: int, raw_y: int, cal_x: int, cal_y: int,
               deadzone_pct: float) -> None:
        self.canvas.delete("dyn")
        cx = cy = self.half
        usable = self.half - 8
        scale = usable / STICK_MAX

        # Deadzone visual ring
        dz_r = (deadzone_pct / 100.0) * usable
        if dz_r > 1:
            self.canvas.create_oval(cx - dz_r, cy - dz_r, cx + dz_r, cy + dz_r,
                                    outline=DEADZONE_COLOR, dash=(3, 3), width=1, tags="dyn")

        # Raw trail line (dark red)
        rx = cx + raw_x * scale
        ry = cy - raw_y * scale
        self.canvas.create_line(cx, cy, rx, ry, fill="#55222b", width=1, tags="dyn")

        # Raw dot (vibrant red)
        self.canvas.create_oval(rx - 5, ry - 5, rx + 5, ry + 5,
                                fill=FG_RED, outline="#ffa4a4", width=1, tags="dyn")

        # Calibrated trail line (subtle green)
        gx = cx + cal_x * scale
        gy = cy - cal_y * scale
        self.canvas.create_line(cx, cy, gx, gy, fill="#1c4728", width=1, tags="dyn")

        # Calibrated dot (glowing green)
        self.canvas.create_oval(gx - 5, gy - 5, gx + 5, gy + 5,
                                fill=FG_GREEN, outline="#bbf7d0", width=1, tags="dyn")

        raw_str = f"{T('raw_prefix')}:  X={raw_x:>6d}  Y={raw_y:>6d}"
        cal_str = f"{T('cal_prefix')}:  X={cal_x:>6d}  Y={cal_y:>6d}"
        self.raw_label.config(text=raw_str)
        self.cal_label.config(text=cal_str)

        pct = min(100, int((math.hypot(cal_x, cal_y) / STICK_MAX) * 100))
        self.mag_label.config(text=f"{T('mag_prefix')}: {pct}%")

    def retranslate(self) -> None:
        self.title_label.config(text=T(self.title_key))


# ---------------------------------------------------------------------------
# TriggerUnit & TriggerBar
# ---------------------------------------------------------------------------
class TriggerUnit:
    """Analog trigger pressure gauge (0-255) with dedicated button indicator."""

    def __init__(self, parent: tk.Widget, label: str, w: int = 80, h: int = 14, mirrored: bool = False) -> None:
        self.w, self.h = w, h
        self.label = label
        self.mirrored = mirrored
        self.frame = tk.Frame(parent, bg=BG_CARD)

        self.btn = tk.Label(
            self.frame, text=label, font=FONT_BUTTON,
            bg="#1e293b", fg="#cbd5e1", width=3,
            padx=2, pady=1, relief="groove", bd=1,
        )

        self.canvas = tk.Canvas(
            self.frame, width=w, height=h, bg="#0d0d1e",
            highlightthickness=1, highlightbackground="#25254d",
        )

        self.val_lbl = tk.Label(
            self.frame, text="  0 (  0%)", font=FONT_SMALL,
            bg=BG_CARD, fg=FG_TEXT, width=8, anchor="center",
        )

        if not mirrored:
            self.btn.pack(side="left", padx=(0, 3))
            self.canvas.pack(side="left", padx=2)
            self.val_lbl.pack(side="left", padx=(3, 0))
        else:
            self.val_lbl.pack(side="left", padx=(0, 3))
            self.canvas.pack(side="left", padx=2)
            self.btn.pack(side="left", padx=(3, 0))

    def update(self, raw: int, cal: int) -> None:
        self.canvas.delete("bar")
        cw = int((cal / 255.0) * self.w)
        rw = int((raw / 255.0) * self.w)

        if self.mirrored:
            if rw > 0:
                self.canvas.create_rectangle(self.w - rw, 0, self.w, self.h, fill="#25254a", outline="", tags="bar")
            if cw > 0:
                self.canvas.create_rectangle(self.w - cw, 0, self.w, self.h, fill="#06b6d4", outline="", tags="bar")
        else:
            if rw > 0:
                self.canvas.create_rectangle(0, 0, rw, self.h, fill="#25254a", outline="", tags="bar")
            if cw > 0:
                self.canvas.create_rectangle(0, 0, cw, self.h, fill="#06b6d4", outline="", tags="bar")

        pct = min(100, int((cal / 255.0) * 100))
        self.val_lbl.config(text=f"{cal:>3d} ({pct:>2d}%)")

        if cal > 15:
            self.btn.config(bg="#06b6d4", fg="#082f49", relief="sunken")
        else:
            self.btn.config(bg="#1e293b", fg="#cbd5e1", relief="groove")


TriggerBar = TriggerUnit


# ---------------------------------------------------------------------------
# Unified ControllerPanel (Physical Xbox 360 Layout)
# ---------------------------------------------------------------------------
class ControllerPanel:
    """Unified Xbox 360 controller panel: authentic layout of triggers, bumpers, menu, D-Pad, and ABXY."""

    def __init__(self, parent: tk.Widget) -> None:
        self.frame = tk.LabelFrame(
            parent, text=f"  {T('buttons')}  ", font=FONT_SECTION,
            bg=BG_CARD, fg=FG_ACCENT, padx=10, pady=6,
            highlightthickness=1, highlightbackground="#25254d",
        )
        self._btns: dict[str, tk.Label] = {}
        self._default_colors: dict[str, tuple[str, str, str, str]] = {}

        # Row 1: Analog Triggers (Left & Right with 0-255 gauges and dedicated buttons)
        row_triggers = tk.Frame(self.frame, bg=BG_CARD)
        row_triggers.pack(fill="x", pady=(1, 4))

        self.lt_unit = TriggerUnit(row_triggers, "LT", w=80, h=14, mirrored=False)
        self.lt_unit.frame.pack(side="left", padx=(4, 0))

        tk.Label(row_triggers, text="🎮", font=FONT_BUTTON, bg=BG_CARD, fg="#4f46e5").pack(side="left", expand=True)

        self.rt_unit = TriggerUnit(row_triggers, "RT", w=80, h=14, mirrored=True)
        self.rt_unit.frame.pack(side="right", padx=(0, 4))

        # Row 2: Bumpers (LB & RB) and Center Menu (Back, Guide, Start)
        row_bumpers_menu = tk.Frame(self.frame, bg=BG_CARD)
        row_bumpers_menu.pack(fill="x", pady=(2, 6))

        self._create_btn(row_bumpers_menu, "LB", unpressed=("#1e293b", "#cbd5e1"), pressed=("#38bdf8", "#082f49"),
                         w=5, side="left", padx=(6, 0))

        center_menu = tk.Frame(row_bumpers_menu, bg=BG_CARD)
        center_menu.pack(side="left", expand=True)
        self._create_btn(center_menu, "Back", unpressed=("#1a1a36", "#a5b4fc"), pressed=("#6366f1", "#1e1b4b"),
                         w=5, side="left", padx=2)
        self._create_btn(center_menu, "Guide", unpressed=("#0d3815", "#86efac"), pressed=("#107c10", "#dcfce7"),
                         w=7, display_text="⨂ Xbox", side="left", padx=3)
        self._create_btn(center_menu, "Start", unpressed=("#1a1a36", "#a5b4fc"), pressed=("#6366f1", "#1e1b4b"),
                         w=5, side="left", padx=2)

        self._create_btn(row_bumpers_menu, "RB", unpressed=("#1e293b", "#cbd5e1"), pressed=("#38bdf8", "#082f49"),
                         w=5, side="right", padx=(0, 6))

        # Row 3: Controller Body Wings (Left Wing: LS & D-Pad | Center: Badge | Right Wing: ABXY & RS)
        row_body = tk.Frame(self.frame, bg=BG_CARD)
        row_body.pack(fill="x", pady=(2, 2))

        # --- Left Wing (LS at top, D-Pad at bottom) ---
        left_wing = tk.Frame(row_body, bg=BG_CARD)
        left_wing.pack(side="left", expand=True)

        ls_frame = tk.Frame(left_wing, bg=BG_CARD)
        ls_frame.pack(pady=(0, 4))
        self._create_btn(ls_frame, "LS", unpressed=("#2e1065", "#e9d5ff"), pressed=("#a855f7", "#2e1065"),
                         w=4, display_text="LS")

        dpad_grid = tk.Frame(left_wing, bg=BG_CARD)
        dpad_grid.pack(pady=(2, 0))
        self._create_grid_btn(dpad_grid, "DPad Up", row=0, col=1, text="▲",
                              unpressed=("#181834", "#cbd5e1"), pressed=("#38bdf8", "#082f49"), w=3)
        self._create_grid_btn(dpad_grid, "DPad Left", row=1, col=0, text="◀",
                              unpressed=("#181834", "#cbd5e1"), pressed=("#38bdf8", "#082f49"), w=3)
        tk.Label(dpad_grid, text="✚", font=FONT_TINY, bg=BG_CARD, fg="#333360", width=2).grid(row=1, column=1)
        self._create_grid_btn(dpad_grid, "DPad Right", row=1, col=2, text="▶",
                              unpressed=("#181834", "#cbd5e1"), pressed=("#38bdf8", "#082f49"), w=3)
        self._create_grid_btn(dpad_grid, "DPad Down", row=2, col=1, text="▼",
                              unpressed=("#181834", "#cbd5e1"), pressed=("#38bdf8", "#082f49"), w=3)

        # --- Center Badge ---
        center_badge = tk.Frame(row_body, bg=BG_CARD)
        center_badge.pack(side="left", expand=True, padx=4)
        tk.Label(center_badge, text="XBOX 360", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg="#4b5563").pack(pady=(10, 1))
        tk.Label(center_badge, text="● ● ●", font=FONT_TINY, bg=BG_CARD, fg="#374151").pack()

        # --- Right Wing (ABXY Diamond at top, RS at bottom) ---
        right_wing = tk.Frame(row_body, bg=BG_CARD)
        right_wing.pack(side="right", expand=True)

        abxy_grid = tk.Frame(right_wing, bg=BG_CARD)
        abxy_grid.pack(pady=(0, 4))
        self._create_grid_btn(abxy_grid, "Y", row=0, col=1, text="Y",
                              unpressed=("#713f12", "#fef08a"), pressed=("#eab308", "#422006"), w=3)
        self._create_grid_btn(abxy_grid, "X", row=1, col=0, text="X",
                              unpressed=("#1e3a8a", "#bfdbfe"), pressed=("#3b82f6", "#0f172a"), w=3)
        tk.Label(abxy_grid, text="•", font=FONT_TINY, bg=BG_CARD, fg="#333360", width=2).grid(row=1, column=1)
        self._create_grid_btn(abxy_grid, "B", row=1, col=2, text="B",
                              unpressed=("#7f1d1d", "#fecaca"), pressed=("#ef4444", "#450a0a"), w=3)
        self._create_grid_btn(abxy_grid, "A", row=2, col=1, text="A",
                              unpressed=("#14532d", "#bbf7d0"), pressed=("#22c55e", "#052e16"), w=3)

        rs_frame = tk.Frame(right_wing, bg=BG_CARD)
        rs_frame.pack(pady=(2, 0))
        self._create_btn(rs_frame, "RS", unpressed=("#2e1065", "#e9d5ff"), pressed=("#a855f7", "#2e1065"),
                         w=4, display_text="RS")

    def _create_btn(self, parent: tk.Widget, name: str,
                    unpressed: tuple[str, str], pressed: tuple[str, str],
                    w: int = 4, display_text: str | None = None,
                    side: str = "left", padx: int | tuple[int, int] = 2,
                    pady: int | tuple[int, int] = 1) -> tk.Label:
        txt = display_text or name
        lbl = tk.Label(parent, text=txt, font=FONT_BUTTON, bg=unpressed[0], fg=unpressed[1],
                       width=w, padx=3, pady=1, relief="groove", bd=1)
        lbl.pack(side=side, padx=padx, pady=pady)
        self._btns[name] = lbl
        self._default_colors[name] = (unpressed[0], unpressed[1], pressed[0], pressed[1])
        return lbl

    def _create_grid_btn(self, parent: tk.Widget, name: str, row: int, col: int, text: str,
                         unpressed: tuple[str, str] = ("#181834", "#cbd5e1"),
                         pressed: tuple[str, str] = ("#38bdf8", "#082f49"),
                         w: int = 3) -> tk.Label:
        lbl = tk.Label(parent, text=text, font=FONT_BUTTON, bg=unpressed[0], fg=unpressed[1],
                       width=w, padx=2, pady=1, relief="groove", bd=1)
        lbl.grid(row=row, column=col, padx=1, pady=1)
        self._btns[name] = lbl
        self._default_colors[name] = (unpressed[0], unpressed[1], pressed[0], pressed[1])
        return lbl

    def update(self, state: ControllerState) -> None:
        pressed = set(state.get_pressed_buttons())
        for name, lbl in self._btns.items():
            u_bg, u_fg, p_bg, p_fg = self._default_colors[name]
            if name in pressed:
                lbl.config(bg=p_bg, fg=p_fg, relief="sunken")
            else:
                lbl.config(bg=u_bg, fg=u_fg, relief="groove")

    def retranslate(self) -> None:
        self.frame.config(text=f"  {T('buttons')}  ")


ButtonPanel = ControllerPanel


# ---------------------------------------------------------------------------
# Stick Calibration Panel (Side-by-Side within Tab 1)
# ---------------------------------------------------------------------------
class StickCalibrationPanel:
    """Controls for calibrating a single analog stick: Auto-Center, Auto-Range, sliders, curves."""

    def __init__(self, parent: tk.Widget, title_key: str, cal: StickCalibration) -> None:
        self.cal = cal
        self.title_key = title_key
        self._sampling_center = False
        self._samples_x: list[int] = []
        self._samples_y: list[int] = []
        self._sampling_range = False
        self._range_max: float = 0.0
        self._range_remaining: int = 0

        self.frame = tk.LabelFrame(
            parent, text=f"  {T(title_key)}  ", font=FONT_SECTION,
            bg=BG_TAB, fg=FG_ACCENT, padx=10, pady=8,
            highlightthickness=1, highlightbackground="#2d2d55",
        )

        # Header: Action Buttons + Center Label + Reset
        row_act = tk.Frame(self.frame, bg=BG_TAB)
        row_act.pack(fill="x", pady=(0, 6))

        self.btn_ac = tk.Button(
            row_act, text=T("auto_center"), font=FONT_BUTTON,
            bg="#166534", fg="#fef08a", activebackground="#15803d",
            relief="flat", padx=10, pady=3, cursor="hand2",
            command=self._start_ac,
        )
        self.btn_ac.pack(side="left")

        self.btn_ar = tk.Button(
            row_act, text=T("auto_range"), font=FONT_BUTTON,
            bg="#701a75", fg="#fed7aa", activebackground="#86198f",
            relief="flat", padx=10, pady=3, cursor="hand2",
            command=self._start_ar,
        )
        self.btn_ar.pack(side="left", padx=(6, 0))

        self.center_lbl = tk.Label(
            row_act, text=f"{T('center')}: X=0.0  Y=0.0",
            font=FONT_VALUE, bg=BG_TAB, fg=FG_DIM,
        )
        self.center_lbl.pack(side="left", padx=(10, 0))

        self.btn_reset = tk.Button(
            row_act, text=T("reset"), font=FONT_SMALL,
            bg=BG_BTN_DEFAULT, fg=FG_DIM, activebackground=BG_BTN_HOVER,
            relief="flat", padx=8, cursor="hand2", command=self._reset,
        )
        self.btn_reset.pack(side="right")

        # Sliders Section
        self._sliders_frame = tk.Frame(self.frame, bg=BG_TAB)
        self._sliders_frame.pack(fill="x")

        self.dz_var = tk.DoubleVar(value=cal.deadzone)
        self.rng_var = tk.DoubleVar(value=cal.range_scale)
        self.nf_var = tk.DoubleVar(value=cal.noise_filter)
        self.aj_var = tk.IntVar(value=cal.anti_jitter)

        self.dz_lbl = self._make_slider("deadzone", self.dz_var, 0, 40, self._on_dz, f"{cal.deadzone:.0f}%")
        self.rng_lbl = self._make_slider("range", self.rng_var, 50, 150, self._on_rng, f"{cal.range_scale:.0f}%")
        self.nf_lbl = self._make_slider("noise_filter", self.nf_var, 0, 0.5, self._on_nf, f"{cal.noise_filter:.0%}")
        self.aj_lbl = self._make_slider("anti_jitter", self.aj_var, 0, 200, self._on_aj, str(cal.anti_jitter))

        # Bottom Row: Response Curve Dropdown + Invert Checkboxes
        row_bot = tk.Frame(self.frame, bg=BG_TAB)
        row_bot.pack(fill="x", pady=(6, 0))

        self.curve_lbl = tk.Label(row_bot, text=T("response_curve"), font=FONT_LABEL,
                                  bg=BG_TAB, fg=FG_DIM)
        self.curve_lbl.pack(side="left")

        self.curve_var = tk.StringVar(value=curve_key_to_label(cal.response_curve))
        self.curve_combo = ttk.Combobox(row_bot, textvariable=self.curve_var,
                                        width=26, state="readonly",
                                        values=get_curve_labels())
        self.curve_combo.pack(side="left", padx=(4, 12))
        self.curve_combo.bind("<<ComboboxSelected>>", self._on_curve)

        self.inv_x_var = tk.BooleanVar(value=cal.invert_x)
        self.inv_y_var = tk.BooleanVar(value=cal.invert_y)

        self.chk_ix = tk.Checkbutton(
            row_bot, text=T("invert_x"), font=FONT_LABEL,
            variable=self.inv_x_var, command=self._on_inv,
            bg=BG_TAB, fg=FG_TEXT, selectcolor="#2d2d5a",
            activebackground=BG_TAB, activeforeground=FG_TEXT,
        )
        self.chk_ix.pack(side="left")

        self.chk_iy = tk.Checkbutton(
            row_bot, text=T("invert_y"), font=FONT_LABEL,
            variable=self.inv_y_var, command=self._on_inv,
            bg=BG_TAB, fg=FG_TEXT, selectcolor="#2d2d5a",
            activebackground=BG_TAB, activeforeground=FG_TEXT,
        )
        self.chk_iy.pack(side="left", padx=(8, 0))

    def _make_slider(self, label_key: str, var: tk.Variable,
                     from_: float, to: float, cmd: Callable,
                     init_text: str) -> tk.Label:
        row = tk.Frame(self._sliders_frame, bg=BG_TAB)
        row.pack(fill="x", pady=2)

        lbl = tk.Label(row, text=T(label_key), font=FONT_LABEL, bg=BG_TAB,
                       fg=FG_DIM, width=17, anchor="w")
        lbl.pack(side="left")
        lbl._i18n_key = label_key

        ttk.Scale(row, from_=from_, to=to, variable=var, orient="horizontal",
                  command=cmd).pack(side="left", fill="x", expand=True, padx=6)

        val_lbl = tk.Label(row, text=init_text, font=FONT_VALUE, bg=BG_TAB,
                           fg=FG_TEXT, width=6, anchor="e")
        val_lbl.pack(side="left")
        return val_lbl

    # -- Callbacks ---
    def _on_dz(self, _v: str) -> None:
        v = self.dz_var.get()
        self.cal.deadzone = v
        self.dz_lbl.config(text=f"{v:.0f}%")

    def _on_rng(self, _v: str) -> None:
        v = self.rng_var.get()
        self.cal.range_scale = v
        self.rng_lbl.config(text=f"{v:.0f}%")

    def _on_nf(self, _v: str) -> None:
        v = self.nf_var.get()
        self.cal.noise_filter = v
        self.nf_lbl.config(text=f"{v:.0%}")

    def _on_aj(self, _v: str) -> None:
        v = int(self.aj_var.get())
        self.cal.anti_jitter = v
        self.aj_lbl.config(text=str(v))

    def _on_curve(self, _e: object) -> None:
        self.cal.response_curve = curve_label_to_key(self.curve_combo.get())

    def _on_inv(self) -> None:
        self.cal.invert_x = self.inv_x_var.get()
        self.cal.invert_y = self.inv_y_var.get()

    def _reset(self) -> None:
        self.cal.center_x = 0.0
        self.cal.center_y = 0.0
        self.cal.deadzone = 5.0
        self.cal.range_scale = 100.0
        self.cal.invert_x = False
        self.cal.invert_y = False
        self.cal.response_curve = "linear"
        self.cal.noise_filter = 0.15
        self.cal.anti_jitter = 80
        self.dz_var.set(5.0)
        self.rng_var.set(100.0)
        self.nf_var.set(0.15)
        self.aj_var.set(80)
        self.inv_x_var.set(False)
        self.inv_y_var.set(False)
        self.curve_combo.set(curve_key_to_label("linear"))
        self._upd_center()

    # -- Auto-center (Median) ---
    def _start_ac(self) -> None:
        self._sampling_center = True
        self._samples_x.clear()
        self._samples_y.clear()
        self.btn_ac.config(text=T("dont_touch"), state="disabled", fg=FG_DIM)

    def feed_sample(self, raw_x: int, raw_y: int) -> None:
        if self._sampling_center:
            self._samples_x.append(raw_x)
            self._samples_y.append(raw_y)
            rem = AUTOCENTER_SAMPLES - len(self._samples_x)
            if rem > 0:
                self.btn_ac.config(text=f"... {rem}")
            else:
                self._finish_ac()

        if self._sampling_range:
            cx = raw_x - self.cal.center_x
            cy = raw_y - self.cal.center_y
            mag = math.hypot(cx, cy)
            if mag > self._range_max:
                self._range_max = mag
            self._range_remaining -= 1
            if self._range_remaining > 0:
                pct = int((self._range_max / STICK_MAX) * 100) if STICK_MAX else 0
                self.btn_ar.config(text=f"Max: {pct}% ({self._range_remaining})")
            else:
                self._finish_ar()

    def _finish_ac(self) -> None:
        if self._samples_x:
            self.cal.center_x = statistics.median(self._samples_x)
            self.cal.center_y = statistics.median(self._samples_y)
        self._sampling_center = False
        self._samples_x.clear()
        self._samples_y.clear()
        self.btn_ac.config(text=T("auto_center"), state="normal", fg="#fef08a")
        self._upd_center()

    def _start_ar(self) -> None:
        self._sampling_range = True
        self._range_max = 0.0
        self._range_remaining = AUTORANGE_SAMPLES
        self.btn_ar.config(text=T("spin_stick"), state="disabled", fg=FG_DIM)

    def _finish_ar(self) -> None:
        if self._range_max > 100:
            pct = (self._range_max / STICK_MAX) * 100
            self.cal.range_scale = round(pct, 1)
            self.rng_var.set(self.cal.range_scale)
            self.rng_lbl.config(text=f"{self.cal.range_scale:.0f}%")
        self._sampling_range = False
        self.btn_ar.config(text=T("auto_range"), state="normal", fg="#fed7aa")

    def _upd_center(self) -> None:
        self.center_lbl.config(
            text=f"{T('center')}: X={self.cal.center_x:.1f}  Y={self.cal.center_y:.1f}")

    def load_from(self, cal: StickCalibration) -> None:
        for attr in ("center_x", "center_y", "deadzone", "range_scale",
                     "invert_x", "invert_y", "response_curve", "noise_filter", "anti_jitter"):
            setattr(self.cal, attr, getattr(cal, attr))
        self.dz_var.set(cal.deadzone)
        self.rng_var.set(cal.range_scale)
        self.nf_var.set(cal.noise_filter)
        self.aj_var.set(cal.anti_jitter)
        self.inv_x_var.set(cal.invert_x)
        self.inv_y_var.set(cal.invert_y)
        self.curve_combo.set(curve_key_to_label(cal.response_curve))
        self._upd_center()

    def retranslate(self) -> None:
        self.frame.config(text=f"  {T(self.title_key)}  ")
        self.btn_ac.config(text=T("auto_center"))
        self.btn_ar.config(text=T("auto_range"))
        self.btn_reset.config(text=T("reset"))
        self.curve_lbl.config(text=T("response_curve"))
        self.chk_ix.config(text=T("invert_x"))
        self.chk_iy.config(text=T("invert_y"))
        self.curve_combo.config(values=get_curve_labels())
        self.curve_combo.set(curve_key_to_label(self.cal.response_curve))
        self._upd_center()
        for widget in self._sliders_frame.winfo_children():
            for child in widget.winfo_children():
                if hasattr(child, "_i18n_key"):
                    child.config(text=T(child._i18n_key))


# ---------------------------------------------------------------------------
# Tab: Triggers & Response Curves Info
# ---------------------------------------------------------------------------
class TriggersTab:
    """Tab 2: Trigger deadzone sliders and response curve comparison."""

    def __init__(self, parent: tk.Widget, settings: CalibrationSettings) -> None:
        self.settings = settings
        self.frame = tk.Frame(parent, bg=BG_TAB, padx=16, pady=12)

        # Trigger Deadzone Settings Card
        self.card_dz = tk.LabelFrame(
            self.frame, text=f"  {T('trig_dz_title')}  ", font=FONT_SECTION,
            bg=BG_CARD, fg=FG_ACCENT, padx=12, pady=10,
            highlightthickness=1, highlightbackground="#25254d",
        )
        self.card_dz.pack(fill="x", pady=(0, 10))

        self.dz_desc = tk.Label(self.card_dz, text=T("trig_dz_desc"), font=FONT_SMALL,
                                bg=BG_CARD, fg=FG_DIM, justify="left")
        self.dz_desc.pack(anchor="w", pady=(0, 8))

        # LT Slider
        row_lt = tk.Frame(self.card_dz, bg=BG_CARD)
        row_lt.pack(fill="x", pady=3)
        self.lt_lbl_title = tk.Label(row_lt, text=T("trig_dz_lt"), font=FONT_LABEL,
                                     bg=BG_CARD, fg=FG_TEXT, width=22, anchor="w")
        self.lt_lbl_title.pack(side="left")
        self.lt_var = tk.IntVar(value=settings.left_trigger_deadzone)
        ttk.Scale(row_lt, from_=0, to=100, variable=self.lt_var, orient="horizontal",
                  command=self._on_lt).pack(side="left", fill="x", expand=True, padx=6)
        self.lt_lbl = tk.Label(row_lt, text=str(settings.left_trigger_deadzone),
                               font=FONT_VALUE, bg=BG_CARD, fg=FG_ACCENT, width=4)
        self.lt_lbl.pack(side="left")

        # RT Slider
        row_rt = tk.Frame(self.card_dz, bg=BG_CARD)
        row_rt.pack(fill="x", pady=3)
        self.rt_lbl_title = tk.Label(row_rt, text=T("trig_dz_rt"), font=FONT_LABEL,
                                     bg=BG_CARD, fg=FG_TEXT, width=22, anchor="w")
        self.rt_lbl_title.pack(side="left")
        self.rt_var = tk.IntVar(value=settings.right_trigger_deadzone)
        ttk.Scale(row_rt, from_=0, to=100, variable=self.rt_var, orient="horizontal",
                  command=self._on_rt).pack(side="left", fill="x", expand=True, padx=6)
        self.rt_lbl = tk.Label(row_rt, text=str(settings.right_trigger_deadzone),
                               font=FONT_VALUE, bg=BG_CARD, fg=FG_ACCENT, width=4)
        self.rt_lbl.pack(side="left")

        # Response Curve Guide Card
        self.card_curves = tk.LabelFrame(
            self.frame, text=f"  {T('help_curves_title')}  ", font=FONT_SECTION,
            bg=BG_CARD, fg=FG_YELLOW, padx=12, pady=10,
            highlightthickness=1, highlightbackground="#25254d",
        )
        self.card_curves.pack(fill="both", expand=True)

        self.curves_text = tk.Text(
            self.card_curves, bg=BG_CARD, fg=FG_TEXT, font=FONT_HELP_BODY,
            wrap="word", relief="flat", highlightthickness=0, height=5,
        )
        self.curves_text.pack(fill="both", expand=True)
        self._fill_curves_text()

    def _on_lt(self, _v: str) -> None:
        v = int(self.lt_var.get())
        self.settings.left_trigger_deadzone = v
        self.lt_lbl.config(text=str(v))

    def _on_rt(self, _v: str) -> None:
        v = int(self.rt_var.get())
        self.settings.right_trigger_deadzone = v
        self.rt_lbl.config(text=str(v))

    def _fill_curves_text(self) -> None:
        self.curves_text.config(state="normal")
        self.curves_text.delete("1.0", "end")
        self.curves_text.insert("1.0", T("help_curves_body"))
        self.curves_text.config(state="disabled")

    def retranslate(self) -> None:
        self.card_dz.config(text=f"  {T('trig_dz_title')}  ")
        self.dz_desc.config(text=T("trig_dz_desc"))
        self.lt_lbl_title.config(text=T("trig_dz_lt"))
        self.rt_lbl_title.config(text=T("trig_dz_rt"))
        self.card_curves.config(text=f"  {T('help_curves_title')}  ")
        self._fill_curves_text()


# ---------------------------------------------------------------------------
# Tab: Rich Tips, Diagnostics & Hall Effect Guide
# ---------------------------------------------------------------------------
class HelpTab:
    """Tab 3: Comprehensive troubleshooting, quickstart, and Hall Effect vs Potentiometers."""

    def __init__(self, parent: tk.Widget) -> None:
        self.frame = tk.Frame(parent, bg=BG_TAB, padx=10, pady=8)

        self.text = tk.Text(
            self.frame, bg=BG_TAB, fg=FG_TEXT, font=FONT_HELP_BODY,
            wrap="word", relief="flat", padx=12, pady=8, height=9,
            highlightthickness=0, selectbackground="#2a2a5e",
        )
        scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.text.pack(fill="both", expand=True)

        self.text.tag_configure("header1", font=("Segoe UI", 11, "bold"), foreground=FG_ACCENT)
        self.text.tag_configure("header2", font=("Segoe UI", 10, "bold"), foreground=FG_YELLOW)
        self.text.tag_configure("body", font=("Segoe UI", 9), foreground=FG_TEXT)
        self.text.tag_configure("dim", font=("Segoe UI", 8), foreground=FG_DIM)

        self._fill()

    def _fill(self) -> None:
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        sections = [
            ("help_quickstart_title", "help_quickstart_body", "header1"),
            ("help_hall_title",       "help_hall_body",       "header2"),
        ]
        for title_k, body_k, tag in sections:
            self.text.insert("end", T(title_k) + "\n", tag)
            self.text.insert("end", "—" * 60 + "\n", "dim")
            self.text.insert("end", T(body_k) + "\n\n\n", "body")

        self.text.config(state="disabled")

    def retranslate(self) -> None:
        self._fill()


# ---------------------------------------------------------------------------
# Tab: Virtual Controller Guide & HidHide
# ---------------------------------------------------------------------------
class VirtualGuideTab:
    """Tab 4: How the virtual gamepad operates, driver downloads, and HidHide dual-input guide."""

    def __init__(self, parent: tk.Widget) -> None:
        self.frame = tk.Frame(parent, bg=BG_TAB, padx=10, pady=8)

        self.text = tk.Text(
            self.frame, bg=BG_TAB, fg=FG_TEXT, font=FONT_HELP_BODY,
            wrap="word", relief="flat", padx=12, pady=8, height=9,
            highlightthickness=0, selectbackground="#2a2a5e",
        )
        scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.text.pack(fill="both", expand=True)

        self.text.tag_configure("header", font=("Segoe UI", 11, "bold"), foreground=FG_ACCENT)
        self.text.tag_configure("body", font=("Segoe UI", 9), foreground=FG_TEXT)
        self.text.tag_configure("dim", font=("Segoe UI", 8), foreground=FG_DIM)

        self._fill()

    def _fill(self) -> None:
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end", T("help_virtual_title") + "\n", "header")
        self.text.insert("end", "—" * 60 + "\n", "dim")
        self.text.insert("end", T("help_virtual_body") + "\n", "body")
        self.text.config(state="disabled")

    def retranslate(self) -> None:
        self._fill()


# ---------------------------------------------------------------------------
# Main Application Window
# ---------------------------------------------------------------------------
class App:
    """Main application orchestrator."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(T("app_title"))
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)
        self.root.minsize(940, 720)

        # Style ttk components
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TScale", background=BG_TAB, troughcolor="#1e1e38")
        style.configure("TCombobox", fieldbackground="#1f1f3a", foreground=FG_TEXT,
                        darkcolor="#2d2d55", lightcolor="#2d2d55")
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_BTN_DEFAULT, foreground=FG_DIM,
                        padding=[14, 5], font=FONT_BUTTON)
        style.map("TNotebook.Tab",
                  background=[("selected", BG_TAB)],
                  foreground=[("selected", FG_ACCENT)])

        # Engine state
        self.settings = CalibrationSettings()
        self.reader = XInputReader()
        self.controller_index: int | None = None
        self.virtual: VirtualGamepad | None = None
        self.virtual_active = False
        self._running = True

        # Exponential moving average noise filters
        self._left_filter = NoiseFilter()
        self._right_filter = NoiseFilter()

        self._build_ui()
        self._find_controller()

        # Center on user display
        self.root.update_idletasks()
        w = max(960, self.root.winfo_width())
        h = max(760, self.root.winfo_height())
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = max(10, (sh - h) // 2 - 20)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.attributes("-topmost", True)
        self.root.after(500, lambda: self.root.attributes("-topmost", False))
        self.root.lift()
        self.root.focus_force()

        # Start 60fps frame loop
        self._tick()

    # -- UI Construction -----------------------------------------------------
    def _build_ui(self) -> None:
        # ==== Header Bar ====
        header = tk.Frame(self.root, bg=BG_HEADER, padx=12, pady=6,
                          highlightthickness=1, highlightbackground="#202042")
        header.pack(fill="x")

        # 10-Language Selector (Combobox)
        self.lang_code_var = tk.StringVar(value=get_language())
        lang_dict = dict(get_languages())
        self.lang_display_var = tk.StringVar(value=lang_dict.get(get_language(), "🇧🇷 Português"))

        self.lang_combo = ttk.Combobox(
            header, textvariable=self.lang_display_var,
            values=[name for _, name in get_languages()],
            width=14, state="readonly",
        )
        self.lang_combo.pack(side="left")
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_lang_combo_select)

        # Power Off Controller Button
        self.btn_power_off = tk.Button(
            header, text=T("power_off_btn"), font=FONT_BUTTON,
            bg="#3b1115", fg="#fca5a5", activebackground="#7f1d1d",
            relief="flat", padx=10, pady=2, cursor="hand2",
            command=self._power_off,
        )
        self.btn_power_off.pack(side="left", padx=(8, 0))

        # Connection status label
        self.status_label = tk.Label(
            header, text=T("searching"), font=FONT_SECTION,
            bg=BG_HEADER, fg=FG_YELLOW,
        )
        self.status_label.pack(side="left", padx=(12, 0))

        # DLL indicator
        self.dll_label = tk.Label(
            header, text=f"XInput: {self.reader.dll_name}",
            font=FONT_SMALL, bg=BG_HEADER, fg=FG_DIM,
        )
        self.dll_label.pack(side="right")

        # ==== Top Area: Left Stick + Center (Triggers/Buttons) + Right Stick ====
        top_area = tk.Frame(self.root, bg=BG_DARK, padx=8, pady=4)
        top_area.pack(fill="x")

        # Left Radar
        self.left_canvas = StickCanvas(top_area, "left_stick", size=200)
        self.left_canvas.frame.pack(side="left", padx=(0, 4), pady=2)

        # Center Column (Unified Controller Display)
        center_col = tk.Frame(top_area, bg=BG_DARK)
        center_col.pack(side="left", fill="both", expand=True, padx=4)

        # Single Unified Controller Panel (Physical Xbox 360 Layout)
        self.btn_panel = ControllerPanel(center_col)
        self.btn_panel.frame.pack(fill="both", expand=True, pady=(2, 2))

        # Direct references for tick processing & backward compatibility
        self.lt_bar = self.btn_panel.lt_unit
        self.rt_bar = self.btn_panel.rt_unit
        self.trig_frame = self.btn_panel.frame

        # Right Radar
        self.right_canvas = StickCanvas(top_area, "right_stick", size=200)
        self.right_canvas.frame.pack(side="right", padx=(4, 0), pady=2)

        # ==== Middle/Lower Area: Rich Notebook with Tabs ====
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=(4, 4))

        # Tab 1: Stick Calibration (Both sticks side-by-side)
        tab_sticks = tk.Frame(self.notebook, bg=BG_TAB, padx=8, pady=6)
        self.notebook.add(tab_sticks, text=T("tab_sticks"))

        sticks_row = tk.Frame(tab_sticks, bg=BG_TAB)
        sticks_row.pack(fill="both", expand=True)

        self.left_cal = StickCalibrationPanel(
            sticks_row, "cal_left_title", self.settings.left_stick,
        )
        self.left_cal.frame.pack(side="left", fill="both", expand=True, padx=(0, 4))

        self.right_cal = StickCalibrationPanel(
            sticks_row, "cal_right_title", self.settings.right_stick,
        )
        self.right_cal.frame.pack(side="right", fill="both", expand=True, padx=(4, 0))

        # Tab 2: Triggers & Curves
        self.trig_tab = TriggersTab(self.notebook, self.settings)
        self.notebook.add(self.trig_tab.frame, text=T("tab_triggers"))

        # Tab 3: Tips & Hall Effect
        self.help_tab = HelpTab(self.notebook)
        self.notebook.add(self.help_tab.frame, text=T("tab_help"))

        # Tab 4: Virtual Gamepad & Games
        self.virtual_tab = VirtualGuideTab(self.notebook)
        self.notebook.add(self.virtual_tab.frame, text=T("tab_virtual"))

        # ==== Footer Toolbar ====
        footer = tk.Frame(self.root, bg=BG_HEADER, padx=12, pady=8,
                          highlightthickness=1, highlightbackground="#202042")
        footer.pack(fill="x", side="bottom")

        # Virtual Controller Toggle
        vg_text = T("activate_virtual") if VGAMEPAD_AVAILABLE else T("install_vgamepad")
        vg_bg = "#166534" if VGAMEPAD_AVAILABLE else "#854d0e"

        self.btn_virtual = tk.Button(
            footer, text=vg_text, font=FONT_BUTTON,
            bg=vg_bg, fg="white", activebackground="#15803d",
            relief="flat", padx=16, pady=5, cursor="hand2",
            command=self._toggle_virtual,
        )
        self.btn_virtual.pack(side="left")

        self.virtual_status = tk.Label(
            footer, text="", font=FONT_SMALL, bg=BG_HEADER, fg=FG_DIM,
        )
        self.virtual_status.pack(side="left", padx=10)

        # Profile Actions (Right)
        btn_kw = dict(font=FONT_BUTTON, relief="flat", padx=12, pady=5, cursor="hand2")

        self.btn_load = tk.Button(
            footer, text=T("load"), bg=BG_BTN_DEFAULT, fg=FG_TEXT,
            activebackground=BG_BTN_HOVER, command=self._load_profile, **btn_kw,
        )
        self.btn_load.pack(side="right", padx=3)

        self.btn_save = tk.Button(
            footer, text=T("save"), bg=BG_BTN_DEFAULT, fg=FG_TEXT,
            activebackground=BG_BTN_HOVER, command=self._save_profile, **btn_kw,
        )
        self.btn_save.pack(side="right", padx=3)

        self.btn_recon = tk.Button(
            footer, text=T("reconnect"), bg=BG_BTN_DEFAULT, fg=FG_TEXT,
            activebackground=BG_BTN_HOVER, command=self._find_controller, **btn_kw,
        )
        self.btn_recon.pack(side="right", padx=3)

    # -- Language Selection --------------------------------------------------
    def _on_lang_combo_select(self, _event: object = None) -> None:
        selected_display = self.lang_display_var.get()
        for code, display in get_languages():
            if display == selected_display:
                set_language(code)
                break
        self._retranslate_all()

    def _toggle_lang(self) -> None:
        toggle_language()
        self._retranslate_all()

    def _retranslate_all(self) -> None:
        self.root.title(T("app_title"))
        lang_dict = dict(get_languages())
        self.lang_display_var.set(lang_dict.get(get_language(), "🌐"))
        self.btn_power_off.config(text=T("power_off_btn"))

        # Header status
        if self.controller_index is not None:
            self.status_label.config(text=T("connected", n=self.controller_index + 1))
        else:
            self.status_label.config(text=T("not_connected"))

        # Radars & center
        self.left_canvas.retranslate()
        self.right_canvas.retranslate()
        self.btn_panel.retranslate()

        # Notebook tab titles
        self.notebook.tab(0, text=T("tab_sticks"))
        self.notebook.tab(1, text=T("tab_triggers"))
        self.notebook.tab(2, text=T("tab_help"))
        self.notebook.tab(3, text=T("tab_virtual"))

        # Inner tab panels
        self.left_cal.retranslate()
        self.right_cal.retranslate()
        self.trig_tab.retranslate()
        self.help_tab.retranslate()
        self.virtual_tab.retranslate()

        # Footer
        if self.virtual_active:
            self.btn_virtual.config(text=T("deactivate_virtual"))
        elif VGAMEPAD_AVAILABLE:
            self.btn_virtual.config(text=T("activate_virtual"))
        else:
            self.btn_virtual.config(text=T("install_vgamepad"))

        self.btn_recon.config(text=T("reconnect"))
        self.btn_save.config(text=T("save"))
        self.btn_load.config(text=T("load"))

    # -- Controller Detection ------------------------------------------------
    def _find_controller(self) -> None:
        idx = self.reader.find_connected_controller()
        if idx is not None:
            self.controller_index = idx
            self.status_label.config(text=T("connected", n=idx + 1), fg=FG_GREEN)
            self._left_filter.reset()
            self._right_filter.reset()
        else:
            self.controller_index = None
            self.status_label.config(text=T("not_connected"), fg=FG_RED)

    def _power_off(self) -> None:
        idx = self.controller_index if self.controller_index is not None else 0
        success = self.reader.power_off(idx)
        if success:
            self.virtual_status.config(text=f"⏻ {T('power_off_success')}", fg=FG_YELLOW)
            self._find_controller()
        else:
            self._find_controller()

    # -- Virtual Gamepad Toggle ----------------------------------------------
    def _toggle_virtual(self) -> None:
        if self.virtual_active:
            if self.virtual:
                self.virtual.deactivate()
                self.virtual = None
            self.virtual_active = False
            self.btn_virtual.config(text=T("activate_virtual"), bg="#166534")
            self.virtual_status.config(text=T("virtual_off"), fg=FG_DIM)
            return

        if not VGAMEPAD_AVAILABLE:
            messagebox.showwarning("vgamepad", T("err_vgamepad"))
            return

        try:
            self.virtual = VirtualGamepad()
            self.virtual.activate()
            self.virtual_active = True
            self.btn_virtual.config(text=T("deactivate_virtual"), bg="#991b1b")
            self.virtual_status.config(text=T("virtual_active"), fg=FG_GREEN)
        except Exception as exc:
            msg = str(exc)
            if any(term in msg.lower() for term in ("vigem", "bus", "driver")):
                messagebox.showerror("ViGEmBus", T("err_vigem"))
            else:
                messagebox.showerror("Error", f"Error: {msg}")

    # -- Profiles Management -------------------------------------------------
    def _save_profile(self) -> None:
        fp = filedialog.asksaveasfilename(
            title=T("save_title"), initialdir=str(get_profile_dir()),
            defaultextension=".json", filetypes=[("JSON", "*.json"), ("All", "*.*")],
        )
        if not fp:
            return
        try:
            import os
            from pathlib import Path
            save_profile(self.settings, os.path.basename(fp),
                         profile_dir=Path(os.path.dirname(fp)))
            self.virtual_status.config(text=T("saved", f=os.path.basename(fp)), fg=FG_GREEN)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _load_profile(self) -> None:
        fp = filedialog.askopenfilename(
            title=T("load_title"), initialdir=str(get_profile_dir()),
            filetypes=[("JSON", "*.json"), ("All", "*.*")],
        )
        if not fp:
            return
        try:
            import os
            from pathlib import Path
            loaded = load_profile(os.path.basename(fp),
                                  profile_dir=Path(os.path.dirname(fp)))
            self.settings.left_stick = loaded.left_stick
            self.settings.right_stick = loaded.right_stick
            self.settings.left_trigger_deadzone = loaded.left_trigger_deadzone
            self.settings.right_trigger_deadzone = loaded.right_trigger_deadzone

            self.left_cal.load_from(self.settings.left_stick)
            self.right_cal.load_from(self.settings.right_stick)
            self.trig_tab.lt_var.set(self.settings.left_trigger_deadzone)
            self.trig_tab.rt_var.set(self.settings.right_trigger_deadzone)
            self.trig_tab.lt_lbl.config(text=str(self.settings.left_trigger_deadzone))
            self.trig_tab.rt_lbl.config(text=str(self.settings.right_trigger_deadzone))

            self._left_filter.reset()
            self._right_filter.reset()
            self.virtual_status.config(text=T("loaded", f=os.path.basename(fp)), fg=FG_GREEN)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    # -- 60fps Processing Loop -----------------------------------------------
    def _tick(self) -> None:
        if not self._running:
            return

        if self.controller_index is not None:
            state = self.reader.get_state(self.controller_index)
            if not state.connected:
                self._find_controller()
            else:
                self._process_frame(state)

        self.root.after(UPDATE_MS, self._tick)

    def _process_frame(self, state: ControllerState) -> None:
        # 1. Apply EMA noise filters to raw sticks
        flx, fly = self._left_filter.apply(
            state.left_stick_x, state.left_stick_y,
            self.settings.left_stick.noise_filter,
            self.settings.left_stick.anti_jitter,
        )
        frx, fry = self._right_filter.apply(
            state.right_stick_x, state.right_stick_y,
            self.settings.right_stick.noise_filter,
            self.settings.right_stick.anti_jitter,
        )

        # 2. Feed samplers with unfiltered signals for accurate median/peak detection
        self.left_cal.feed_sample(state.left_stick_x, state.left_stick_y)
        self.right_cal.feed_sample(state.right_stick_x, state.right_stick_y)

        # 3. Apply mathematical calibration pipeline
        clx, cly = apply_stick_calibration(flx, fly, self.settings.left_stick)
        crx, cry = apply_stick_calibration(frx, fry, self.settings.right_stick)
        clt = apply_trigger_deadzone(state.left_trigger, self.settings.left_trigger_deadzone)
        crt = apply_trigger_deadzone(state.right_trigger, self.settings.right_trigger_deadzone)

        # 4. Update real-time visual controls
        self.left_canvas.update(flx, fly, clx, cly, self.settings.left_stick.deadzone)
        self.right_canvas.update(frx, fry, crx, cry, self.settings.right_stick.deadzone)
        self.lt_bar.update(state.left_trigger, clt)
        self.rt_bar.update(state.right_trigger, crt)
        self.btn_panel.update(state)

        # 5. Passthrough to virtual gamepad
        if self.virtual_active and self.virtual and self.virtual.is_active:
            self.virtual.update(state, clx, cly, crx, cry, clt, crt)

    # -- Lifecycle -----------------------------------------------------------
    def run(self) -> None:
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _on_close(self) -> None:
        self._running = False
        if self.virtual_active and self.virtual:
            self.virtual.deactivate()
        self.root.destroy()


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def main() -> None:
    try:
        app = App()
        app.run()
    except RuntimeError as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", str(exc))
        root.destroy()
        sys.exit(1)


if __name__ == "__main__":
    main()
