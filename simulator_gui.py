#python -m pip install PyQt5
"""
CSEN601 - Package 3: Double Big Harvard Combo
Pipeline Simulator GUI
"""

import sys
import subprocess
import os
import re
import tempfile
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QTextEdit, QTableWidget,
    QTableWidgetItem, QSplitter, QFrame, QFileDialog, QMessageBox,
    QScrollArea, QGroupBox, QHeaderView, QTabWidget, QSlider,
    QStatusBar, QSizePolicy
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation,
    QEasingCurve, QRect, QSize
)
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QTextCursor, QPixmap,
    QLinearGradient, QPainter, QBrush, QPen, QFontDatabase
)

# ─────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────
BG_DARK      = "#0D1117"
BG_MID       = "#161B22"
BG_CARD      = "#1C2128"
BG_HOVER     = "#21262D"
ACCENT_BLUE  = "#58A6FF"
ACCENT_GREEN = "#3FB950"
ACCENT_RED   = "#F85149"
ACCENT_GOLD  = "#D29922"
ACCENT_PURP  = "#BC8CFF"
TEXT_PRIMARY = "#E6EDF3"
TEXT_MUTED   = "#8B949E"
BORDER       = "#30363D"

STAGE_COLORS = {
    "IF":  "#1F6FEB",
    "ID":  "#388BFD",
    "EX":  "#3FB950",
    "MEM": "#D29922",
    "WB":  "#BC8CFF",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BG_DARK};
    color: {TEXT_PRIMARY};
    font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
}}

QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 8px;
    font-size: 11px;
    font-weight: bold;
    color: {TEXT_MUTED};
    background-color: {BG_CARD};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
    color: {ACCENT_BLUE};
    letter-spacing: 1px;
    text-transform: uppercase;
}}

QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 6px;
    background-color: {BG_CARD};
}}
QTabBar::tab {{
    background: {BG_MID};
    color: {TEXT_MUTED};
    padding: 8px 16px;
    border: 1px solid {BORDER};
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 0.5px;
}}
QTabBar::tab:selected {{
    background: {BG_CARD};
    color: {ACCENT_BLUE};
    border-bottom: 2px solid {ACCENT_BLUE};
}}
QTabBar::tab:hover {{
    background: {BG_HOVER};
    color: {TEXT_PRIMARY};
}}

QTextEdit {{
    background-color: {BG_MID};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    font-size: 12px;
    padding: 8px;
    selection-background-color: {ACCENT_BLUE};
}}

QTableWidget {{
    background-color: {BG_MID};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    gridline-color: {BORDER};
    font-size: 11px;
    alternate-background-color: {BG_CARD};
}}
QTableWidget::item {{
    padding: 4px 8px;
    border: none;
}}
QTableWidget::item:selected {{
    background-color: #1F6FEB33;
    color: {TEXT_PRIMARY};
}}
QHeaderView::section {{
    background-color: {BG_DARK};
    color: {ACCENT_BLUE};
    padding: 6px 8px;
    border: none;
    border-right: 1px solid {BORDER};
    border-bottom: 1px solid {BORDER};
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

QPushButton {{
    background-color: {BG_HOVER};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 8px 18px;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 0.5px;
}}
QPushButton:hover {{
    background-color: #30363D;
    border-color: {ACCENT_BLUE};
    color: {ACCENT_BLUE};
}}
QPushButton:pressed {{
    background-color: #1F6FEB22;
}}
QPushButton:disabled {{
    color: {TEXT_MUTED};
    border-color: {BORDER};
}}

QPushButton#btn_run {{
    background-color: #238636;
    border-color: #2EA043;
    color: #FFFFFF;
}}
QPushButton#btn_run:hover {{
    background-color: #2EA043;
    border-color: #3FB950;
}}

QPushButton#btn_step {{
    background-color: #1F6FEB;
    border-color: #388BFD;
    color: #FFFFFF;
}}
QPushButton#btn_step:hover {{
    background-color: #388BFD;
}}

QPushButton#btn_reset {{
    background-color: #6E40C9;
    border-color: #8B5CF6;
    color: #FFFFFF;
}}
QPushButton#btn_reset:hover {{
    background-color: #8B5CF6;
}}

QPushButton#btn_load {{
    background-color: {BG_HOVER};
    border-color: {ACCENT_GOLD};
    color: {ACCENT_GOLD};
}}
QPushButton#btn_load:hover {{
    background-color: #D2992222;
}}

QLabel#lbl_title {{
    font-size: 20px;
    font-weight: bold;
    color: {ACCENT_BLUE};
    letter-spacing: 2px;
}}
QLabel#lbl_subtitle {{
    font-size: 11px;
    color: {TEXT_MUTED};
    letter-spacing: 1px;
}}
QLabel#lbl_cycle {{
    font-size: 28px;
    font-weight: bold;
    color: {ACCENT_GOLD};
}}
QLabel#lbl_stage_header {{
    font-size: 10px;
    font-weight: bold;
    color: {TEXT_MUTED};
    letter-spacing: 2px;
}}

QScrollBar:vertical {{
    background: {BG_MID};
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT_MUTED};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: {BG_MID};
    height: 8px;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER};
    border-radius: 4px;
}}

QStatusBar {{
    background: {BG_MID};
    color: {TEXT_MUTED};
    border-top: 1px solid {BORDER};
    font-size: 11px;
}}

QSplitter::handle {{
    background-color: {BORDER};
    width: 2px;
    height: 2px;
}}

QSlider::groove:horizontal {{
    border: none;
    height: 4px;
    background: {BORDER};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {ACCENT_BLUE};
    border: none;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QSlider::sub-page:horizontal {{
    background: {ACCENT_BLUE};
    border-radius: 2px;
}}
"""

# ─────────────────────────────────────────────
#  SIMULATOR ENGINE  (pure Python re-implementation)
#  Mirrors the C logic exactly so the GUI can
#  step through without calling the C binary.
# ─────────────────────────────────────────────
OPCODE_NAMES = {
    0: "ADD", 1: "SUB", 2: "MUL",  3: "MOVI",
    4: "BEQZ", 5: "ANDI", 6: "EOR", 7: "BR",
    8: "SLC",  9: "SRC",  10: "LDR", 11: "STR",
}
MNEMONIC_MAP = {v: k for k, v in OPCODE_NAMES.items()}

def to_int8(v):
    v = v & 0xFF
    return v - 256 if v >= 128 else v

def to_uint8(v):
    return v & 0xFF

class SimulatorEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.instruction_memory = [0] * 1024
        self.data_memory        = [0] * 2048
        self.registers          = [0] * 64
        self.PC                 = 0
        self.SREG               = dict(C=0, V=0, N=0, S=0, Z=0)
        self.instruction_count  = 0
        self.cycle              = 0
        self.done               = False

        # Pipeline buffers
        self.IF_ID = dict(instruction=0, pc=0, valid=False)
        self.ID_EX = dict(
            raw=0, opcode=0, r1=0, r2=0, immediate=0,
            r1Value=0, r2Value=0, pc=0, valid=False
        )

        # Hazard / forwarding state
        self.flush_pipeline     = False
        self.branch_target      = 0
        self.forwarding_enabled = False
        self.forwarded_register = 0
        self.forwarded_value    = 0

        # Log of events per cycle
        self.cycle_log = []   # list of dicts, one per cycle

    # ── parser ──────────────────────────────────────────────────────
    def load_program(self, text: str):
        self.reset()
        lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
        for idx, line in enumerate(lines):
            parts = line.split()
            mnemonic = parts[0].upper()
            opcode = MNEMONIC_MAP.get(mnemonic, -1)
            if opcode == -1:
                continue
            r_type = opcode in (0,1,2,6,7)   # ADD SUB MUL EOR BR
            instruction = 0
            if r_type:
                r1 = int(parts[1][1:]) if len(parts) > 1 else 0
                r2 = int(parts[2][1:]) if len(parts) > 2 else 0
                instruction = (opcode << 12) | (r1 << 6) | r2
            else:
                r1  = int(parts[1][1:]) if len(parts) > 1 else 0
                imm = int(parts[2])      if len(parts) > 2 else 0
                instruction = (opcode << 12) | (r1 << 6) | (imm & 0x3F)
            self.instruction_memory[idx] = instruction
            self.instruction_count += 1

    # ── flag helpers ─────────────────────────────────────────────────
    def _update_zero(self, result):
        self.SREG['Z'] = 1 if to_int8(result) == 0 else 0

    def _update_negative(self, result):
        self.SREG['N'] = 1 if to_int8(result) < 0 else 0

    def _update_carry(self, v1, v2):
        u = to_uint8(v1) + to_uint8(v2)
        self.SREG['C'] = (u >> 8) & 1

    def _update_overflow_add(self, v1, v2, result):
        i1, i2, ir = to_int8(v1), to_int8(v2), to_int8(result)
        self.SREG['V'] = 1 if (i1>=0 and i2>=0 and ir<0) or (i1<0 and i2<0 and ir>=0) else 0

    def _update_overflow_sub(self, v1, v2, result):
        i1, i2, ir = to_int8(v1), to_int8(v2), to_int8(result)
        self.SREG['V'] = 1 if (i1>=0 and i2<0 and ir<0) or (i1<0 and i2>=0 and ir>=0) else 0

    def _update_sign(self):
        self.SREG['S'] = self.SREG['N'] ^ self.SREG['V']

    # ── single-cycle step ─────────────────────────────────────────────
    def step(self):
        """Run one clock cycle. Returns a dict describing what happened."""
        if self.done:
            return None

        log = {
            "cycle":    self.cycle + 1,
            "fetch":    None,
            "decode":   None,
            "execute":  None,
            "reg_changes":  [],
            "mem_changes":  [],
            "sreg":     dict(self.SREG),
            "flushed":  False,
            "forwarded": False,
            "pipeline_bubble": False,
        }

        self.cycle += 1

        # ── EXECUTE ──────────────────────────────────────────
        ex_log = self._execute()
        log["execute"] = ex_log
        if ex_log:
            log["reg_changes"] += ex_log.get("reg_changes", [])
            log["mem_changes"] += ex_log.get("mem_changes", [])
            log["sreg"] = dict(self.SREG)

        # ── DECODE ───────────────────────────────────────────
        dec_log = self._decode()
        log["decode"] = dec_log
        if dec_log and dec_log.get("forwarded"):
            log["forwarded"] = True

        # ── FETCH ────────────────────────────────────────────
        if self.PC < self.instruction_count:
            fetch_log = self._fetch()
            log["fetch"] = fetch_log
            if fetch_log and fetch_log.get("flushed"):
                log["flushed"] = True
        else:
            if not self.IF_ID['valid'] and not self.ID_EX['valid']:
                self.done = True

        if not log["fetch"] and not log["decode"] and not log["execute"]:
            self.done = True

        self.cycle_log.append(log)
        return log

    def _fetch(self):
        if self.flush_pipeline:
            self.IF_ID['valid'] = False
            self.flush_pipeline = False
            return {"flushed": True, "pc": None, "instruction": None}

        instr = self.instruction_memory[self.PC]
        self.IF_ID = dict(instruction=instr, pc=self.PC, valid=True)
        old_pc = self.PC
        self.PC += 1
        return {"flushed": False, "pc": old_pc, "instruction": instr}

    def _decode(self):
        self.ID_EX['valid'] = False
        if not self.IF_ID['valid']:
            return None

        instr   = self.IF_ID['instruction']
        opcode  = (instr >> 12) & 0xF
        r1      = (instr >>  6) & 0x3F
        r2      =  instr        & 0x3F
        imm_raw =  instr        & 0x3F
        # sign-extend 6-bit immediate
        if imm_raw & 0x20:
            imm_raw |= 0xC0
        immediate = to_int8(imm_raw)

        r1Value = to_int8(self.registers[r1])
        r2Value = to_int8(self.registers[r2])
        forwarded = False
        if self.forwarding_enabled:
            if r1 == self.forwarded_register:
                r1Value = self.forwarded_value
                forwarded = True
            if r2 == self.forwarded_register:
                r2Value = self.forwarded_value
                forwarded = True

        self.ID_EX = dict(
            raw=instr, opcode=opcode, r1=r1, r2=r2,
            immediate=immediate, r1Value=r1Value, r2Value=r2Value,
            pc=self.IF_ID['pc'], valid=True
        )
        self.forwarding_enabled = False
        self.IF_ID['valid'] = False

        return {
            "instruction": instr,
            "opcode": opcode,
            "r1": r1, "r2": r2,
            "immediate": immediate,
            "r1Value": r1Value, "r2Value": r2Value,
            "forwarded": forwarded,
        }

    def _execute(self):
        self.forwarding_enabled = False
        if not self.ID_EX['valid']:
            return None

        opcode = self.ID_EX['opcode']
        r1     = self.ID_EX['r1']
        r2     = self.ID_EX['r2']
        imm    = self.ID_EX['immediate']
        val1   = self.ID_EX['r1Value']
        val2   = self.ID_EX['r2Value']
        result = 0

        reg_changes = []
        mem_changes = []

        def set_reg(reg, val):
            val = to_int8(val)
            old = to_int8(self.registers[reg])
            self.registers[reg] = val & 0xFF
            if old != val:
                reg_changes.append((reg, old, val))

        name = OPCODE_NAMES.get(opcode, "???")

        if opcode == 0:   # ADD
            result = val1 + val2
            set_reg(r1, result)
            self._update_zero(result); self._update_negative(result)
            self._update_carry(val1, val2)
            self._update_overflow_add(val1, val2, result)
            self._update_sign()
            op_str = f"ADD R{r1}, R{r2}  →  {to_int8(val1)} + {to_int8(val2)} = {to_int8(result)}"

        elif opcode == 1: # SUB
            result = val1 - val2
            set_reg(r1, result)
            self._update_zero(result); self._update_negative(result)
            self._update_overflow_sub(val1, val2, result)
            self._update_sign()
            op_str = f"SUB R{r1}, R{r2}  →  {to_int8(val1)} - {to_int8(val2)} = {to_int8(result)}"

        elif opcode == 2: # MUL
            result = val1 * val2
            set_reg(r1, result)
            self._update_zero(result); self._update_negative(result); self._update_sign()
            op_str = f"MUL R{r1}, R{r2}  →  {to_int8(val1)} × {to_int8(val2)} = {to_int8(result)}"

        elif opcode == 3: # MOVI
            result = imm
            set_reg(r1, result)
            op_str = f"MOVI R{r1}, {imm}  →  R{r1} = {to_int8(imm)}"

        elif opcode == 4: # BEQZ
            if val1 == 0:
                self.branch_target  = self.ID_EX['pc'] + 1 + imm
                self.PC             = self.branch_target
                self.flush_pipeline = True
                op_str = f"BEQZ R{r1}, {imm}  →  TAKEN → PC={self.PC}"
            else:
                op_str = f"BEQZ R{r1}, {imm}  →  NOT TAKEN  (R{r1}={val1})"

        elif opcode == 5: # ANDI
            result = val1 & imm
            set_reg(r1, result)
            self._update_zero(result); self._update_negative(result); self._update_sign()
            op_str = f"ANDI R{r1}, {imm}  →  {to_int8(val1)} & {imm} = {to_int8(result)}"

        elif opcode == 6: # EOR
            result = val1 ^ val2
            set_reg(r1, result)
            self._update_zero(result); self._update_negative(result); self._update_sign()
            op_str = f"EOR R{r1}, R{r2}  →  {to_int8(val1)} ^ {to_int8(val2)} = {to_int8(result)}"

        elif opcode == 7: # BR
            high = to_uint8(val1) << 8
            low  = to_uint8(val2)
            self.branch_target  = high | low
            self.PC             = self.branch_target
            self.flush_pipeline = True
            self.IF_ID['valid'] = False
            op_str = f"BR R{r1}, R{r2}  →  JUMP → PC={self.PC}"

        elif opcode == 8: # SLC
            shamt = imm % 8
            u = to_uint8(val1)
            if shamt == 0:
                result = val1
            else:
                result = ((u << shamt) | (u >> (8 - shamt))) & 0xFF
            set_reg(r1, result)
            self._update_zero(result); self._update_negative(result); self._update_sign()
            op_str = f"SLC R{r1}, {imm}  →  rotate_left({to_uint8(val1)}, {shamt}) = {result}"

        elif opcode == 9: # SRC
            shamt = imm % 8
            u = to_uint8(val1)
            if shamt == 0:
                result = val1
            else:
                result = ((u >> shamt) | (u << (8 - shamt))) & 0xFF
            set_reg(r1, result)
            self._update_zero(result); self._update_negative(result); self._update_sign()
            op_str = f"SRC R{r1}, {imm}  →  rotate_right({to_uint8(val1)}, {shamt}) = {result}"

        elif opcode == 10: # LDR
            addr = to_uint8(imm)
            result = self.data_memory[addr] if addr < 2048 else 0
            set_reg(r1, result)
            self._update_zero(result); self._update_negative(result); self._update_sign()
            op_str = f"LDR R{r1}, [{addr}]  →  MEM[{addr}]={to_int8(result)}"

        elif opcode == 11: # STR
            addr = to_uint8(imm)
            if addr < 2048:
                old = self.data_memory[addr]
                self.data_memory[addr] = to_int8(self.registers[r1])
                mem_changes.append((addr, old, self.data_memory[addr]))
            op_str = f"STR R{r1}, [{addr}]  →  MEM[{addr}] = {to_int8(self.registers[r1])}"
        else:
            op_str = f"UNKNOWN opcode={opcode}"

        # Enable forwarding for register-writing ops
        if opcode in (0,1,2,3,5,6):
            self.forwarding_enabled = True
            self.forwarded_register = r1
            self.forwarded_value    = to_int8(self.registers[r1])

        self.ID_EX['valid'] = False

        return {
            "opcode": opcode, "name": name, "op_str": op_str,
            "r1": r1, "r2": r2, "result": to_int8(result),
            "reg_changes": reg_changes,
            "mem_changes": mem_changes,
        }

    def is_finished(self):
        return self.done or (
            self.PC >= self.instruction_count
            and not self.IF_ID['valid']
            and not self.ID_EX['valid']
        )


# ─────────────────────────────────────────────
#  PIPELINE DIAGRAM WIDGET
# ─────────────────────────────────────────────
class PipelineDiagram(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._stages = {}   # stage_name -> (label, active, color)
        self._active = {}
        self._instructions = {s: "" for s in ["IF","ID","EX"]}

    def update_pipeline(self, fetch_log, decode_log, execute_log):
        self._instructions = {
            "IF": "",
            "ID": "",
            "EX": "",
        }
        if fetch_log and not fetch_log.get("flushed") and fetch_log.get("pc") is not None:
            self._instructions["IF"] = f"PC={fetch_log['pc']}"
        if decode_log:
            opc = decode_log.get("opcode", 0)
            self._instructions["ID"] = OPCODE_NAMES.get(opc, "???")
        if execute_log:
            self._instructions["EX"] = execute_log.get("name", "")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Background
        painter.fillRect(0, 0, w, h, QColor(BG_CARD))

        stages    = ["IF", "ID", "EX"]
        colors    = [QColor(STAGE_COLORS[s]) for s in stages]
        full_names = ["FETCH", "DECODE", "EXECUTE"]

        box_w = 160
        box_h = 90
        gap   = 40
        total = len(stages) * box_w + (len(stages)-1) * gap
        start_x = (w - total) // 2
        y = (h - box_h) // 2

        for i, (stage, color, full) in enumerate(zip(stages, colors, full_names)):
            x = start_x + i * (box_w + gap)
            instr_text = self._instructions.get(stage, "")
            active = bool(instr_text)

            # Arrow
            if i > 0:
                ax = x - gap
                ay = y + box_h // 2
                painter.setPen(QPen(QColor(BORDER), 2))
                painter.drawLine(ax, ay, x - 2, ay)
                # arrowhead
                painter.setBrush(QBrush(QColor(BORDER)))
                pts = [
                    (x-2, ay),
                    (x-10, ay-5),
                    (x-10, ay+5),
                ]
                from PyQt5.QtCore import QPoint
                from PyQt5.QtGui import QPolygon
                poly = QPolygon([QPoint(p[0], p[1]) for p in pts])
                painter.drawPolygon(poly)

            # Box shadow
            if active:
                shadow_color = QColor(color)
                shadow_color.setAlpha(40)
                painter.fillRect(x+4, y+4, box_w, box_h, shadow_color)

            # Box fill
            if active:
                grad = QLinearGradient(x, y, x, y + box_h)
                c1 = QColor(color); c1.setAlpha(200)
                c2 = QColor(color); c2.setAlpha(80)
                grad.setColorAt(0, c1)
                grad.setColorAt(1, c2)
                painter.fillRect(x, y, box_w, box_h, grad)
                painter.setPen(QPen(color, 2))
            else:
                painter.fillRect(x, y, box_w, box_h, QColor(BG_MID))
                painter.setPen(QPen(QColor(BORDER), 1))
            painter.drawRect(x, y, box_w, box_h)

            # Stage label
            lbl_font = QFont("JetBrains Mono", 9, QFont.Bold)
            painter.setFont(lbl_font)
            lbl_color = QColor(color) if active else QColor(TEXT_MUTED)
            painter.setPen(lbl_color)
            painter.drawText(x, y, box_w, 24, Qt.AlignCenter, full)

            # Divider
            painter.setPen(QPen(QColor(color if active else BORDER), 1))
            painter.drawLine(x, y+24, x+box_w, y+24)

            # Instruction text
            instr_font = QFont("JetBrains Mono", 11, QFont.Bold)
            painter.setFont(instr_font)
            painter.setPen(QColor(TEXT_PRIMARY if active else TEXT_MUTED))
            painter.drawText(x, y+24, box_w, box_h-24, Qt.AlignCenter,
                             instr_text if instr_text else "—")

        painter.end()


# ─────────────────────────────────────────────
#  SREG FLAG WIDGET
# ─────────────────────────────────────────────
class SREGWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(10)

        self._labels = {}
        flag_colors = {
            'C': ACCENT_BLUE,
            'V': ACCENT_GOLD,
            'N': ACCENT_RED,
            'S': ACCENT_PURP,
            'Z': ACCENT_GREEN,
        }

        for flag, color in flag_colors.items():
            box = QFrame()
            box.setFixedSize(60, 52)
            box.setStyleSheet(f"""
                QFrame {{
                    background: {BG_MID};
                    border: 1px solid {BORDER};
                    border-radius: 6px;
                }}
            """)
            vl = QVBoxLayout(box)
            vl.setContentsMargins(4, 2, 4, 2)
            vl.setSpacing(0)

            name_lbl = QLabel(flag)
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(f"font-size:9px; font-weight:bold; color:{color}; border:none;")

            val_lbl = QLabel("0")
            val_lbl.setAlignment(Qt.AlignCenter)
            val_lbl.setStyleSheet(f"font-size:18px; font-weight:bold; color:{TEXT_MUTED}; border:none;")

            vl.addWidget(name_lbl)
            vl.addWidget(val_lbl)
            self._labels[flag] = (box, val_lbl, color)
            layout.addWidget(box)

        layout.addStretch()

    def update_flags(self, sreg: dict):
        for flag, (box, val_lbl, color) in self._labels.items():
            val = sreg.get(flag, 0)
            val_lbl.setText(str(val))
            if val:
                val_lbl.setStyleSheet(
                    f"font-size:18px; font-weight:bold; color:{color}; border:none;")
                box.setStyleSheet(f"""
                    QFrame {{
                        background: {color}22;
                        border: 1px solid {color};
                        border-radius: 6px;
                    }}
                """)
            else:
                val_lbl.setStyleSheet(
                    f"font-size:18px; font-weight:bold; color:{TEXT_MUTED}; border:none;")
                box.setStyleSheet(f"""
                    QFrame {{
                        background: {BG_MID};
                        border: 1px solid {BORDER};
                        border-radius: 6px;
                    }}
                """)


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = SimulatorEngine()
        self._auto_timer = QTimer(self)
        self._auto_timer.timeout.connect(self._auto_step)
        self.setWindowTitle("CSEN601 — Package 3 Pipeline Simulator")
        self.resize(1400, 900)
        self.setMinimumSize(1100, 700)
        self._build_ui()
        self._apply_default_program()

    # ── UI Construction ───────────────────────────────────────────────
    def _build_ui(self):
        self.setStyleSheet(STYLESHEET)
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ─────────────────────────────────────────────────
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {BG_MID}, stop:0.5 #1A2035, stop:1 {BG_MID});
                border-bottom: 1px solid {BORDER};
            }}
        """)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 0, 20, 0)

        dot = QLabel("◈")
        dot.setStyleSheet(f"font-size:22px; color:{ACCENT_BLUE}; background:transparent; border:none;")
        title = QLabel("PIPELINE SIMULATOR")
        title.setObjectName("lbl_title")
        title.setStyleSheet(f"font-size:18px; font-weight:bold; color:{ACCENT_BLUE}; "
                             f"letter-spacing:3px; background:transparent; border:none;")
        sub = QLabel("Harvard · 3-Stage · Package 3")
        sub.setObjectName("lbl_subtitle")
        sub.setStyleSheet(f"font-size:10px; color:{TEXT_MUTED}; background:transparent; border:none;")

        vsep = QFrame()
        vsep.setFixedSize(1, 36)
        vsep.setStyleSheet(f"background:{BORDER};")

        self.lbl_cycle = QLabel("Cycle  0")
        self.lbl_cycle.setObjectName("lbl_cycle")
        self.lbl_cycle.setStyleSheet(
            f"font-size:20px; font-weight:bold; color:{ACCENT_GOLD}; background:transparent; border:none;")

        title_col = QVBoxLayout()
        title_col.setSpacing(0)
        title_col.addWidget(title)
        title_col.addWidget(sub)

        hl.addWidget(dot)
        hl.addSpacing(8)
        hl.addLayout(title_col)
        hl.addStretch()
        hl.addWidget(vsep)
        hl.addSpacing(16)
        hl.addWidget(self.lbl_cycle)
        root.addWidget(header)

        # ── Body (splitter) ─────────────────────────────────────────
        body = QSplitter(Qt.Horizontal)
        body.setHandleWidth(2)

        # LEFT PANEL
        left = QWidget()
        left.setMinimumWidth(320)
        left.setMaximumWidth(420)
        ll = QVBoxLayout(left)
        ll.setContentsMargins(12, 12, 6, 12)
        ll.setSpacing(10)

        # Program editor
        prog_grp = QGroupBox("ASSEMBLY PROGRAM")
        pg = QVBoxLayout(prog_grp)
        self.program_editor = QTextEdit()
        self.program_editor.setFont(QFont("JetBrains Mono", 11))
        self.program_editor.setPlaceholderText("# Enter assembly here\nMOVI R1 5\nADD R1 R2\n...")
        pg.addWidget(self.program_editor)

        btn_load_file = QPushButton("📂  Load from File")
        btn_load_file.setObjectName("btn_load")
        btn_load_file.clicked.connect(self._load_file)
        pg.addWidget(btn_load_file)
        ll.addWidget(prog_grp, 3)

        # Control buttons
        ctrl_grp = QGroupBox("CONTROLS")
        cg = QVBoxLayout(ctrl_grp)

        btn_row1 = QHBoxLayout()
        self.btn_load = QPushButton("⚡  Load Program")
        self.btn_load.setObjectName("btn_load")
        self.btn_load.clicked.connect(self._load_program)
        self.btn_step = QPushButton("▶  Step")
        self.btn_step.setObjectName("btn_step")
        self.btn_step.clicked.connect(self._step)
        self.btn_step.setEnabled(False)
        btn_row1.addWidget(self.btn_load)
        btn_row1.addWidget(self.btn_step)

        btn_row2 = QHBoxLayout()
        self.btn_run = QPushButton("⏩  Run All")
        self.btn_run.setObjectName("btn_run")
        self.btn_run.clicked.connect(self._toggle_run)
        self.btn_run.setEnabled(False)
        self.btn_reset = QPushButton("↺  Reset")
        self.btn_reset.setObjectName("btn_reset")
        self.btn_reset.clicked.connect(self._reset)
        btn_row2.addWidget(self.btn_run)
        btn_row2.addWidget(self.btn_reset)

        spd_row = QHBoxLayout()
        spd_lbl = QLabel("Speed:")
        spd_lbl.setStyleSheet(f"color:{TEXT_MUTED}; font-size:10px; background:transparent;")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        self.speed_slider.setToolTip("Simulation speed (1=slow, 10=fast)")
        self.speed_lbl_val = QLabel("5")
        self.speed_lbl_val.setStyleSheet(f"color:{ACCENT_BLUE}; font-size:10px; background:transparent;")
        self.speed_slider.valueChanged.connect(
            lambda v: self.speed_lbl_val.setText(str(v)))
        spd_row.addWidget(spd_lbl)
        spd_row.addWidget(self.speed_slider)
        spd_row.addWidget(self.speed_lbl_val)

        cg.addLayout(btn_row1)
        cg.addLayout(btn_row2)
        cg.addLayout(spd_row)
        ll.addWidget(ctrl_grp)

        # SREG
        sreg_grp = QGroupBox("STATUS REGISTER  (SREG)")
        sg = QVBoxLayout(sreg_grp)
        self.sreg_widget = SREGWidget()
        sg.addWidget(self.sreg_widget)
        ll.addWidget(sreg_grp)

        body.addWidget(left)

        # RIGHT PANEL
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(6, 12, 12, 12)
        rl.setSpacing(10)

        # Pipeline diagram
        pipe_grp = QGroupBox("PIPELINE DIAGRAM")
        pg2 = QVBoxLayout(pipe_grp)
        self.pipeline_diagram = PipelineDiagram()
        pg2.addWidget(self.pipeline_diagram)
        rl.addWidget(pipe_grp)

        # Tab panel: registers, memory, log
        tabs = QTabWidget()

        # Registers tab
        reg_tab = QWidget()
        rtl = QHBoxLayout(reg_tab)
        rtl.setContentsMargins(8, 8, 8, 8)
        rtl.setSpacing(8)
        self.reg_table = self._make_reg_table()
        rtl.addWidget(self.reg_table)
        tabs.addTab(reg_tab, "⬡  Registers")

        # Data memory tab
        mem_tab = QWidget()
        mtl = QVBoxLayout(mem_tab)
        mtl.setContentsMargins(8, 8, 8, 8)
        self.mem_table = self._make_mem_table()
        mtl.addWidget(self.mem_table)
        tabs.addTab(mem_tab, "🗄  Data Memory")

        # Instruction memory tab
        imem_tab = QWidget()
        itl = QVBoxLayout(imem_tab)
        itl.setContentsMargins(8, 8, 8, 8)
        self.imem_table = self._make_imem_table()
        itl.addWidget(self.imem_table)
        tabs.addTab(imem_tab, "💾  Instr Memory")

        # Cycle log tab
        log_tab = QWidget()
        ltl = QVBoxLayout(log_tab)
        ltl.setContentsMargins(8, 8, 8, 8)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("JetBrains Mono", 10))
        ltl.addWidget(self.log_text)
        tabs.addTab(log_tab, "📋  Cycle Log")

        rl.addWidget(tabs, 1)
        body.addWidget(right)
        body.setSizes([360, 1040])
        root.addWidget(body, 1)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready — load a program to begin.")

    def _make_reg_table(self):
        cols = 4
        rows = 16
        t = QTableWidget(rows, cols * 3)
        t.setAlternatingRowColors(True)
        hdrs = []
        for c in range(cols):
            hdrs += ["Reg", "Dec", "Hex"]
        t.setHorizontalHeaderLabels(hdrs)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QTableWidget.NoEditTriggers)
        t.setSelectionMode(QTableWidget.NoSelection)
        # populate reg names
        for r in range(rows):
            for c in range(cols):
                reg_idx = r + c * rows
                if reg_idx < 64:
                    item = QTableWidgetItem(f"R{reg_idx}")
                    item.setForeground(QColor(ACCENT_BLUE))
                    item.setFont(QFont("JetBrains Mono", 10, QFont.Bold))
                    t.setItem(r, c*3, item)
                    t.setItem(r, c*3+1, QTableWidgetItem("0"))
                    t.setItem(r, c*3+2, QTableWidgetItem("0x00"))
        return t

    def _make_mem_table(self):
        t = QTableWidget(50, 3)
        t.setHorizontalHeaderLabels(["Address", "Decimal", "Hex"])
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QTableWidget.NoEditTriggers)
        t.setAlternatingRowColors(True)
        for r in range(50):
            addr_item = QTableWidgetItem(str(r))
            addr_item.setForeground(QColor(ACCENT_GOLD))
            t.setItem(r, 0, addr_item)
            t.setItem(r, 1, QTableWidgetItem("0"))
            t.setItem(r, 2, QTableWidgetItem("0x00"))
        return t

    def _make_imem_table(self):
        t = QTableWidget(64, 4)
        t.setHorizontalHeaderLabels(["Address", "Hex", "Binary", "Mnemonic"])
        t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QTableWidget.NoEditTriggers)
        t.setAlternatingRowColors(True)
        return t

    # ── Actions ───────────────────────────────────────────────────────
    def _apply_default_program(self):
        self.program_editor.setPlainText(
            "MOVI R1 0\n"
            "BEQZ R1 2\n"
            "MOVI R2 5\n"
            "MOVI R3 7\n"
            "MOVI R4 9\n"
        )

    def _load_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Assembly File", "", "Text Files (*.txt *.asm);;All Files (*)")
        if path:
            with open(path) as f:
                self.program_editor.setPlainText(f.read())
            self.status.showMessage(f"Loaded: {path}")

    def _load_program(self):
        text = self.program_editor.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "No Program", "Please enter an assembly program.")
            return
        self.engine.load_program(text)
        self._refresh_imem_table()
        self._refresh_reg_table()
        self._refresh_mem_table()
        self.log_text.clear()
        self.lbl_cycle.setText("Cycle  0")
        self.pipeline_diagram.update_pipeline(None, None, None)
        self.sreg_widget.update_flags(self.engine.SREG)
        self.btn_step.setEnabled(True)
        self.btn_run.setEnabled(True)
        self.status.showMessage(
            f"Program loaded — {self.engine.instruction_count} instructions.")

    def _step(self):
        if self.engine.is_finished():
            self._finish()
            return
        log = self.engine.step()
        if log:
            self._apply_log(log)

    def _toggle_run(self):
        if self._auto_timer.isActive():
            self._auto_timer.stop()
            self.btn_run.setText("⏩  Run All")
        else:
            speed = self.speed_slider.value()
            interval = int(1100 - speed * 100)   # 100ms – 1000ms
            self._auto_timer.start(interval)
            self.btn_run.setText("⏸  Pause")

    def _auto_step(self):
        if self.engine.is_finished():
            self._auto_timer.stop()
            self.btn_run.setText("⏩  Run All")
            self._finish()
            return
        log = self.engine.step()
        if log:
            self._apply_log(log)

    def _reset(self):
        self._auto_timer.stop()
        self.btn_run.setText("⏩  Run All")
        text = self.program_editor.toPlainText().strip()
        self.engine.load_program(text)
        self._refresh_imem_table()
        self._refresh_reg_table()
        self._refresh_mem_table()
        self.log_text.clear()
        self.lbl_cycle.setText("Cycle  0")
        self.pipeline_diagram.update_pipeline(None, None, None)
        self.sreg_widget.update_flags(self.engine.SREG)
        self.btn_step.setEnabled(True)
        self.btn_run.setEnabled(True)
        self.status.showMessage("Reset — program reloaded.")

    def _finish(self):
        self.btn_step.setEnabled(False)
        self.btn_run.setEnabled(False)
        self.status.showMessage(
            f"✔  Simulation complete — {self.engine.cycle} cycles.")
        self._append_log(
            f"\n{'═'*60}\n  SIMULATION COMPLETE — {self.engine.cycle} CYCLES\n{'═'*60}\n",
            color=ACCENT_GREEN)

    # ── Log rendering ─────────────────────────────────────────────────
    def _apply_log(self, log: dict):
        cycle = log['cycle']
        self.lbl_cycle.setText(f"Cycle  {cycle}")

        # Pipeline diagram
        self.pipeline_diagram.update_pipeline(
            log.get("fetch"), log.get("decode"), log.get("execute"))

        # SREG
        self.sreg_widget.update_flags(log['sreg'])

        # Register table highlight
        for reg, old, new in log.get("reg_changes", []):
            self._highlight_reg(reg, new)

        # Memory table
        for addr, old, new in log.get("mem_changes", []):
            self._highlight_mem(addr, new)

        # Refresh tables
        self._refresh_reg_table()
        self._refresh_mem_table()

        # Log text
        self._write_cycle_log(log)

        # Status bar
        msgs = []
        ex = log.get("execute")
        if ex:
            msgs.append(f"EX: {ex['op_str']}")
        if log.get("flushed"):
            msgs.append("⚡ Pipeline flushed (branch/jump)")
        if log.get("forwarded"):
            msgs.append("↺ Data forwarded")
        self.status.showMessage(f"Cycle {cycle}  —  " + ("  |  ".join(msgs) if msgs else "idle"))

    def _write_cycle_log(self, log):
        c = log['cycle']
        self._append_log(f"\n{'─'*50}\n  CLOCK CYCLE {c}\n{'─'*50}", color=ACCENT_GOLD)

        # FETCH
        fetch = log.get("fetch")
        if fetch:
            if fetch.get("flushed"):
                self._append_log("  [IF] — FLUSHED (pipeline flush)", color=ACCENT_RED)
            elif fetch.get("pc") is not None:
                instr_hex = f"0x{self.engine.instruction_memory[fetch['pc']]:04X}"
                self._append_log(
                    f"  [IF] Fetched {instr_hex}  from PC={fetch['pc']}", color=STAGE_COLORS["IF"])
        else:
            self._append_log("  [IF] — empty", color=TEXT_MUTED)

        # DECODE
        decode = log.get("decode")
        if decode:
            opc_name = OPCODE_NAMES.get(decode['opcode'], "???")
            self._append_log(
                f"  [ID] Decoding {opc_name}  R1=R{decode['r1']}({decode['r1Value']})  "
                f"R2=R{decode['r2']}({decode['r2Value']})  IMM={decode['immediate']}",
                color=STAGE_COLORS["ID"])
            if decode.get("forwarded"):
                self._append_log("       ↺ Forwarded value applied", color=ACCENT_PURP)
        else:
            self._append_log("  [ID] — empty", color=TEXT_MUTED)

        # EXECUTE
        ex = log.get("execute")
        if ex:
            self._append_log(f"  [EX] {ex['op_str']}", color=STAGE_COLORS["EX"])
            sreg = log['sreg']
            flags = f"C={sreg['C']} V={sreg['V']} N={sreg['N']} S={sreg['S']} Z={sreg['Z']}"
            self._append_log(f"       SREG: {flags}", color=TEXT_MUTED)
            for reg, old, new in ex.get("reg_changes", []):
                self._append_log(f"       R{reg}: {old} → {new}", color=ACCENT_GREEN)
            for addr, old, new in ex.get("mem_changes", []):
                self._append_log(f"       MEM[{addr}]: {old} → {new}", color=ACCENT_GOLD)
        else:
            self._append_log("  [EX] — empty", color=TEXT_MUTED)

        # Auto-scroll log
        self.log_text.moveCursor(QTextCursor.End)

    def _append_log(self, text: str, color: str = TEXT_PRIMARY):
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        fmt = cursor.charFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText(text + "\n")

    # ── Table refreshes ───────────────────────────────────────────────
    def _refresh_reg_table(self):
        regs = self.engine.registers
        rows = 16
        cols = 4
        for c in range(cols):
            for r in range(rows):
                reg_idx = r + c * rows
                if reg_idx < 64:
                    val = regs[reg_idx]
                    signed = val if val < 128 else val - 256
                    item_d = QTableWidgetItem(str(signed))
                    item_h = QTableWidgetItem(f"0x{val:02X}")
                    if val != 0:
                        item_d.setForeground(QColor(ACCENT_GREEN))
                        item_h.setForeground(QColor(ACCENT_GREEN))
                    else:
                        item_d.setForeground(QColor(TEXT_MUTED))
                        item_h.setForeground(QColor(TEXT_MUTED))
                    self.reg_table.setItem(r, c*3+1, item_d)
                    self.reg_table.setItem(r, c*3+2, item_h)

    def _refresh_mem_table(self):
        for r in range(50):
            val = self.engine.data_memory[r]
            signed = val if val < 128 else val - 256
            item_d = QTableWidgetItem(str(signed))
            item_h = QTableWidgetItem(f"0x{val & 0xFF:02X}")
            if val != 0:
                item_d.setForeground(QColor(ACCENT_GOLD))
                item_h.setForeground(QColor(ACCENT_GOLD))
            else:
                item_d.setForeground(QColor(TEXT_MUTED))
                item_h.setForeground(QColor(TEXT_MUTED))
            self.mem_table.setItem(r, 1, item_d)
            self.mem_table.setItem(r, 2, item_h)

    def _refresh_imem_table(self):
        n = self.engine.instruction_count
        self.imem_table.setRowCount(n)
        for i in range(n):
            instr = self.engine.instruction_memory[i]
            opcode = (instr >> 12) & 0xF
            r1     = (instr >>  6) & 0x3F
            r2     =  instr        & 0x3F
            name   = OPCODE_NAMES.get(opcode, "???")
            binary = f"{instr:016b}"
            binary_fmt = f"{binary[:4]} {binary[4:10]} {binary[10:]}"

            addr_item = QTableWidgetItem(str(i))
            addr_item.setForeground(QColor(ACCENT_BLUE))
            hex_item  = QTableWidgetItem(f"0x{instr:04X}")
            hex_item.setForeground(QColor(ACCENT_GOLD))
            bin_item  = QTableWidgetItem(binary_fmt)
            bin_item.setForeground(QColor(TEXT_MUTED))
            mnem_item = QTableWidgetItem(f"{name} R{r1}, R{r2}/IMM")
            mnem_item.setForeground(QColor(ACCENT_GREEN))

            self.imem_table.setItem(i, 0, addr_item)
            self.imem_table.setItem(i, 1, hex_item)
            self.imem_table.setItem(i, 2, bin_item)
            self.imem_table.setItem(i, 3, mnem_item)

    def _highlight_reg(self, reg_idx, new_val):
        rows = 16; cols = 4
        c = reg_idx // rows
        r = reg_idx % rows
        if c < cols:
            item = self.reg_table.item(r, c*3+1)
            if item:
                item.setBackground(QColor(ACCENT_GREEN + "44"))

    def _highlight_mem(self, addr, new_val):
        if addr < 50:
            item = self.mem_table.item(addr, 1)
            if item:
                item.setBackground(QColor(ACCENT_GOLD + "44"))


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("CSEN601 Pipeline Simulator")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())