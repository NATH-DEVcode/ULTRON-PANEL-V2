#!/usr/bin/env python3
"""
ULTRON // CORE  -  GUI V2
Centro de operaciones futurista para Linux
Estética: negro + naranja | Core con anillos orbitando | Mapa plano
"""

import tkinter as tk
from tkinter import font as tkfont, colorchooser
import math
import time
import socket
import platform
import subprocess
import json
import os
import re
import threading
import shlex
import tempfile
import shutil
import urllib.request
import urllib.error
import uuid
import wave

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


# ============================================================
# PALETA ULTRON  (naranja + turquesa + verde)
# ============================================================
BG            = "#050505"
BG_PANEL      = "#0c0c0c"
BG_PANEL2     = "#111111"
ORANGE        = "#ff6b00"
ORANGE_L      = "#ff9500"
ORANGE_D      = "#cc5500"
ORANGE_DIM    = "#3a2200"
TURQUOISE     = "#00d4c8"
TURQUOISE_D   = "#008b84"
TURQUOISE_DIM = "#003d3a"
GRAY          = "#1a1a1a"
GRAY2         = "#2a2a2a"
TEXT          = "#e0e0e0"
TEXT_DIM      = "#888888"
GREEN         = "#00cc66"
RED           = "#ff3333"


# ============================================================
# SISTEMA DE APARIENCIAS / THEMES
# ============================================================
CONFIG_FILE = os.path.join(
    os.path.expanduser("~"),
    ".ultron_core_theme.json"
)

THEMES = {
    "ULTRON CLASSIC": {
        "BG": "#050505",
        "BG_PANEL": "#0c0c0c",
        "BG_PANEL2": "#111111",
        "PRIMARY": "#ff6b00",
        "PRIMARY_L": "#ff9500",
        "PRIMARY_D": "#cc5500",
        "PRIMARY_DIM": "#3a2200",
        "SECONDARY": "#00d4c8",
        "SECONDARY_D": "#008b84",
        "SECONDARY_DIM": "#003d3a",
        "TEXT": "#e0e0e0",
        "TEXT_DIM": "#888888",
        "GOOD": "#00cc66",
        "DANGER": "#ff3333",
    },

    "ULTRON CRIMSON": {
        "BG": "#040000",
        "BG_PANEL": "#100505",
        "BG_PANEL2": "#180808",
        "PRIMARY": "#ff2a2a",
        "PRIMARY_L": "#ff5c5c",
        "PRIMARY_D": "#a90000",
        "PRIMARY_DIM": "#3b0707",
        "SECONDARY": "#ffb000",
        "SECONDARY_D": "#b26f00",
        "SECONDARY_DIM": "#4a2c00",
        "TEXT": "#f2e8e8",
        "TEXT_DIM": "#9b8080",
        "GOOD": "#56e39f",
        "DANGER": "#ff3030",
    },

    "STARK ARC": {
        "BG": "#020609",
        "BG_PANEL": "#071018",
        "BG_PANEL2": "#0b1722",
        "PRIMARY": "#00bfff",
        "PRIMARY_L": "#65dcff",
        "PRIMARY_D": "#0074a6",
        "PRIMARY_DIM": "#003346",
        "SECONDARY": "#ffffff",
        "SECONDARY_D": "#8aa8b8",
        "SECONDARY_DIM": "#263844",
        "TEXT": "#e8f7ff",
        "TEXT_DIM": "#7892a3",
        "GOOD": "#00e690",
        "DANGER": "#ff4655",
    },

    "VOID PROTOCOL": {
        "BG": "#030304",
        "BG_PANEL": "#0b0b10",
        "BG_PANEL2": "#11111a",
        "PRIMARY": "#8d5cff",
        "PRIMARY_L": "#b094ff",
        "PRIMARY_D": "#5d35bc",
        "PRIMARY_DIM": "#21143e",
        "SECONDARY": "#2ef2d0",
        "SECONDARY_D": "#169f8a",
        "SECONDARY_DIM": "#083f37",
        "TEXT": "#eeeaff",
        "TEXT_DIM": "#8b849f",
        "GOOD": "#48f08b",
        "DANGER": "#ff476f",
    },

    "NIGHT VISION": {
        "BG": "#010401",
        "BG_PANEL": "#061006",
        "BG_PANEL2": "#0a170a",
        "PRIMARY": "#38ff66",
        "PRIMARY_L": "#8dffa7",
        "PRIMARY_D": "#169a35",
        "PRIMARY_DIM": "#0b3914",
        "SECONDARY": "#b7ff00",
        "SECONDARY_D": "#6c9600",
        "SECONDARY_DIM": "#273700",
        "TEXT": "#dcffe3",
        "TEXT_DIM": "#6f9477",
        "GOOD": "#57ff80",
        "DANGER": "#ff4a4a",
    },
}


def load_theme_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return {"theme": "ULTRON CLASSIC"}


def save_theme_config(data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def apply_theme_globals(theme_data):
    global BG, BG_PANEL, BG_PANEL2
    global ORANGE, ORANGE_L, ORANGE_D, ORANGE_DIM
    global TURQUOISE, TURQUOISE_D, TURQUOISE_DIM
    global TEXT, TEXT_DIM, GREEN, RED

    BG = theme_data["BG"]
    BG_PANEL = theme_data["BG_PANEL"]
    BG_PANEL2 = theme_data["BG_PANEL2"]

    ORANGE = theme_data["PRIMARY"]
    ORANGE_L = theme_data["PRIMARY_L"]
    ORANGE_D = theme_data["PRIMARY_D"]
    ORANGE_DIM = theme_data["PRIMARY_DIM"]

    TURQUOISE = theme_data["SECONDARY"]
    TURQUOISE_D = theme_data["SECONDARY_D"]
    TURQUOISE_DIM = theme_data["SECONDARY_DIM"]

    TEXT = theme_data["TEXT"]
    TEXT_DIM = theme_data["TEXT_DIM"]
    GREEN = theme_data["GOOD"]
    RED = theme_data["DANGER"]


_THEME_CFG = load_theme_config()
_THEME_NAME = _THEME_CFG.get("theme", "ULTRON CLASSIC")

if _THEME_NAME == "CUSTOM":
    custom = _THEME_CFG.get("custom_theme")
    if isinstance(custom, dict):
        apply_theme_globals(custom)
else:
    apply_theme_globals(THEMES.get(_THEME_NAME, THEMES["ULTRON CLASSIC"]))


def run_cmd(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "No disponible"


class UltronCore:
    def __init__(self, canvas, cx, cy, base_radius=110, on_activate=None):
        self.canvas = canvas
        self.cx = cx
        self.cy = cy
        self.base_r = base_radius
        self.on_activate = on_activate
        self.angle = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.base_speed = [0.35, -0.22, 0.48, -0.15, 0.28]
        self.speed = list(self.base_speed)
        self.state = "IDLE"
        self.pulse_phase = 0.0
        self.rings = []
        self.items = []
        self._build()

    def _build(self):
        c = self.canvas
        cx, cy, r = self.cx, self.cy, self.base_r
        for scale in [1.55, 1.42, 1.30]:
            self.items.append(c.create_oval(cx-r*scale, cy-r*scale, cx+r*scale, cy+r*scale, outline=ORANGE_DIM, width=1, tags=("ultron_core",)))
        ring_specs = [(1.22,2,ORANGE),(1.08,3,ORANGE_L),(0.94,2,ORANGE),(0.80,3,ORANGE_L),(0.66,2,ORANGE_D)]
        for rel, width, color in ring_specs:
            self.rings.append(c.create_arc(cx-r*rel, cy-r*rel, cx+r*rel, cy+r*rel, start=0, extent=300, style=tk.ARC, outline=color, width=width, tags=("ultron_core",)))
            self.rings.append(c.create_arc(cx-r*rel, cy-r*rel, cx+r*rel, cy+r*rel, start=180, extent=120, style=tk.ARC, outline=ORANGE_D, width=max(1,width-1), tags=("ultron_core",)))
        self.outer_core = c.create_oval(cx-r*0.48, cy-r*0.48, cx+r*0.48, cy+r*0.48, fill="#1a0a00", outline=ORANGE_D, width=2, tags=("ultron_core","core_click"))
        self.mid_core = c.create_oval(cx-r*0.38, cy-r*0.38, cx+r*0.38, cy+r*0.38, fill="#2a1200", outline=ORANGE, width=1, tags=("ultron_core","core_click"))
        self.inner_core = c.create_oval(cx-r*0.18, cy-r*0.18, cx+r*0.18, cy+r*0.18, fill=ORANGE, outline=ORANGE_L, width=1, tags=("ultron_core","core_click"))
        self.center_core = c.create_oval(cx-r*0.08, cy-r*0.08, cx+r*0.08, cy+r*0.08, fill=ORANGE_L, outline="", tags=("ultron_core","core_click"))
        for deg in range(0,360,30):
            rad=math.radians(deg)
            x1=cx+math.cos(rad)*r*0.52; y1=cy+math.sin(rad)*r*0.52
            x2=cx+math.cos(rad)*r*0.58; y2=cy+math.sin(rad)*r*0.58
            c.create_line(x1,y1,x2,y2,fill=ORANGE_D,width=1,tags=("ultron_core",))
        self.state_text=c.create_text(cx,cy+r*0.72,text="● IDLE  /  CLICK CORE",fill=TEXT_DIM,font=("Consolas",9),tags=("ultron_core",))
        c.create_oval(cx-r*0.52, cy-r*0.52, cx+r*0.52, cy+r*0.52, fill="", outline="", tags=("core_click",))
        c.tag_bind("core_click","<Button-1>",self._handle_click)
        c.tag_bind("core_click","<Enter>",self._handle_enter)
        c.tag_bind("core_click","<Leave>",self._handle_leave)
        self._apply_state_style()

    def _handle_click(self, _event=None):
        if callable(self.on_activate): self.on_activate()
    def _handle_enter(self, _event=None):
        self.canvas.configure(cursor="hand2")
        if self.state=="IDLE":
            self.canvas.itemconfig(self.inner_core, outline=TURQUOISE, width=2)
            self.canvas.itemconfig(self.state_text, fill=TURQUOISE)
    def _handle_leave(self, _event=None):
        self.canvas.configure(cursor="")
        self._apply_state_style()
    def set_state(self,state):
        state=str(state).upper().strip()
        if state not in {"IDLE","LISTENING","THINKING","SPEAKING"}: state="IDLE"
        self.state=state
        self.speed={
            "IDLE":list(self.base_speed),
            "LISTENING":[0.55,-0.36,0.66,-0.25,0.42],
            "THINKING":[1.20,-0.90,1.45,-0.72,1.00],
            "SPEAKING":[0.70,-0.45,0.82,-0.32,0.55],
        }[state]
        self._apply_state_style()
    def _apply_state_style(self):
        styles={
            "IDLE":(ORANGE,ORANGE_L,ORANGE_D,"● IDLE  /  CLICK CORE"),
            "LISTENING":(TURQUOISE,"#75fff7",TURQUOISE_D,"● LISTENING"),
            "THINKING":(ORANGE_L,"#ffd166",ORANGE,"● THINKING"),
            "SPEAKING":(GREEN,"#8cffbd",TURQUOISE,"● SPEAKING"),
        }
        primary,bright,dim,label=styles[self.state]
        self.canvas.itemconfig(self.outer_core,outline=dim)
        self.canvas.itemconfig(self.mid_core,outline=primary,fill=BG_PANEL2)
        self.canvas.itemconfig(self.inner_core,fill=primary,outline=bright,width=2 if self.state!="IDLE" else 1)
        self.canvas.itemconfig(self.center_core,fill=bright)
        self.canvas.itemconfig(self.state_text,text=label,fill=primary if self.state!="IDLE" else TEXT_DIM)
    def _animate_pulse(self):
        self.pulse_phase+=0.14
        amount={"IDLE":0.012,"LISTENING":0.055,"THINKING":0.025,"SPEAKING":0.075}[self.state]
        pulse=1.0+math.sin(self.pulse_phase)*amount
        cx,cy,r=self.cx,self.cy,self.base_r
        inner_r=r*0.18*pulse
        center_r=r*0.08*(1.0+math.sin(self.pulse_phase*1.35)*amount*1.6)
        self.canvas.coords(self.inner_core,cx-inner_r,cy-inner_r,cx+inner_r,cy+inner_r)
        self.canvas.coords(self.center_core,cx-center_r,cy-center_r,cx+center_r,cy+center_r)
    def animate(self):
        for i,ring_id in enumerate(self.rings):
            idx=i//2
            self.angle[idx]=(self.angle[idx]+self.speed[idx])%360
            start=self.angle[idx] if i%2==0 else (self.angle[idx]+180)%360
            extent=280 if i%2==0 else 90
            self.canvas.itemconfig(ring_id,start=start,extent=extent)
        self._animate_pulse()


class UltronGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ULTRON // CORE")
        self.root.configure(bg=BG)
        self.root.geometry("1400x900")
        self.root.minsize(1100, 720)

        self.font_title = tkfont.Font(family="Segoe UI", size=14, weight="bold")
        self.font_label = tkfont.Font(family="Segoe UI", size=10)
        self.font_small = tkfont.Font(family="Segoe UI", size=9)
        self.font_mono  = tkfont.Font(family="Consolas", size=9)

        # CONCIENCIA / IA
        self.ai_history = [
            {
                "role": "system",
                "content": (
                    "Eres ULTRON, la conciencia integrada de un panel Linux llamado "
                    "ULTRON CORE. Habla en español de forma natural, clara y concisa. "
                    "No digas que eres Groq ni que eres otro asistente. "
                    "Si no sabes algo, dilo. No inventes resultados del sistema."
                )
            }
        ]
        self.ai_busy = False
        self.consciousness_active = False
        self.tts_process = None
        self.voice_record_seconds = 12
        self.voice_silence_seconds = 0.9
        self.live_transcript_var = tk.StringVar(value="")
        self.audio_input_device = None
        self.audio_output_device = None
        self.ultron_volume = 70

        self._build_ui()
        self._start_animation()
        self._update_metrics()

    def _build_ui(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

        top = tk.Frame(main, bg=BG, height=42)
        top.pack(fill=tk.X, pady=(0, 8))
        top.pack_propagate(False)

        tk.Label(top, text="ULTRON // CORE", font=self.font_title,
                 fg=ORANGE, bg=BG).pack(side=tk.LEFT, padx=8)

        self.status_label = tk.Label(
            top, text="● SYSTEM ONLINE",
            font=self.font_small, fg=TURQUOISE, bg=BG
        )
        self.status_label.pack(side=tk.RIGHT, padx=12)

        mid = tk.Frame(main, bg=BG)
        mid.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(mid, bg=BG_PANEL, width=280)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)
        self._build_left_panel(left)

        center = tk.Frame(mid, bg=BG)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.core_canvas = tk.Canvas(center, bg=BG, highlightthickness=0)
        self.core_canvas.pack(fill=tk.BOTH, expand=True)

        self.live_transcript_label = tk.Label(
            center,
            textvariable=self.live_transcript_var,
            font=self.font_mono,
            fg=TEXT,
            bg=BG,
            wraplength=520,
            justify="center"
        )
        self.live_transcript_label.pack(fill=tk.X, padx=10, pady=(2, 4))

        right = tk.Frame(mid, bg=BG_PANEL, width=320)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right.pack_propagate(False)
        self._build_right_panel(right)

        bottom = tk.Frame(main, bg=BG, height=210)
        bottom.pack(fill=tk.X, pady=(10, 0))
        bottom.pack_propagate(False)
        self._build_bottom(bottom)

        self.root.after(80, self._init_core)

    def _build_left_panel(self, parent):
        header = tk.Frame(parent, bg=BG_PANEL2, height=36)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="SYSTEM STATUS", font=self.font_small,
                 fg=ORANGE, bg=BG_PANEL2).pack(side=tk.LEFT, padx=12, pady=8)

        items = [
            ("Security Level", "HIGH", GREEN),
            ("External Access", "MONITORED", TURQUOISE),
            ("Network Status", "RESTRICTED", ORANGE_L),
            ("User Privileges", "STANDARD", TEXT_DIM),
            ("System Shield", "ACTIVE", GREEN),
            ("Kernel", self._get_hostname(), TEXT),
            ("Arch", platform.machine(), TEXT),
        ]

        for label, value, color in items:
            row = tk.Frame(parent, bg=BG_PANEL, height=36)
            row.pack(fill=tk.X, padx=8, pady=2)
            row.pack_propagate(False)
            tk.Label(row, text=label, font=self.font_small,
                     fg=TEXT_DIM, bg=BG_PANEL, anchor="w").pack(side=tk.LEFT, padx=6)
            tk.Label(row, text=value, font=self.font_small,
                     fg=color, bg=BG_PANEL, anchor="e").pack(side=tk.RIGHT, padx=6)

        tk.Frame(parent, bg=GRAY2, height=1).pack(fill=tk.X, padx=10, pady=10)

        tk.Frame(parent, bg=GRAY2, height=1).pack(fill=tk.X, padx=10, pady=8)

        # MODULES con scroll (para que quepan los 8)

        tk.Label(parent, text="MODULES", font=self.font_small,
                 fg=ORANGE, bg=BG_PANEL).pack(anchor="w", padx=14, pady=(0, 4))

        modules_container = tk.Frame(parent, bg=BG_PANEL, height=108)
        modules_container.pack(fill=tk.X, padx=4, pady=2)
        modules_container.pack_propagate(False)

        canvas = tk.Canvas(modules_container, bg=BG_PANEL, highlightthickness=0)
        scrollbar = tk.Scrollbar(
            modules_container, orient="vertical", command=canvas.yview,
            bg=BG_PANEL2, troughcolor=BG_PANEL, activebackground=ORANGE_D
        )
        scroll_frame = tk.Frame(canvas, bg=BG_PANEL)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            # Scroll solo cuando el cursor está sobre el panel de módulos.
            if getattr(event, "delta", 0):
                canvas.yview_scroll(int(-2 * (event.delta / 120)), "units")
            elif getattr(event, "num", None) == 4:
                canvas.yview_scroll(-2, "units")
            elif getattr(event, "num", None) == 5:
                canvas.yview_scroll(2, "units")

        def _bind_module_scroll(_event=None):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_mousewheel)
            canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbind_module_scroll(_event=None):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        # El scroll se activa únicamente mientras el mouse está encima.
        canvas.bind("<Enter>", _bind_module_scroll)
        canvas.bind("<Leave>", _unbind_module_scroll)
        scroll_frame.bind("<Enter>", _bind_module_scroll)
        scroll_frame.bind("<Leave>", _unbind_module_scroll)

        modules = [
            ("01  CONCIENCIA", self._on_ai),
            ("02  SISTEMA", self._on_system),
            ("03  PREFERENCIAS", self._on_appearance),
            ("04  RED", self._on_network),
            ("05  SEGURIDAD", self._on_security),
            ("06  ARCHIVOS", self._on_files),
            ("07  HERRAMIENTAS", self._on_tools),
            ("08  DIAGNOSTICO", self._on_diagnostics),
            ("09  PAQUETES", self._on_packages),
            ("10  CHAT WIFI", self._on_chat),
        ]

        for name, cmd in modules:
            frame = tk.Frame(
                scroll_frame, bg=BG_PANEL,
                highlightbackground=ORANGE_D, highlightthickness=1
            )
            frame.pack(fill=tk.X, padx=6, pady=3)

            btn = tk.Button(
                frame, text=name, font=self.font_small,
                fg=ORANGE, bg=BG_PANEL2,
                activeforeground=ORANGE_L, activebackground=GRAY,
                relief=tk.FLAT, bd=0, cursor="hand2",
                command=cmd, padx=12, pady=7, anchor="w"
            )
            btn.pack(fill=tk.X)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=GRAY, fg=ORANGE_L))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BG_PANEL2, fg=ORANGE))

    def _build_right_panel(self, parent):
        header = tk.Frame(parent, bg=BG_PANEL2, height=36)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="THREAT LEVEL", font=self.font_small,
                 fg=ORANGE, bg=BG_PANEL2).pack(side=tk.LEFT, padx=12, pady=8)
        tk.Label(header, text="CONTROLLED", font=self.font_small,
                 fg=TURQUOISE, bg=BG_PANEL2).pack(side=tk.RIGHT, padx=12, pady=8)

        self.map_canvas = tk.Canvas(
            parent, bg="#080808", highlightthickness=0, height=280
        )
        self.map_canvas.pack(fill=tk.X, padx=8, pady=8)
        self.root.after(100, self._draw_map)

        live = tk.Frame(parent, bg=BG_PANEL)
        live.pack(fill=tk.X, padx=10, pady=4)
        tk.Label(live, text="● LIVE MONITORING", font=self.font_small,
                 fg=TURQUOISE, bg=BG_PANEL).pack(side=tk.LEFT)

        proto = tk.Frame(parent, bg=BG_PANEL)
        proto.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(proto, text="PROTOCOL STATUS", font=self.font_small,
                 fg=TEXT_DIM, bg=BG_PANEL).pack(anchor="w")

        status_row = tk.Frame(proto, bg=BG_PANEL)
        status_row.pack(fill=tk.X, pady=6)

        for name, color in [
            ("SHIELD", GREEN), ("LOCK", TURQUOISE),
            ("LINK", ORANGE), ("AUTH", GREEN), ("KEY", TURQUOISE)
        ]:
            lbl = tk.Label(
                status_row, text=name, font=self.font_small,
                fg=color, bg=BG_PANEL2, padx=8, pady=3
            )
            lbl.pack(side=tk.LEFT, padx=3)

    def _draw_map(self):
        c = self.map_canvas
        c.delete("all")
        h = c.winfo_height() or 270

        na   = [25,70, 55,55, 85,60, 95,85, 80,120, 60,135, 35,125, 20,100]
        sa   = [50,145, 75,140, 85,170, 80,210, 60,230, 40,215, 35,180, 45,155]
        eu   = [130,55, 155,50, 170,65, 165,90, 145,95, 125,80]
        af   = [135,105, 165,100, 180,130, 175,175, 155,200, 130,190, 120,150, 130,120]
        asia = [175,45, 230,35, 275,50, 285,80, 270,110, 240,120, 200,105, 180,75]
        oc   = [240,145, 270,140, 280,160, 265,175, 245,170]

        for poly in [na, sa, eu, af, asia, oc]:
            c.create_polygon(poly, outline="#1f1f1f", fill="#0e0e0e", width=1)
            c.create_polygon(poly, outline=TURQUOISE_DIM, fill="", width=1)

        nodes = [
            (50, 95), (60, 185), (145, 75), (150, 155),
            (235, 70), (255, 155), (210, 95),
        ]
        connections = [
            (0, 2), (0, 3), (1, 3), (2, 4), (2, 3),
            (3, 5), (4, 5), (4, 6), (2, 6), (0, 4),
        ]

        for a, b in connections:
            x1, y1 = nodes[a]
            x2, y2 = nodes[b]
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2 - 22
            points = []
            for j in range(15):
                t = j / 14
                px = (1-t)**2 * x1 + 2*(1-t)*t * mx + t**2 * x2
                py = (1-t)**2 * y1 + 2*(1-t)*t * my + t**2 * y2
                points.extend([px, py])
            c.create_line(*points, fill=ORANGE, width=1.6, smooth=True)

        for x, y in nodes:
            c.create_oval(x-5, y-5, x+5, y+5, fill=ORANGE, outline=ORANGE_L, width=1)
            c.create_oval(x-2, y-2, x+2, y+2, fill=ORANGE_L, outline="")

        c.create_text(
            10, h - 14, text="GLOBAL LINKS  •  FIXED",
            anchor="w", fill=TEXT_DIM, font=self.font_small
        )

    def _build_bottom(self, parent):
        metrics = tk.Frame(parent, bg=BG)
        metrics.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        tk.Label(metrics, text="SYSTEM METRICS", font=self.font_small,
                 fg=ORANGE, bg=BG).pack(anchor="w", padx=4, pady=(0, 4))

        cards = tk.Frame(metrics, bg=BG)
        cards.pack(fill=tk.X)

        self.metric_vars = {}
        for key, label in [
            ("cpu", "CPU"), ("ram", "MEMORY"),
            ("disk", "DISK"), ("net", "NETWORK")
        ]:
            card = tk.Frame(cards, bg=BG_PANEL, width=120, height=70)
            card.pack(side=tk.LEFT, padx=4, pady=2)
            card.pack_propagate(False)
            tk.Label(card, text=label, font=self.font_small,
                     fg=TEXT_DIM, bg=BG_PANEL).pack(pady=(8, 0))
            var = tk.StringVar(value="-- %")
            self.metric_vars[key] = var
            tk.Label(card, textvariable=var, font=self.font_title,
                     fg=ORANGE, bg=BG_PANEL).pack()

        logs_frame = tk.Frame(parent, bg=BG_PANEL, width=520)
        logs_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(8, 0))
        logs_frame.pack_propagate(False)

        log_header = tk.Frame(logs_frame, bg=BG_PANEL2, height=28)
        log_header.pack(fill=tk.X)
        log_header.pack_propagate(False)
        tk.Label(log_header, text="SYSTEM LOGS", font=self.font_small,
                 fg=ORANGE, bg=BG_PANEL2).pack(side=tk.LEFT, padx=10, pady=4)
        tk.Label(log_header, text="● LIVE", font=self.font_small,
                 fg=GREEN, bg=BG_PANEL2).pack(side=tk.RIGHT, padx=10, pady=4)

        self.log_text = tk.Text(
            logs_frame, bg="#080808", fg=TEXT_DIM, font=self.font_mono,
            relief=tk.FLAT, height=8, state=tk.DISABLED,
            insertbackground=ORANGE, selectbackground=ORANGE_D
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self._add_log("ULTRON CORE initialized")
        self._add_log("Loading system modules...")
        self._add_log("Network interfaces scanned")
        self._add_log("Security shield active")
        self._add_log("All systems nominal")

    def _init_core(self):
        self.core_canvas.update_idletasks()
        w = self.core_canvas.winfo_width()
        h = self.core_canvas.winfo_height()
        cx, cy = w // 2, h // 2
        self.core = UltronCore(
            self.core_canvas, cx, cy,
            base_radius=min(w, h) // 3.2,
            on_activate=self._activate_consciousness
        )

    def _set_consciousness_state(self, state, top_text=None, color=None):
        """Actualiza el Core desde el hilo principal de Tkinter."""
        if hasattr(self, "core"):
            self.core.set_state(state)

        if top_text:
            self.status_label.configure(
                text=top_text,
                fg=color or TURQUOISE
            )

    def _activate_consciousness(self):
        """
        Un clic activa CONCIENCIA de forma continua.
        Otro clic la desactiva.
        Mientras está activa: escucha -> piensa -> habla -> vuelve a escuchar.
        """
        if not hasattr(self, "core"):
            return

        if self.consciousness_active:
            self.consciousness_active = False
            self._stop_speaking()
            self.ai_busy = False
            self._set_live_text("")
            self._set_consciousness_state(
                "IDLE",
                "● SYSTEM ONLINE",
                TURQUOISE
            )
            self._add_log("CONCIENCIA desactivada")
            return

        self.consciousness_active = True
        self._add_log("CONCIENCIA activada")
        self._begin_continuous_listening()

    def _begin_continuous_listening(self):
        if not self.consciousness_active or self.ai_busy:
            return

        self.ai_busy = True
        self._set_live_text("")
        self._set_consciousness_state(
            "LISTENING",
            "● CONCIENCIA ACTIVA",
            TURQUOISE
        )

        threading.Thread(
            target=self._voice_cycle,
            daemon=True
        ).start()

    def _set_live_text(self, text):
        self.root.after(0, lambda t=text: self.live_transcript_var.set(t))

    def _record_until_silence(self, wav_path):
        """Graba hasta detectar una pausa después de que el usuario hable."""
        source = self._resolve_input_device()
        cmd = ["parecord"]
        if source:
            cmd.append(f"--device={source}")
        cmd.extend(["--raw", "--format=s16le", "--rate=16000", "--channels=1"])

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rate = 16000
        sample_width = 2
        chunk_ms = 100
        chunk_bytes = int(rate * sample_width * chunk_ms / 1000)
        max_chunks = int(self.voice_record_seconds * 1000 / chunk_ms)
        silence_needed = max(1, int(self.voice_silence_seconds * 1000 / chunk_ms))

        frames = []
        started = False
        silent = 0
        threshold = 450

        try:
            for _ in range(max_chunks):
                data = proc.stdout.read(chunk_bytes)
                if not data:
                    break
                frames.append(data)
                samples = memoryview(data).cast("h")
                level = int(
                    (sum(sample * sample for sample in samples) / len(samples)) ** 0.5
                ) if samples else 0

                if level >= threshold:
                    started = True
                    silent = 0
                elif started:
                    silent += 1
                    if silent >= silence_needed:
                        break

            if not started:
                raise RuntimeError(
                    "No detecté voz. Revisa el micrófono en Preferencias > Audio."
                )
        finally:
            try:
                proc.terminate()
                proc.wait(timeout=1)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass

        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(b"".join(frames))

    def _animate_response_text(self, text):
        """Muestra la respuesta palabra por palabra."""
        words = text.split()
        shown = []

        def step(i=0):
            if i >= len(words):
                return
            shown.append(words[i])
            self.live_transcript_var.set("ULTRON: " + " ".join(shown))
            self.root.after(35, lambda: step(i + 1))

        self.root.after(0, step)

    def _voice_cycle(self):
        """Grabación -> Groq STT -> Groq chat -> voz local."""
        wav_path = None

        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "No encuentro GROQ_API_KEY en el entorno. "
                    "Abre ULTRON desde la misma terminal donde "
                    "`echo $GROQ_API_KEY` muestra tu clave."
                )

            if not shutil.which("parecord"):
                raise RuntimeError(
                    "No encuentro `parecord`. Instala PulseAudio utilities con: "
                    "sudo apt install pulseaudio-utils"
                )

            # Archivo temporal para la voz del usuario.
            tmp = tempfile.NamedTemporaryFile(
                prefix="ultron_voice_",
                suffix=".wav",
                delete=False
            )
            wav_path = tmp.name
            tmp.close()

            # Se detiene automáticamente al detectar silencio.
            self._set_live_text("🎙 ESCUCHANDO…")
            self._record_until_silence(wav_path)

            self.root.after(
                0,
                lambda: self._set_consciousness_state(
                    "THINKING",
                    "● CONCIENCIA PENSANDO",
                    ORANGE_L
                )
            )
            self._safe_log("CONCIENCIA: audio capturado")

            user_text = self._groq_transcribe(wav_path, api_key).strip()

            if not user_text:
                raise RuntimeError("No pude detectar voz en la grabación.")

            self._safe_log(f"TÚ: {user_text}")
            self._set_live_text(f"TÚ: {user_text}")

            self.ai_history.append({
                "role": "user",
                "content": user_text
            })

            # Evitar mandar una conversación enorme en cada petición.
            system_message = self.ai_history[0]
            recent = self.ai_history[1:][-12:]
            payload_history = [system_message] + recent

            response_text = self._groq_chat(payload_history, api_key).strip()

            if not response_text:
                raise RuntimeError("Groq devolvió una respuesta vacía.")

            self.ai_history.append({
                "role": "assistant",
                "content": response_text
            })

            self._safe_log(f"ULTRON: {response_text}")
            self._animate_response_text(response_text)

            self.root.after(
                0,
                lambda: self._set_consciousness_state(
                    "SPEAKING",
                    "● CONCIENCIA HABLANDO",
                    GREEN
                )
            )

            self._speak_text(response_text)

        except Exception as exc:
            message = str(exc)
            self._safe_log(f"CONCIENCIA ERROR: {message}")
            self.root.after(
                0,
                lambda m=message: self._voice_error(m)
            )

        finally:
            if wav_path:
                try:
                    os.remove(wav_path)
                except Exception:
                    pass

            self.ai_busy = False

            if self.consciousness_active:
                self.root.after(
                    120,
                    self._begin_continuous_listening
                )
            else:
                self.root.after(
                    0,
                    lambda: self._set_consciousness_state(
                        "IDLE",
                        "● SYSTEM ONLINE",
                        TURQUOISE
                    )
                )

    def _safe_log(self, text):
        self.root.after(0, lambda t=text: self._add_log(t))

    def _voice_error(self, message):
        self._set_consciousness_state(
            "IDLE",
            "● CONCIENCIA ERROR",
            RED
        )
        self._show_module(
            "CONCIENCIA / AUDIO",
            message
        )

    def _groq_transcribe(self, wav_path, api_key):
        """
        Envía el WAV a Groq Speech-to-Text usando Whisper Large V3 Turbo.
        Implementado con urllib para no obligar a instalar el SDK de Groq.
        """
        boundary = "----UltronBoundary" + uuid.uuid4().hex

        with open(wav_path, "rb") as f:
            audio = f.read()

        parts = []

        def add_field(name, value):
            parts.append(
                (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                    f"{value}\r\n"
                ).encode("utf-8")
            )

        add_field("model", "whisper-large-v3-turbo")
        add_field("language", "es")
        add_field("response_format", "json")

        parts.append(
            (
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="file"; filename="voice.wav"\r\n'
                "Content-Type: audio/wav\r\n\r\n"
            ).encode("utf-8")
        )
        parts.append(audio)
        parts.append(b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode("utf-8"))

        body = b"".join(parts)

        request = urllib.request.Request(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "User-Agent": "ULTRON-Core/3.0",
            }
        )

        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Groq STT respondió HTTP {exc.code}: {detail[:350]}"
            )
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"No pude conectar con Groq para transcribir: {exc.reason}"
            )

        return data.get("text", "")

    def _groq_chat(self, history, api_key):
        """Obtiene la respuesta conversacional de ULTRON mediante Groq."""
        payload = json.dumps({
            "model": "llama-3.1-8b-instant",
            "messages": history,
            "temperature": 0.55,
            "max_completion_tokens": 500
        }).encode("utf-8")

        request = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "ULTRON-Core/3.0",
            }
        )

        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Groq Chat respondió HTTP {exc.code}: {detail[:350]}"
            )
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"No pude conectar con Groq Chat: {exc.reason}"
            )

        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            raise RuntimeError(
                "La respuesta de Groq no tenía el formato esperado."
            )

    def _stop_speaking(self):
        """Detiene la reproducción actual inmediatamente."""
        process = self.tts_process
        self.tts_process = None

        if process and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=1)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass

    def _speak_text(self, text):
        """
        Voz principal: edge-tts (más natural, online).
        Respaldo: espeak-ng/espeak si edge-tts no está instalado o falla.
        """
        edge_tts = shutil.which("edge-tts")
        paplay = shutil.which("paplay")

        if not paplay:
            raise RuntimeError(
                "No encuentro `paplay`. Instala: sudo apt install pulseaudio-utils"
            )

        default_sink = self._resolve_output_device()

        if default_sink:
            try:
                subprocess.run(
                    ["pactl", "set-sink-volume", default_sink, f"{int(self.ultron_volume)}%"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=3
                )
            except Exception:
                pass

        # Voz natural principal.
        if edge_tts:
            mp3 = tempfile.NamedTemporaryFile(
                prefix="ultron_tts_",
                suffix=".mp3",
                delete=False
            )
            speech_path = mp3.name
            mp3.close()

            try:
                synth = subprocess.run(
                    [
                        edge_tts,
                        "--voice", "es-MX-DaliaNeural",
                        "--rate=+0%",
                        "--pitch=+0Hz",
                        "--text", text,
                        "--write-media", speech_path
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=45
                )

                if synth.returncode == 0 and os.path.getsize(speech_path) > 500:
                    player = shutil.which("ffplay") or shutil.which("mpv")
                    if player:
                        if os.path.basename(player) == "ffplay":
                            cmd = [player, "-nodisp", "-autoexit", "-loglevel", "quiet", speech_path]
                        else:
                            cmd = [player, "--no-video", "--really-quiet", speech_path]

                        self.tts_process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self.tts_process.wait()
                        self.tts_process = None
                        return
            finally:
                try:
                    os.remove(speech_path)
                except Exception:
                    pass

        raise RuntimeError(
            "La voz natural no está disponible. Instala edge-tts con: "
            "python3 -m pip install edge-tts --break-system-packages "
            "y ffmpeg con: sudo apt install ffmpeg"
        )


    def _start_animation(self):
        def tick():
            if hasattr(self, "core"):
                self.core.animate()
            self.root.after(40, tick)
        self.root.after(100, tick)

    def _update_metrics(self):
        if HAS_PSUTIL:
            try:
                self.metric_vars["cpu"].set(f"{psutil.cpu_percent():.0f} %")
                self.metric_vars["ram"].set(f"{psutil.virtual_memory().percent:.0f} %")
                self.metric_vars["disk"].set(f"{psutil.disk_usage('/').percent:.0f} %")
                self.metric_vars["net"].set("connected")
            except Exception:
                pass
        else:
            self.metric_vars["cpu"].set("-- %")
            self.metric_vars["ram"].set("-- %")
            self.metric_vars["disk"].set("-- %")
            self.metric_vars["net"].set("N/A")
        self.root.after(2000, self._update_metrics)

    def _add_log(self, msg):
        self.log_text.configure(state=tk.NORMAL)
        ts = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{ts}]  > {msg}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _get_hostname(self):
        try:
            return socket.gethostname()[:18]
        except Exception:
            return "Linux"

    def _uptime_str(self):
        if not HAS_PSUTIL:
            return "N/A"
        seconds = int(time.time() - psutil.boot_time())
        d = seconds // 86400
        h = (seconds % 86400) // 3600
        m = (seconds % 3600) // 60
        return f"{d}d {h}h {m}m"

    def _on_ai(self):
        self._add_log("Module CONCIENCIA selected")
        self._show_module(
            "CONCIENCIA / AI",
            "MODO ESCRITO DE CONCIENCIA\n\n"
            "El chat escrito se conectará en la siguiente etapa y compartirá "
            "el mismo historial que la voz.\n\n"
            "VOZ ACTUAL:\n"
            "• Clic en CORE: escuchar durante 7 segundos\n"
            "• Voz a texto: Groq Whisper\n"
            "• Respuesta: Groq Chat\n"
            "• Texto a voz: espeak-ng / espeak\n"
            "• Salida: dispositivo ALSA predeterminado\n\n"
            "Necesitas que GROQ_API_KEY esté disponible en el entorno."
        )

    def _on_system(self):
        self._add_log("Module SISTEMA selected")
        info = (
            f"Sistema: {platform.system()} {platform.release()}\n"
            f"Arquitectura: {platform.machine()}\n"
            f"Equipo: {platform.node()}\n"
            f"Uptime: {self._uptime_str()}\n"
        )
        if HAS_PSUTIL:
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            info += (
                f"\nCPU: {psutil.cpu_percent()}%\n"
                f"RAM: {ram.percent}%  "
                f"({ram.used/1024**3:.1f} / {ram.total/1024**3:.1f} GB)\n"
                f"Disco: {disk.percent}%  "
                f"({disk.used/1024**3:.1f} / {disk.total/1024**3:.1f} GB)"
            )
        self._show_module("SISTEMA", info)

    def _on_network(self):
        self._add_log("Module RED selected")
        ip = run_cmd("hostname -I")
        status = run_cmd("nmcli device status")
        general = run_cmd("nmcli general")
        info = (
            f"IP del equipo:\n{ip}\n\n"
            f"Estado de dispositivos:\n{status}\n\n"
            f"Informacion general:\n{general}"
        )
        self._show_module("RED", info)

    def _on_security(self):
        self._add_log("Module SEGURIDAD selected")
        ports = run_cmd("ss -tuln | head -20")
        services = run_cmd("systemctl --type=service --state=running | head -15")
        uname = run_cmd("uname -a")
        info = (
            f"Puertos abiertos (muestra):\n{ports}\n\n"
            f"Servicios activos (muestra):\n{services}\n\n"
            f"Kernel:\n{uname}"
        )
        self._show_module("SEGURIDAD", info)

    def _on_files(self):
        self._add_log("Module ARCHIVOS selected")
        df = run_cmd("df -h | head -12")
        lsblk = run_cmd("lsblk")
        info = f"Espacio en disco:\n{df}\n\nDispositivos:\n{lsblk}"
        self._show_module("ARCHIVOS", info)

    def _run_command_async(self, command, output_widget, title="COMANDO"):
        """Ejecuta comandos sin congelar la interfaz."""
        output_widget.configure(state=tk.NORMAL)
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, f"> {command}\n\nEjecutando...\n")
        output_widget.configure(state=tk.DISABLED)

        def worker():
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=120
                )
                text = result.stdout.strip() or "(Sin salida)"
            except subprocess.TimeoutExpired:
                text = (
                    "El comando tardó demasiado.\n\n"
                    "Si es un comando con sudo, ULTRON no puede responder "
                    "una contraseña desde esta ventana. Usa el botón TERMINAL "
                    "para los comandos administrativos."
                )
            except Exception as exc:
                text = f"Error:\n{exc}"

            def show():
                if not output_widget.winfo_exists():
                    return
                output_widget.configure(state=tk.NORMAL)
                output_widget.delete("1.0", tk.END)
                output_widget.insert(tk.END, text)
                output_widget.configure(state=tk.DISABLED)
                self._add_log(f"{title}: comando finalizado")

            self.root.after(0, show)

        threading.Thread(target=worker, daemon=True).start()

    def _run_admin_terminal(self, command):
        """Abre un comando administrativo en una terminal para que sudo pueda pedir contraseña."""
        script = f"{command}; echo; echo 'Presiona ENTER para cerrar'; read _"
        terminals = [
            ["x-terminal-emulator", "-e", "bash", "-lc", script],
            ["gnome-terminal", "--", "bash", "-lc", script],
            ["konsole", "-e", "bash", "-lc", script],
            ["xfce4-terminal", "-e", f"bash -lc {shlex.quote(script)}"],
        ]

        for terminal_cmd in terminals:
            try:
                subprocess.Popen(
                    terminal_cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self._add_log(f"Terminal administrativa: {command}")
                return
            except FileNotFoundError:
                continue
            except Exception:
                continue

        self._show_module(
            "COMANDO ADMINISTRATIVO",
            "No encontré un emulador de terminal compatible.\n\n"
            f"Ejecuta manualmente:\n\n{command}"
        )

    def _module_action_window(self, title, actions, search_action=None):
        """Ventana reutilizable para módulos de comandos."""
        win = tk.Toplevel(self.root)
        win.title(f"ULTRON — {title}")
        win.configure(bg=BG)
        win.geometry("780x560")
        win.minsize(650, 480)
        win.transient(self.root)

        header = tk.Frame(win, bg=BG_PANEL2, height=44)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text=f"// {title}",
            font=self.font_title, fg=ORANGE, bg=BG_PANEL2
        ).pack(side=tk.LEFT, padx=16, pady=8)

        main = tk.Frame(win, bg=BG)
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        controls = tk.Frame(main, bg=BG_PANEL, width=245)
        controls.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        controls.pack_propagate(False)

        output_frame = tk.Frame(main, bg=BG_PANEL)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            controls, text="ACCIONES",
            font=self.font_small, fg=ORANGE, bg=BG_PANEL
        ).pack(anchor="w", padx=10, pady=(10, 6))

        search_var = tk.StringVar()

        if search_action:
            tk.Label(
                controls, text="Paquete / búsqueda",
                font=self.font_small, fg=TEXT_DIM, bg=BG_PANEL
            ).pack(anchor="w", padx=10, pady=(4, 2))

            search_entry = tk.Entry(
                controls, textvariable=search_var,
                font=self.font_mono,
                bg=BG_PANEL2, fg=TEXT,
                insertbackground=ORANGE,
                relief=tk.FLAT
            )
            search_entry.pack(fill=tk.X, padx=10, pady=(0, 6))

        output = tk.Text(
            output_frame,
            bg="#080808",
            fg=TEXT,
            font=self.font_mono,
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=12,
            pady=10,
            state=tk.DISABLED
        )
        output_scroll = tk.Scrollbar(
            output_frame,
            orient="vertical",
            command=output.yview
        )
        output.configure(yscrollcommand=output_scroll.set)
        output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        output_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        def run_normal(label, command):
            self._add_log(f"{title}: {label}")
            self._run_command_async(command, output, title)

        def run_search():
            value = search_var.get().strip()
            if not value:
                output.configure(state=tk.NORMAL)
                output.delete("1.0", tk.END)
                output.insert(tk.END, "Escribe primero el nombre del paquete.")
                output.configure(state=tk.DISABLED)
                return
            command = search_action.format(query=shlex.quote(value))
            run_normal("buscar", command)

        if search_action:
            tk.Button(
                controls,
                text="BUSCAR",
                font=self.font_small,
                fg=TURQUOISE,
                bg=BG_PANEL2,
                activeforeground=TEXT,
                activebackground=GRAY,
                relief=tk.FLAT,
                command=run_search,
                padx=8, pady=7
            ).pack(fill=tk.X, padx=10, pady=(0, 8))

        for item in actions:
            label = item["label"]
            command = item["command"]
            admin = item.get("admin", False)

            if admin:
                callback = lambda c=command: self._run_admin_terminal(c)
            else:
                callback = lambda l=label, c=command: run_normal(l, c)

            tk.Button(
                controls,
                text=label,
                font=self.font_small,
                fg=ORANGE if not admin else ORANGE_L,
                bg=BG_PANEL2,
                activeforeground=ORANGE_L,
                activebackground=GRAY,
                relief=tk.FLAT,
                anchor="w",
                command=callback,
                padx=10,
                pady=8
            ).pack(fill=tk.X, padx=10, pady=3)

        tk.Label(
            controls,
            text="Los comandos con sudo se abren\nen una terminal para solicitar\nla contraseña de forma normal.",
            font=self.font_small,
            fg=TEXT_DIM,
            bg=BG_PANEL,
            justify="left"
        ).pack(side=tk.BOTTOM, anchor="w", padx=10, pady=10)

        output.configure(state=tk.NORMAL)
        output.insert(
            tk.END,
            f"{title}\n\nSelecciona una acción en el panel izquierdo."
        )
        output.configure(state=tk.DISABLED)

    def _on_tools(self):
        self._add_log("Module HERRAMIENTAS selected")
        self._module_action_window(
            "HERRAMIENTAS",
            actions=[
                {
                    "label": "Ver herramientas instaladas",
                    "command": "which nmap sqlmap aircrack-ng hydra"
                },
                {
                    "label": "Actualizar lista de paquetes",
                    "command": "sudo apt update",
                    "admin": True
                },
                {
                    "label": "Información de Python",
                    "command": "python3 --version"
                },
                {
                    "label": "Información de Kali",
                    "command": "cat /etc/os-release"
                },
            ],
            search_action="apt-cache search {query}"
        )

    def _on_diagnostics(self):
        self._add_log("Module DIAGNOSTICO selected")
        self._module_action_window(
            "DIAGNOSTICO",
            actions=[
                {
                    "label": "Información del procesador",
                    "command": "lscpu | grep -E 'Model name|Nombre del modelo' | head -1"
                },
                {
                    "label": "Memoria RAM",
                    "command": "free -h"
                },
                {
                    "label": "Uso del disco",
                    "command": "df -h"
                },
                {
                    "label": "Procesos activos",
                    "command": "ps aux --sort=-%cpu | head -15"
                },
                {
                    "label": "Temperatura del sistema",
                    "command": "sensors"
                },
            ]
        )

    def _on_packages(self):
        self._add_log("Module PAQUETES selected")
        self._module_action_window(
            "GESTOR DE PAQUETES",
            actions=[
                {
                    "label": "Ver paquetes instalados",
                    "command": "apt list --installed 2>/dev/null"
                },
                {
                    "label": "Actualizar repositorios",
                    "command": "sudo apt update",
                    "admin": True
                },
                {
                    "label": "Actualizar sistema",
                    "command": "sudo apt upgrade",
                    "admin": True
                },
                {
                    "label": "Limpiar paquetes",
                    "command": "sudo apt autoremove",
                    "admin": True
                },
            ],
            search_action="apt-cache search {query}"
        )

    # ============================================================
    # CHAT WIFI - adaptación gráfica del módulo original
    # ============================================================
    def _on_chat(self):
        self._add_log("Module CHAT WIFI selected")

        win = tk.Toplevel(self.root)
        win.title("ULTRON — CHAT WIFI")
        win.configure(bg=BG)
        win.geometry("880x600")
        win.minsize(720, 500)
        win.transient(self.root)

        state = {
            "server": None,
            "client": None,
            "clients": {},
            "running": False,
            "mode": None,
            "username": "",
            "threads": [],
        }
        chat_lock = threading.Lock()

        header = tk.Frame(win, bg=BG_PANEL2, height=44)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="// ULTRON CHAT / LOCAL WIFI",
            font=self.font_title, fg=ORANGE, bg=BG_PANEL2
        ).pack(side=tk.LEFT, padx=16, pady=8)

        status_var = tk.StringVar(value="● DESCONECTADO")
        status_lbl = tk.Label(
            header, textvariable=status_var,
            font=self.font_small, fg=RED, bg=BG_PANEL2
        )
        status_lbl.pack(side=tk.RIGHT, padx=16)

        body = tk.Frame(win, bg=BG)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        left = tk.Frame(body, bg=BG_PANEL, width=245)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        center = tk.Frame(body, bg=BG_PANEL)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            left, text="CONEXIÓN",
            font=self.font_small, fg=ORANGE, bg=BG_PANEL
        ).pack(anchor="w", padx=10, pady=(10, 8))

        username_var = tk.StringVar(value=socket.gethostname()[:12] or "Usuario")
        host_var = tk.StringVar(value="127.0.0.1")
        port_var = tk.StringVar(value="5050")

        for label, var in (
            ("Nombre de usuario", username_var),
            ("IP del servidor", host_var),
            ("Puerto", port_var),
        ):
            tk.Label(
                left, text=label,
                font=self.font_small, fg=TEXT_DIM, bg=BG_PANEL
            ).pack(anchor="w", padx=10, pady=(5, 2))
            tk.Entry(
                left, textvariable=var,
                font=self.font_mono,
                bg=BG_PANEL2, fg=TEXT,
                insertbackground=ORANGE,
                relief=tk.FLAT
            ).pack(fill=tk.X, padx=10)

        users_var = tk.StringVar(value="Usuarios: 0")
        tk.Label(
            left, textvariable=users_var,
            font=self.font_small, fg=TURQUOISE, bg=BG_PANEL
        ).pack(anchor="w", padx=10, pady=(14, 4))

        users_list = tk.Listbox(
            left,
            bg="#080808",
            fg=TEXT,
            font=self.font_small,
            relief=tk.FLAT,
            height=8,
            selectbackground=ORANGE_D
        )
        users_list.pack(fill=tk.X, padx=10, pady=(0, 10))

        messages = tk.Text(
            center,
            bg="#080808",
            fg=TEXT,
            font=self.font_mono,
            relief=tk.FLAT,
            wrap=tk.WORD,
            state=tk.DISABLED,
            padx=12,
            pady=10
        )
        msg_scroll = tk.Scrollbar(center, orient="vertical", command=messages.yview)
        messages.configure(yscrollcommand=msg_scroll.set)
        messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        msg_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        bottom = tk.Frame(win, bg=BG, height=52)
        bottom.pack(fill=tk.X, padx=12, pady=(0, 12))
        bottom.pack_propagate(False)

        message_var = tk.StringVar()
        entry = tk.Entry(
            bottom,
            textvariable=message_var,
            font=self.font_mono,
            bg=BG_PANEL2,
            fg=TEXT,
            insertbackground=ORANGE,
            relief=tk.FLAT
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=8)

        def ui_log(text, tag=None):
            def update():
                if not messages.winfo_exists():
                    return
                messages.configure(state=tk.NORMAL)
                messages.insert(tk.END, text + "\n")
                messages.see(tk.END)
                messages.configure(state=tk.DISABLED)
            self.root.after(0, update)

        def ui_status(text, color):
            def update():
                if status_lbl.winfo_exists():
                    status_var.set(text)
                    status_lbl.configure(fg=color)
            self.root.after(0, update)

        def set_users(names):
            def update():
                if not users_list.winfo_exists():
                    return
                users_list.delete(0, tk.END)
                for name in names:
                    users_list.insert(tk.END, f"■ {name}")
                users_var.set(f"Usuarios: {len(names)}")
            self.root.after(0, update)

        def send_line(sock, text):
            try:
                sock.sendall((text + "\n").encode("utf-8"))
                return True
            except Exception:
                return False

        def server_user_names():
            with chat_lock:
                names = [state["username"]]
                names.extend(
                    data["username"] for data in state["clients"].values()
                )
            return names

        def server_broadcast(text, exclude=None):
            dead = []
            with chat_lock:
                snapshot = list(state["clients"].items())
            for sock, data in snapshot:
                if sock is exclude:
                    continue
                if not send_line(sock, text):
                    dead.append(sock)
            for sock in dead:
                try:
                    sock.close()
                except Exception:
                    pass
                with chat_lock:
                    state["clients"].pop(sock, None)

        def server_send_users():
            names = server_user_names()
            payload = "USERLIST:" + "|".join(names)
            server_broadcast(payload)
            set_users(names)

        def handle_server_client(client, address, username):
            ui_log(f"■ {username} se conectó ({address[0]}).")
            server_broadcast(f"SYS:{username} se conectó.", exclude=client)
            server_send_users()
            buffer = ""

            try:
                while state["running"] and state["mode"] == "server":
                    data = client.recv(4096)
                    if not data:
                        break
                    buffer += data.decode("utf-8", errors="replace")

                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        if line == "/exit":
                            raise ConnectionError("Cliente salió")
                        formatted = f"{username}: {line}"
                        ui_log(formatted)
                        server_broadcast("MSG:" + formatted, exclude=client)
            except Exception:
                pass
            finally:
                with chat_lock:
                    state["clients"].pop(client, None)
                try:
                    client.close()
                except Exception:
                    pass
                ui_log(f"■ {username} se desconectó.")
                server_broadcast(f"SYS:{username} se desconectó.")
                server_send_users()

        def server_accept_loop():
            server = state["server"]
            while state["running"] and state["mode"] == "server":
                try:
                    client, address = server.accept()
                    client.settimeout(None)
                    raw = client.recv(1024)
                    if not raw:
                        client.close()
                        continue
                    username = raw.decode("utf-8", errors="replace").strip() or "Usuario"
                    with chat_lock:
                        state["clients"][client] = {
                            "username": username,
                            "address": address
                        }
                    send_line(client, "READY")
                    threading.Thread(
                        target=handle_server_client,
                        args=(client, address, username),
                        daemon=True
                    ).start()
                except OSError:
                    break
                except Exception as exc:
                    if state["running"]:
                        ui_log(f"Error del servidor: {exc}")

        def start_server():
            if state["running"]:
                ui_log("Ya existe una conexión activa.")
                return

            username = username_var.get().strip() or "Usuario"
            try:
                port = int(port_var.get().strip())
            except ValueError:
                ui_log("Puerto no válido.")
                return

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                server.bind(("0.0.0.0", port))
                server.listen(10)
            except Exception as exc:
                ui_log(f"No se pudo iniciar el servidor: {exc}")
                try:
                    server.close()
                except Exception:
                    pass
                return

            state["server"] = server
            state["running"] = True
            state["mode"] = "server"
            state["username"] = username

            ui_status(f"● SERVIDOR :{port}", GREEN)
            ui_log(f"Servidor iniciado en el puerto {port}.")
            ui_log("Los otros equipos deben conectarse a la IP de este equipo.")
            set_users([username])
            self._add_log(f"CHAT servidor iniciado en puerto {port}")

            threading.Thread(
                target=server_accept_loop,
                daemon=True
            ).start()

        def client_receive_loop(client):
            buffer = ""
            try:
                while state["running"] and state["mode"] == "client":
                    data = client.recv(4096)
                    if not data:
                        break
                    buffer += data.decode("utf-8", errors="replace")

                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        line = line.strip()
                        if not line or line == "READY":
                            continue
                        if line.startswith("USERLIST:"):
                            raw = line.split(":", 1)[1]
                            set_users([x for x in raw.split("|") if x])
                        elif line.startswith("MSG:"):
                            ui_log(line[4:])
                        elif line.startswith("SYS:"):
                            ui_log("■ " + line[4:])
                        else:
                            ui_log(line)
            except Exception as exc:
                if state["running"]:
                    ui_log(f"Conexión finalizada: {exc}")
            finally:
                if state["running"] and state["mode"] == "client":
                    self.root.after(0, disconnect)

        def connect_client():
            if state["running"]:
                ui_log("Ya existe una conexión activa.")
                return

            host = host_var.get().strip() or "127.0.0.1"
            username = username_var.get().strip() or "Usuario"

            try:
                port = int(port_var.get().strip())
            except ValueError:
                ui_log("Puerto no válido.")
                return

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(8)

            try:
                client.connect((host, port))
                client.settimeout(None)
                send_line(client, username)
            except Exception as exc:
                ui_log(f"No se pudo conectar: {exc}")
                try:
                    client.close()
                except Exception:
                    pass
                return

            state["client"] = client
            state["running"] = True
            state["mode"] = "client"
            state["username"] = username

            ui_status(f"● CONECTADO {host}:{port}", TURQUOISE)
            ui_log(f"Conectado a {host}:{port}.")
            self._add_log(f"CHAT conectado a {host}:{port}")

            threading.Thread(
                target=client_receive_loop,
                args=(client,),
                daemon=True
            ).start()

        def disconnect():
            if not state["running"]:
                return

            mode = state["mode"]
            state["running"] = False

            if mode == "client":
                client = state.get("client")
                if client:
                    try:
                        send_line(client, "/exit")
                        client.shutdown(socket.SHUT_RDWR)
                    except Exception:
                        pass
                    try:
                        client.close()
                    except Exception:
                        pass
                state["client"] = None

            elif mode == "server":
                with chat_lock:
                    clients = list(state["clients"].keys())
                    state["clients"].clear()

                for client in clients:
                    try:
                        send_line(client, "SYS:Servidor cerrado.")
                        client.shutdown(socket.SHUT_RDWR)
                    except Exception:
                        pass
                    try:
                        client.close()
                    except Exception:
                        pass

                server = state.get("server")
                if server:
                    try:
                        server.close()
                    except Exception:
                        pass
                state["server"] = None

            state["mode"] = None
            ui_status("● DESCONECTADO", RED)
            set_users([])
            ui_log("Chat desconectado.")
            self._add_log("CHAT desconectado")

        def send_message():
            text = message_var.get().strip()
            if not text:
                return
            if not state["running"]:
                ui_log("Primero inicia un servidor o conéctate a uno.")
                return

            username = state["username"]
            if state["mode"] == "client":
                client = state.get("client")
                if client and send_line(client, text):
                    ui_log(f"{username}: {text}")
                else:
                    ui_log("No se pudo enviar el mensaje.")
            else:
                formatted = f"{username}: {text}"
                ui_log(formatted)
                server_broadcast("MSG:" + formatted)

            message_var.set("")

        tk.Button(
            left, text="INICIAR SERVIDOR",
            font=self.font_small,
            fg=GREEN, bg=BG_PANEL2,
            activebackground=GRAY,
            relief=tk.FLAT,
            command=start_server,
            padx=8, pady=8
        ).pack(fill=tk.X, padx=10, pady=(4, 3))

        tk.Button(
            left, text="CONECTAR COMO CLIENTE",
            font=self.font_small,
            fg=TURQUOISE, bg=BG_PANEL2,
            activebackground=GRAY,
            relief=tk.FLAT,
            command=connect_client,
            padx=8, pady=8
        ).pack(fill=tk.X, padx=10, pady=3)

        tk.Button(
            left, text="DESCONECTAR",
            font=self.font_small,
            fg=RED, bg=BG_PANEL2,
            activebackground=GRAY,
            relief=tk.FLAT,
            command=disconnect,
            padx=8, pady=8
        ).pack(fill=tk.X, padx=10, pady=3)

        tk.Button(
            bottom, text="ENVIAR",
            font=self.font_small,
            fg=ORANGE, bg=BG_PANEL2,
            activeforeground=ORANGE_L,
            activebackground=GRAY,
            relief=tk.FLAT,
            command=send_message,
            padx=18, pady=7
        ).pack(side=tk.RIGHT)

        entry.bind("<Return>", lambda _e: send_message())

        def close_chat():
            disconnect()
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", close_chat)
        ui_log("ULTRON CHAT listo.")
        ui_log("Inicia un servidor o escribe la IP de otro equipo y conéctate.")

    def _theme_dict_from_globals(self):
        return {
            "BG": BG,
            "BG_PANEL": BG_PANEL,
            "BG_PANEL2": BG_PANEL2,
            "PRIMARY": ORANGE,
            "PRIMARY_L": ORANGE_L,
            "PRIMARY_D": ORANGE_D,
            "PRIMARY_DIM": ORANGE_DIM,
            "SECONDARY": TURQUOISE,
            "SECONDARY_D": TURQUOISE_D,
            "SECONDARY_DIM": TURQUOISE_DIM,
            "TEXT": TEXT,
            "TEXT_DIM": TEXT_DIM,
            "GOOD": GREEN,
            "DANGER": RED,
        }

    def _pick_color(self, var):
        current = var.get()
        color = colorchooser.askcolor(
            color=current,
            title="ULTRON // Seleccionar color"
        )[1]
        if color:
            var.set(color)

    def _recolor_widget_tree(self, widget, old_theme, new_theme):
        """Recolorea widgets ya existentes sin reconstruir toda la aplicación."""
        color_map = {
            old_theme["BG"]: new_theme["BG"],
            old_theme["BG_PANEL"]: new_theme["BG_PANEL"],
            old_theme["BG_PANEL2"]: new_theme["BG_PANEL2"],
            old_theme["PRIMARY"]: new_theme["PRIMARY"],
            old_theme["PRIMARY_L"]: new_theme["PRIMARY_L"],
            old_theme["PRIMARY_D"]: new_theme["PRIMARY_D"],
            old_theme["PRIMARY_DIM"]: new_theme["PRIMARY_DIM"],
            old_theme["SECONDARY"]: new_theme["SECONDARY"],
            old_theme["SECONDARY_D"]: new_theme["SECONDARY_D"],
            old_theme["SECONDARY_DIM"]: new_theme["SECONDARY_DIM"],
            old_theme["TEXT"]: new_theme["TEXT"],
            old_theme["TEXT_DIM"]: new_theme["TEXT_DIM"],
            old_theme["GOOD"]: new_theme["GOOD"],
            old_theme["DANGER"]: new_theme["DANGER"],
            "#080808": new_theme["BG"],
            "#1a1a1a": new_theme["BG_PANEL2"],
            "#2a2a2a": new_theme["PRIMARY_DIM"],
        }

        options = (
            "background", "foreground",
            "activebackground", "activeforeground",
            "highlightbackground", "highlightcolor",
            "insertbackground", "selectbackground", "selectforeground",
            "troughcolor"
        )

        for option in options:
            try:
                current = widget.cget(option)
                if current in color_map:
                    widget.configure(**{option: color_map[current]})
            except Exception:
                pass

        for child in widget.winfo_children():
            self._recolor_widget_tree(child, old_theme, new_theme)

    def _apply_theme_live(self, theme):
        """Aplica el tema inmediatamente; no requiere reiniciar ULTRON."""
        old_theme = self._theme_dict_from_globals()
        apply_theme_globals(theme)

        # Recolorear todos los widgets, incluidas ventanas secundarias abiertas.
        self._recolor_widget_tree(self.root, old_theme, theme)

        # Los Canvas tienen gráficos propios; se redibujan con el nuevo tema.
        try:
            self.core_canvas.delete("all")
            self.core_canvas.configure(bg=BG)
            self._init_core()
        except Exception:
            pass

        try:
            self.map_canvas.configure(bg=BG_PANEL)
            self._draw_map()
        except Exception:
            pass

        self.root.configure(bg=BG)
        self.root.update_idletasks()

    def _list_audio_sources(self):
        """Devuelve fuentes de audio visibles en PipeWire/PulseAudio."""
        devices = []
        try:
            out = subprocess.check_output(
                ["pactl", "list", "short", "sources"],
                text=True,
                stderr=subprocess.DEVNULL
            )
            for line in out.splitlines():
                parts = line.split("\t")
                if len(parts) >= 2:
                    name = parts[1].strip()
                    # Ocultar monitores de salida para no confundir.
                    if name.endswith(".monitor"):
                        continue
                    devices.append(name)
        except Exception:
            pass
        return devices

    def _list_audio_sinks(self):
        """Devuelve salidas de audio visibles en PipeWire/PulseAudio."""
        devices = []
        try:
            out = subprocess.check_output(
                ["pactl", "list", "short", "sinks"],
                text=True,
                stderr=subprocess.DEVNULL
            )
            for line in out.splitlines():
                parts = line.split("\t")
                if len(parts) >= 2:
                    devices.append(parts[1].strip())
        except Exception:
            pass
        return devices

    def _resolve_input_device(self):
        if self.audio_input_device and self.audio_input_device != "Automático":
            return self.audio_input_device
        try:
            return subprocess.check_output(
                ["pactl", "get-default-source"],
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
        except Exception:
            return ""

    def _resolve_output_device(self):
        if self.audio_output_device and self.audio_output_device != "Automático":
            return self.audio_output_device
        try:
            return subprocess.check_output(
                ["pactl", "get-default-sink"],
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
        except Exception:
            return ""

    def _test_microphone(self, parent=None):
        """Graba 3 segundos y muestra si se pudo capturar audio."""
        def worker():
            tmp = tempfile.NamedTemporaryFile(
                prefix="ultron_mic_test_",
                suffix=".wav",
                delete=False
            )
            path = tmp.name
            tmp.close()

            try:
                device = self._resolve_input_device()
                cmd = ["parecord"]
                if device:
                    cmd.append(f"--device={device}")
                cmd.extend([
                    "--file-format=wav",
                    "--format=s16le",
                    "--rate=16000",
                    "--channels=1",
                    path
                ])

                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True
                )

                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.terminate()
                    try:
                        proc.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        proc.kill()

                size = os.path.getsize(path) if os.path.exists(path) else 0
                msg = (
                    f"Micrófono detectado.\nDispositivo: {device or 'predeterminado'}\n"
                    f"Se capturaron {size} bytes de audio."
                    if size > 1000
                    else "No se detectó una grabación válida."
                )
            except Exception as exc:
                msg = f"Error probando micrófono:\n{exc}"
            finally:
                try:
                    os.remove(path)
                except Exception:
                    pass

            self.root.after(
                0,
                lambda: self._show_module("PRUEBA DE MICRÓFONO", msg)
            )

        threading.Thread(target=worker, daemon=True).start()

    def _test_voice_output(self, parent=None):
        """Genera una frase corta y la reproduce en la salida seleccionada."""
        def worker():
            try:
                espeak = shutil.which("espeak-ng") or shutil.which("espeak")
                paplay = shutil.which("paplay")

                if not espeak or not paplay:
                    raise RuntimeError(
                        "Falta espeak-ng/espeak o paplay."
                    )

                tmp = tempfile.NamedTemporaryFile(
                    prefix="ultron_voice_test_",
                    suffix=".wav",
                    delete=False
                )
                path = tmp.name
                tmp.close()

                subprocess.run(
                    [
                        espeak,
                        "-v", "es",
                        "-s", "150",
                        "-p", "42",
                        "-w", path,
                        "Sistema de audio de Ultron operativo."
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=20
                )

                device = self._resolve_output_device()
                cmd = ["paplay"]
                if device:
                    cmd.append(f"--device={device}")
                cmd.append(path)

                subprocess.run(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=20
                )
                msg = f"Prueba enviada a:\n{device or 'salida predeterminada'}"
            except Exception as exc:
                msg = f"Error probando salida de audio:\n{exc}"
            finally:
                try:
                    os.remove(path)
                except Exception:
                    pass

            self.root.after(
                0,
                lambda: self._show_module("PRUEBA DE VOZ", msg)
            )

        threading.Thread(target=worker, daemon=True).start()

    def _on_appearance(self):
        self._add_log("Module PREFERENCIAS selected")

        win = tk.Toplevel(self.root)
        win.title("ULTRON — PREFERENCIAS")
        win.configure(bg=BG)
        win.geometry("900x600")
        win.minsize(760, 520)
        win.transient(self.root)

        header = tk.Frame(win, bg=BG_PANEL2, height=48)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="// PREFERENCIAS / APARIENCIA",
            font=self.font_title, fg=ORANGE, bg=BG_PANEL2
        ).pack(side=tk.LEFT, padx=18, pady=9)

        status = tk.Label(
            header, text="● LIVE THEME ENGINE",
            font=self.font_small, fg=TURQUOISE, bg=BG_PANEL2
        )
        status.pack(side=tk.RIGHT, padx=18)

        # Contenedor con scroll independiente para Preferencias.
        pref_outer = tk.Frame(win, bg=BG)
        pref_outer.pack(fill=tk.BOTH, expand=True)

        pref_canvas = tk.Canvas(
            pref_outer,
            bg=BG,
            highlightthickness=0,
            bd=0
        )
        pref_scrollbar = tk.Scrollbar(
            pref_outer,
            orient="vertical",
            command=pref_canvas.yview,
            bg=BG_PANEL2,
            troughcolor=BG,
            activebackground=ORANGE_D
        )

        body = tk.Frame(pref_canvas, bg=BG)
        body_window = pref_canvas.create_window(
            (0, 0),
            window=body,
            anchor="nw"
        )

        def _sync_pref_scrollregion(_event=None):
            pref_canvas.configure(scrollregion=pref_canvas.bbox("all"))

        def _sync_pref_width(event):
            # Mantiene el contenido al ancho visible del canvas.
            pref_canvas.itemconfigure(body_window, width=event.width)

        body.bind("<Configure>", _sync_pref_scrollregion)
        pref_canvas.bind("<Configure>", _sync_pref_width)
        pref_canvas.configure(yscrollcommand=pref_scrollbar.set)

        pref_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        pref_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _pref_mousewheel(event):
            if getattr(event, "delta", 0):
                pref_canvas.yview_scroll(int(-2 * (event.delta / 120)), "units")
            elif getattr(event, "num", None) == 4:
                pref_canvas.yview_scroll(-2, "units")
            elif getattr(event, "num", None) == 5:
                pref_canvas.yview_scroll(2, "units")

        def _bind_pref_scroll(_event=None):
            pref_canvas.bind_all("<MouseWheel>", _pref_mousewheel)
            pref_canvas.bind_all("<Button-4>", _pref_mousewheel)
            pref_canvas.bind_all("<Button-5>", _pref_mousewheel)

        def _unbind_pref_scroll(_event=None):
            pref_canvas.unbind_all("<MouseWheel>")
            pref_canvas.unbind_all("<Button-4>")
            pref_canvas.unbind_all("<Button-5>")

        # Toda la ventana de preferencias responde a la rueda.
        pref_canvas.bind("<Enter>", _bind_pref_scroll)
        pref_canvas.bind("<Leave>", _unbind_pref_scroll)
        body.bind("<Enter>", _bind_pref_scroll)
        body.bind("<Leave>", _unbind_pref_scroll)

        content = tk.Frame(body, bg=BG)
        content.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        controls = tk.Frame(content, bg=BG, width=470)
        controls.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))
        controls.pack_propagate(False)

        preview_side = tk.Frame(content, bg=BG_PANEL, width=360, height=500)
        preview_side.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        preview_side.pack_propagate(False)

        tk.Label(
            controls, text="APARIENCIAS PREDEFINIDAS",
            font=self.font_small, fg=TEXT_DIM, bg=BG
        ).pack(anchor="w", pady=(0, 6))

        preset_frame = tk.Frame(controls, bg=BG)
        preset_frame.pack(fill=tk.X)

        current = self._theme_dict_from_globals()
        color_vars = {
            "BG": tk.StringVar(value=current["BG"]),
            "BG_PANEL": tk.StringVar(value=current["BG_PANEL"]),
            "BG_PANEL2": tk.StringVar(value=current["BG_PANEL2"]),
            "PRIMARY": tk.StringVar(value=current["PRIMARY"]),
            "PRIMARY_L": tk.StringVar(value=current["PRIMARY_L"]),
            "SECONDARY": tk.StringVar(value=current["SECONDARY"]),
            "TEXT": tk.StringVar(value=current["TEXT"]),
            "TEXT_DIM": tk.StringVar(value=current["TEXT_DIM"]),
            "GOOD": tk.StringVar(value=current["GOOD"]),
            "DANGER": tk.StringVar(value=current["DANGER"]),
        }

        # Valores internos que no se muestran como selector principal.
        hidden_colors = {
            "PRIMARY_D": current["PRIMARY_D"],
            "PRIMARY_DIM": current["PRIMARY_DIM"],
            "SECONDARY_D": current["SECONDARY_D"],
            "SECONDARY_DIM": current["SECONDARY_DIM"],
        }

        tk.Label(
            preview_side, text="VISUALIZACIÓN PREVIA",
            font=self.font_small, fg=ORANGE, bg=BG_PANEL
        ).pack(anchor="w", padx=12, pady=(12, 4))

        tk.Label(
            preview_side,
            text="Los cambios se muestran aquí antes de guardarlos.",
            font=self.font_small, fg=TEXT_DIM, bg=BG_PANEL
        ).pack(anchor="w", padx=12, pady=(0, 8))

        preview = tk.Canvas(
            preview_side, bg=BG, highlightthickness=0
        )
        preview.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        def safe_color(key, fallback):
            value = color_vars[key].get().strip()
            if re.match(r"^#[0-9a-fA-F]{6}$", value):
                return value
            return fallback

        def refresh_preview(*_):
            preview.delete("all")
            preview.update_idletasks()
            w = max(preview.winfo_width(), 300)
            h = max(preview.winfo_height(), 380)

            bg = safe_color("BG", BG)
            panel = safe_color("BG_PANEL", BG_PANEL)
            panel2 = safe_color("BG_PANEL2", BG_PANEL2)
            pri = safe_color("PRIMARY", ORANGE)
            pril = safe_color("PRIMARY_L", ORANGE_L)
            sec = safe_color("SECONDARY", TURQUOISE)
            text = safe_color("TEXT", TEXT)
            dim = safe_color("TEXT_DIM", TEXT_DIM)
            good = safe_color("GOOD", GREEN)

            preview.configure(bg=bg)

            # Marco general.
            preview.create_rectangle(8, 8, w-8, h-8, fill=bg, outline=pri, width=1)

            # Top bar.
            preview.create_rectangle(18, 18, w-18, 58, fill=panel2, outline="")
            preview.create_text(
                30, 38, text="ULTRON // CORE",
                anchor="w", fill=pri, font=self.font_small
            )
            preview.create_text(
                w-30, 38, text="● ONLINE",
                anchor="e", fill=sec, font=self.font_small
            )

            # Panel de módulos.
            left_w = int(w * 0.34)
            preview.create_rectangle(
                18, 70, left_w, h-85,
                fill=panel, outline=hidden_colors["PRIMARY_DIM"], width=1
            )
            preview.create_text(
                30, 90, text="MODULES",
                anchor="w", fill=pri, font=self.font_small
            )

            module_names = [
                "01  CONCIENCIA",
                "02  SISTEMA",
                "03  PREFERENCIAS",
                "04  RED",
                "05  SEGURIDAD",
                "06  ARCHIVOS",
            ]
            yy = 112
            for i, name in enumerate(module_names):
                preview.create_rectangle(
                    28, yy, left_w-10, yy+34,
                    fill=panel2,
                    outline=pri if i == 2 else hidden_colors["PRIMARY_DIM"],
                    width=1
                )
                preview.create_text(
                    39, yy+17, text=name,
                    anchor="w",
                    fill=pril if i == 2 else pri,
                    font=self.font_small
                )
                yy += 42

            # Centro / core.
            center_x = int((left_w + (w-18)) / 2)
            center_y = int(h * 0.43)
            r = min(int((w-left_w)*0.23), 82)

            for rr, width in [(r+28, 1), (r+14, 2), (r, 2), (r-16, 2)]:
                preview.create_oval(
                    center_x-rr, center_y-rr,
                    center_x+rr, center_y+rr,
                    outline=pri, width=width
                )

            preview.create_oval(
                center_x-r//2, center_y-r//2,
                center_x+r//2, center_y+r//2,
                fill=panel2, outline=pril, width=2
            )
            preview.create_oval(
                center_x-16, center_y-16,
                center_x+16, center_y+16,
                fill=pril, outline=""
            )

            # Métricas inferiores.
            metric_y = h - 70
            metric_w = max(58, int((w-56)/4))
            for i, label in enumerate(("CPU", "RAM", "DISK", "NET")):
                x1 = 18 + i*(metric_w+6)
                x2 = x1 + metric_w
                preview.create_rectangle(
                    x1, metric_y, x2, h-20,
                    fill=panel, outline=""
                )
                preview.create_text(
                    (x1+x2)/2, metric_y+14,
                    text=label, fill=dim, font=self.font_small
                )
                preview.create_text(
                    (x1+x2)/2, metric_y+34,
                    text="OK" if label == "NET" else "42%",
                    fill=good if label == "NET" else pri,
                    font=self.font_small
                )

            preview.create_text(
                center_x, center_y + r + 48,
                text="LIVE THEME PREVIEW",
                fill=text, font=self.font_small
            )

        def build_theme_from_vars():
            return {
                "BG": safe_color("BG", BG),
                "BG_PANEL": safe_color("BG_PANEL", BG_PANEL),
                "BG_PANEL2": safe_color("BG_PANEL2", BG_PANEL2),
                "PRIMARY": safe_color("PRIMARY", ORANGE),
                "PRIMARY_L": safe_color("PRIMARY_L", ORANGE_L),
                "PRIMARY_D": hidden_colors["PRIMARY_D"],
                "PRIMARY_DIM": hidden_colors["PRIMARY_DIM"],
                "SECONDARY": safe_color("SECONDARY", TURQUOISE),
                "SECONDARY_D": hidden_colors["SECONDARY_D"],
                "SECONDARY_DIM": hidden_colors["SECONDARY_DIM"],
                "TEXT": safe_color("TEXT", TEXT),
                "TEXT_DIM": safe_color("TEXT_DIM", TEXT_DIM),
                "GOOD": safe_color("GOOD", GREEN),
                "DANGER": safe_color("DANGER", RED),
            }

        def load_vars_from_theme(theme):
            visible_keys = (
                "BG", "BG_PANEL", "BG_PANEL2", "PRIMARY", "PRIMARY_L",
                "SECONDARY", "TEXT", "TEXT_DIM", "GOOD", "DANGER"
            )
            for key in visible_keys:
                color_vars[key].set(theme[key])

            for key in hidden_colors:
                hidden_colors[key] = theme[key]

            refresh_preview()

        def apply_preset(name):
            theme = THEMES[name].copy()
            load_vars_from_theme(theme)
            self._apply_theme_live(theme)
            save_theme_config({"theme": name})
            self._add_log(f"Apariencia aplicada en vivo: {name}")
            status.configure(text=f"● {name} APLICADO", fg=TURQUOISE)

        for name in THEMES:
            btn = tk.Button(
                preset_frame,
                text=name,
                font=self.font_small,
                fg=ORANGE,
                bg=BG_PANEL2,
                activeforeground=ORANGE_L,
                activebackground=GRAY,
                relief=tk.FLAT,
                cursor="hand2",
                padx=9,
                pady=7,
                command=lambda n=name: apply_preset(n)
            )
            btn.pack(side=tk.LEFT, padx=3, pady=4)

        tk.Frame(controls, bg=GRAY2, height=1).pack(fill=tk.X, pady=14)

        tk.Label(
            controls, text="CREAR APARIENCIA PERSONALIZADA",
            font=self.font_small, fg=ORANGE, bg=BG
        ).pack(anchor="w", pady=(0, 6))

        tk.Label(
            controls,
            text=(
                "Cambia los colores y observa el resultado en la vista previa. "
                "Al aplicar, toda la interfaz cambia inmediatamente."
            ),
            font=self.font_small,
            fg=TEXT_DIM,
            bg=BG,
            justify="left",
            wraplength=530
        ).pack(anchor="w", pady=(0, 10))

        grid = tk.Frame(controls, bg=BG)
        grid.pack(fill=tk.X)

        labels = [
            ("Fondo principal", "BG"),
            ("Panel", "BG_PANEL"),
            ("Panel secundario", "BG_PANEL2"),
            ("Color primario", "PRIMARY"),
            ("Brillo primario", "PRIMARY_L"),
            ("Color secundario", "SECONDARY"),
            ("Texto", "TEXT"),
            ("Texto tenue", "TEXT_DIM"),
            ("Estado OK", "GOOD"),
            ("Alerta", "DANGER"),
        ]

        for i, (label, key) in enumerate(labels):
            row = i
            tk.Label(
                grid, text=label, font=self.font_small,
                fg=TEXT_DIM, bg=BG, width=18, anchor="w"
            ).grid(row=row, column=0, sticky="w", padx=(0, 6), pady=4)

            entry = tk.Entry(
                grid,
                textvariable=color_vars[key],
                width=12,
                font=self.font_mono,
                bg=BG_PANEL2,
                fg=TEXT,
                insertbackground=ORANGE,
                relief=tk.FLAT
            )
            entry.grid(row=row, column=1, padx=4, pady=4)

            tk.Button(
                grid,
                text="ELEGIR",
                font=self.font_small,
                fg=ORANGE,
                bg=BG_PANEL2,
                activeforeground=ORANGE_L,
                activebackground=GRAY,
                relief=tk.FLAT,
                width=9,
                command=lambda v=color_vars[key]: self._pick_color(v)
            ).grid(row=row, column=2, padx=(6, 0), pady=4)

        # Preview en tiempo real al editar cualquier código hexadecimal.
        for var in color_vars.values():
            var.trace_add("write", refresh_preview)

        tk.Frame(controls, bg=GRAY2, height=1).pack(fill=tk.X, pady=14)

        tk.Label(
            controls, text="AUDIO",
            font=self.font_small, fg=ORANGE, bg=BG
        ).pack(anchor="w", pady=(0, 6))

        tk.Label(
            controls,
            text="Automático usa los dispositivos predeterminados del sistema.",
            font=self.font_small,
            fg=TEXT_DIM,
            bg=BG,
            wraplength=430,
            justify="left"
        ).pack(anchor="w", pady=(0, 8))

        audio_grid = tk.Frame(controls, bg=BG)
        audio_grid.pack(fill=tk.X)

        input_options = ["Automático"] + self._list_audio_sources()
        output_options = ["Automático"] + self._list_audio_sinks()

        input_var = tk.StringVar(
            value=self.audio_input_device or "Automático"
        )
        output_var = tk.StringVar(
            value=self.audio_output_device or "Automático"
        )
        volume_var = tk.IntVar(value=self.ultron_volume)

        tk.Label(
            audio_grid, text="Entrada",
            font=self.font_small, fg=TEXT_DIM, bg=BG, width=14, anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=4)

        input_menu = tk.OptionMenu(audio_grid, input_var, *input_options)
        input_menu.configure(
            bg=BG_PANEL2, fg=TEXT, relief=tk.FLAT,
            activebackground=GRAY, activeforeground=ORANGE_L,
            highlightthickness=0, width=28
        )
        input_menu["menu"].configure(bg=BG_PANEL2, fg=TEXT)
        input_menu.grid(row=0, column=1, sticky="w", pady=4)

        tk.Label(
            audio_grid, text="Salida",
            font=self.font_small, fg=TEXT_DIM, bg=BG, width=14, anchor="w"
        ).grid(row=1, column=0, sticky="w", pady=4)

        output_menu = tk.OptionMenu(audio_grid, output_var, *output_options)
        output_menu.configure(
            bg=BG_PANEL2, fg=TEXT, relief=tk.FLAT,
            activebackground=GRAY, activeforeground=ORANGE_L,
            highlightthickness=0, width=28
        )
        output_menu["menu"].configure(bg=BG_PANEL2, fg=TEXT)
        output_menu.grid(row=1, column=1, sticky="w", pady=4)

        tk.Label(
            audio_grid, text="Volumen ULTRON",
            font=self.font_small, fg=TEXT_DIM, bg=BG, width=14, anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=6)

        volume_scale = tk.Scale(
            audio_grid,
            from_=10, to=100,
            orient=tk.HORIZONTAL,
            variable=volume_var,
            bg=BG,
            fg=TEXT,
            troughcolor=BG_PANEL2,
            activebackground=ORANGE,
            highlightthickness=0,
            length=220
        )
        volume_scale.grid(row=2, column=1, sticky="w", pady=2)

        audio_buttons = tk.Frame(controls, bg=BG)
        audio_buttons.pack(fill=tk.X, pady=(8, 0))

        def apply_audio_preferences():
            self.audio_input_device = input_var.get()
            self.audio_output_device = output_var.get()
            self.ultron_volume = volume_var.get()
            self._add_log(
                f"Audio actualizado: entrada={self.audio_input_device}, "
                f"salida={self.audio_output_device}, volumen={self.ultron_volume}%"
            )

        tk.Button(
            audio_buttons,
            text="[ PROBAR MICRÓFONO ]",
            font=self.font_small,
            fg=TURQUOISE,
            bg=BG_PANEL2,
            relief=tk.FLAT,
            command=lambda: (
                apply_audio_preferences(),
                self._test_microphone(win)
            ),
            padx=10, pady=7
        ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(
            audio_buttons,
            text="[ PROBAR VOZ ]",
            font=self.font_small,
            fg=ORANGE,
            bg=BG_PANEL2,
            relief=tk.FLAT,
            command=lambda: (
                apply_audio_preferences(),
                self._test_voice_output(win)
            ),
            padx=10, pady=7
        ).pack(side=tk.LEFT)

        actions = tk.Frame(controls, bg=BG)
        actions.pack(fill=tk.X, pady=(16, 0))

        def preview_on_real_ui():
            theme = build_theme_from_vars()
            self._apply_theme_live(theme)
            self._add_log("Vista previa aplicada temporalmente")
            status.configure(text="● PREVIEW ACTIVO", fg=TURQUOISE)

        def save_custom():
            custom = build_theme_from_vars()
            save_theme_config({
                "theme": "CUSTOM",
                "custom_theme": custom
            })
            self._apply_theme_live(custom)
            self._add_log("Apariencia personalizada guardada y aplicada")
            status.configure(text="● PERSONALIZADO GUARDADO", fg=GREEN)

        tk.Button(
            actions,
            text="[ PROBAR EN ULTRON ]",
            font=self.font_small,
            fg=TURQUOISE,
            bg=BG_PANEL2,
            activeforeground=TEXT,
            activebackground=GRAY,
            relief=tk.FLAT,
            padx=13,
            pady=8,
            command=preview_on_real_ui
        ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(
            actions,
            text="[ GUARDAR Y APLICAR ]",
            font=self.font_small,
            fg=ORANGE,
            bg=BG_PANEL2,
            activeforeground=ORANGE_L,
            activebackground=GRAY,
            relief=tk.FLAT,
            padx=13,
            pady=8,
            command=save_custom
        ).pack(side=tk.RIGHT)

        preview.bind("<Configure>", refresh_preview)
        refresh_preview()

    def _show_module(self, title, content):
        win = tk.Toplevel(self.root)
        win.title(f"ULTRON — {title}")
        win.configure(bg=BG)
        win.geometry("640x440")
        win.transient(self.root)

        header = tk.Frame(win, bg=BG_PANEL2, height=42)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header, text=f"// {title}",
            font=self.font_title, fg=ORANGE, bg=BG_PANEL2
        ).pack(side=tk.LEFT, padx=16, pady=8)

        text_frame = tk.Frame(win, bg=BG)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        txt = tk.Text(
            text_frame, bg="#080808", fg=TEXT, font=self.font_mono,
            relief=tk.FLAT, padx=14, pady=12, wrap=tk.WORD
        )
        txt_scroll = tk.Scrollbar(
            text_frame,
            orient="vertical",
            command=txt.yview,
            bg=BG_PANEL2,
            troughcolor=BG,
            activebackground=ORANGE_D
        )
        txt.configure(yscrollcommand=txt_scroll.set)

        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        txt_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        txt.insert(tk.END, content)
        txt.configure(state=tk.DISABLED)

        btn_frame = tk.Frame(win, bg=BG)
        btn_frame.pack(fill=tk.X, pady=8)
        tk.Button(
            btn_frame, text="[ CERRAR ]", font=self.font_small,
            fg=ORANGE, bg=BG_PANEL2, relief=tk.FLAT,
            command=win.destroy, padx=18, pady=6
        ).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = UltronGUI(root)
    root.mainloop()
                     

