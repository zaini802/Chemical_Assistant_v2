# =============================================================================
# HEAT EXCHANGER DESIGNER — INDUSTRIAL GRADE
# pages/heat_exchanger.py
#
# Author   : Zunair Shahzad (2022-CH-246), Chemical Engineering, UET Lahore
# Version  : 3.0.0
# Standard : TEMA 9th Edition, ASME Sec VIII, API 661
#
# References (see full table at bottom of module):
#   Kern (1950) · TEMA (2007) · Kays & London (1984)
#   Bowman-Mueller-Nagle (1940) · Dittus-Boelter (1930)
#   Colburn (1933) · Darcy-Weisbach · Crane TP-410
#   API 661 · ALFA LAVAL Handbook · Coulson & Richardson Vol.6
# =============================================================================

import math
import io
import datetime
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image as RLImage
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas

# ─────────────────────────────────────────────────────────────────────────────
# 1.  CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Base ─────────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* ── Main header ─────────────────────────────────────────────────────────── */
.main-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1a237e 100%);
    padding: 28px 36px;
    border-radius: 16px;
    margin-bottom: 24px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(30,60,114,0.45);
    border: 1px solid rgba(255,255,255,0.12);
}
.main-header h1 {
    color: #ffffff;
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.main-header p {
    color: rgba(255,255,255,0.75);
    font-size: 0.95rem;
    margin: 0;
    font-weight: 300;
}

/* ── Section headers ──────────────────────────────────────────────────────── */
.section-header {
    background: linear-gradient(135deg, #0f3443 0%, #1a5a6e 100%);
    padding: 14px 22px;
    border-radius: 10px;
    margin: 20px 0 14px 0;
    border-left: 4px solid #34e89e;
}
.section-header h3 {
    color: #ffffff;
    margin: 0;
    font-size: 1.1rem;
    font-weight: 700;
}

/* ── Input heading label ─────────────────────────────────────────────────── */
.input-label {
    color: #ff6666;
    font-weight: 700;
    font-size: 0.85rem;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ── Result card ─────────────────────────────────────────────────────────── */
.result-card {
    background: #0f2027;
    border: 1px solid #34e89e;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 8px 0;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
}
.result-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 32px rgba(52,232,158,0.25);
}
.result-card .label {
    color: rgba(255,255,255,0.6);
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 6px;
}
.result-card .value {
    color: #34e89e;
    font-size: 2rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
.result-card .unit {
    color: rgba(255,255,255,0.45);
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 4px;
}

/* ── Warning / info boxes ────────────────────────────────────────────────── */
.warn-box {
    background: rgba(255,153,0,0.12);
    border-left: 4px solid #ff9900;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #ffc966;
    font-size: 0.9rem;
}
.info-box {
    background: rgba(52,232,158,0.08);
    border-left: 4px solid #34e89e;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #b0ffe0;
    font-size: 0.9rem;
}
.error-box {
    background: rgba(255,80,80,0.12);
    border-left: 4px solid #ff5050;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 10px 0;
    color: #ffaaaa;
    font-size: 0.9rem;
}

/* ── Recommendation card ─────────────────────────────────────────────────── */
.rec-card {
    background: linear-gradient(135deg, #0d1f2d 0%, #162435 100%);
    border: 1px solid #2196f3;
    border-radius: 14px;
    padding: 22px 26px;
    margin: 16px 0;
    box-shadow: 0 6px 24px rgba(33,150,243,0.2);
}
.rec-card h4 {
    color: #64b5f6;
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 10px 0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.rec-card .rec-type {
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 800;
    margin: 0 0 14px 0;
}
.rec-card ul {
    margin: 0;
    padding-left: 20px;
    color: rgba(255,255,255,0.75);
    font-size: 0.88rem;
    line-height: 1.8;
}

/* ── Step calculation box ────────────────────────────────────────────────── */
.calc-step {
    background: #0a1628;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #c8d8e8;
    line-height: 1.7;
}
.calc-step .step-title {
    color: #34e89e;
    font-weight: 700;
    font-size: 0.85rem;
    margin-bottom: 8px;
}
.calc-step .formula {
    color: #ffd700;
    font-size: 0.85rem;
}
.calc-step .result-line {
    color: #64ffda;
    font-weight: 600;
}

/* ── Tab styling ─────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #0a1628;
    border-radius: 10px 10px 0 0;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: rgba(255,255,255,0.55);
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1e3c72, #2a5298) !important;
    color: #ffffff !important;
}

/* ── Streamlit widget overrides ──────────────────────────────────────────── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background-color: #0f2027 !important;
    color: #ffffff !important;
    border: 1px solid #34e89e44 !important;
    border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important;
}

/* ── Download buttons ────────────────────────────────────────────────────── */
.btn-pdf   { background: linear-gradient(90deg,#c0392b,#e74c3c) !important; }
.btn-word  { background: linear-gradient(90deg,#1565c0,#1976d2) !important; }
.btn-txt   { background: linear-gradient(90deg,#1b5e20,#2e7d32) !important; }
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# 2.  FLUID PROPERTIES DATABASE
#     Simple polynomial/constant models at operating temperature.
#     Ref: Incropera & DeWitt, Perry's Chemical Engineers' Handbook
# ─────────────────────────────────────────────────────────────────────────────

def fluid_properties(fluid_type: str, T_avg_C: float) -> dict:
    """
    Return dict with keys: rho [kg/m3], Cp [J/kg·K], mu [Pa·s], k [W/m·K].
    Values are approximate and sufficient for preliminary design.
    """
    T = T_avg_C
    T_K = T + 273.15

    if fluid_type == "Water":
        # Valid ~10-100 °C
        rho = 1000.6 - 0.0128 * T**1.76
        Cp  = 4226 - 1.9 * T + 0.012 * T**2
        mu  = 2.414e-5 * 10**(247.8 / (T_K - 140))
        k   = 0.5618 + 0.00197 * T - 8.0e-6 * T**2

    elif fluid_type == "Steam":
        rho = max(0.6, 353.0 / T_K)
        Cp  = 1900 + 0.4 * T
        mu  = 8.0e-6 + 2.5e-8 * T
        k   = 0.0186 + 5.5e-5 * T

    elif fluid_type == "Air":
        rho = 353.0 / T_K
        Cp  = 1007 + 0.04 * T
        mu  = 1.716e-5 + 4.0e-8 * T
        k   = 0.02442 + 7.1e-5 * T

    elif fluid_type == "Oil (Mineral)":
        rho = 900 - 0.65 * T
        Cp  = 1750 + 4.0 * T
        mu  = 0.08 * math.exp(-0.022 * T)
        k   = 0.145 - 0.0001 * T

    elif fluid_type == "Organic Solvent":
        rho = 870 - 0.8 * T
        Cp  = 1600 + 2.5 * T
        mu  = 0.005 * math.exp(-0.015 * T)
        k   = 0.14 - 0.00015 * T

    elif fluid_type == "Brine (NaCl 20%)":
        rho = 1150 - 0.5 * T
        Cp  = 3500 - 1.5 * T
        mu  = 1.8e-3 * math.exp(-0.018 * T)
        k   = 0.51 + 0.001 * T

    elif fluid_type == "Gas (Generic)":
        rho = max(0.5, 29.0 / (8314 / 28.97) * 1e5 / T_K)
        Cp  = 1050 + 0.1 * T
        mu  = 1.8e-5 + 3.5e-8 * T
        k   = 0.025 + 6.0e-5 * T

    else:  # fallback = water
        rho = 1000.0; Cp = 4180.0; mu = 8.9e-4; k = 0.6

    # Clamp to physical bounds
    rho = max(0.1, rho)
    Cp  = max(500.0, Cp)
    mu  = max(1e-7, mu)
    k   = max(0.01, k)
    return {"rho": rho, "Cp": Cp, "mu": mu, "k": k}


# ─────────────────────────────────────────────────────────────────────────────
# 3.  ENGINEERING HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def lmtd_counter(T1, T2, t1, t2) -> float:
    """LMTD for pure counter-current flow. Kern (1950) Ch.3."""
    dT1 = T1 - t2
    dT2 = T2 - t1
    if abs(dT1 - dT2) < 1e-6:
        return dT1
    if dT1 <= 0 or dT2 <= 0:
        return abs(dT1 + dT2) / 2
    return (dT1 - dT2) / math.log(dT1 / dT2)


def f_correction_1shell_2pass(P: float, R: float) -> float:
    """
    F correction factor for 1-shell, 2-tube-pass (and even number of passes).
    Bowman, Mueller & Nagle (1940) analytical formula.
    Returns F (0 < F ≤ 1). Returns 0.75 minimum floor for safe design check.
    """
    if abs(R - 1.0) < 1e-4:
        # R ≈ 1 limiting case
        denom = (1.0 - P)
        if denom <= 0:
            return 0.75
        S = P * math.sqrt(2.0) / (2.0 - P * (1.0 + math.sqrt(2.0) - 1.0))
        return S / (S + 1.0) if S > 0 else 0.75
    try:
        S = math.sqrt(R**2 + 1.0) / (R - 1.0)
        num = math.log((1.0 - P) / (1.0 - P * R))
        arg = (2.0 / P - 1.0 - R + S) / (2.0 / P - 1.0 - R - S)
        if arg <= 0:
            return 0.75
        denom = S * math.log(arg)
        if abs(denom) < 1e-9:
            return 0.75
        return num / denom
    except Exception:
        return 0.75


def u_clean_estimate(hot_fluid: str, cold_fluid: str) -> float:
    """
    Estimate clean overall U from fluid pair table.
    Ref: Kern (1950) Table 8 and Coulson & Richardson Vol.6.
    Returns U_clean [W/m²·K].
    """
    matrix = {
        ("Water",        "Water"):           1200,
        ("Steam",        "Water"):           2000,
        ("Oil (Mineral)","Water"):           300,
        ("Air",          "Water"):           60,
        ("Air",          "Air"):             25,
        ("Steam",        "Oil (Mineral)"):   400,
        ("Water",        "Oil (Mineral)"):   300,
        ("Water",        "Brine (NaCl 20%)"): 900,
        ("Steam",        "Brine (NaCl 20%)"): 1500,
        ("Gas (Generic)","Gas (Generic)"):   30,
        ("Gas (Generic)","Water"):           150,
        ("Organic Solvent","Water"):         500,
        ("Organic Solvent","Brine (NaCl 20%)"): 450,
    }
    key = (hot_fluid, cold_fluid)
    if key in matrix:
        return matrix[key]
    key2 = (cold_fluid, hot_fluid)
    if key2 in matrix:
        return matrix[key2]
    # default
    if "Gas" in hot_fluid or "Air" in hot_fluid or "Gas" in cold_fluid or "Air" in cold_fluid:
        return 35
    return 500


def fouling_resistance(fluid: str) -> float:
    """
    Fouling resistance R_f [m²·K/W].
    Ref: TEMA Standards Table RGP-T-2.1
    """
    table = {
        "Water":             0.0002,
        "Steam":             0.0001,
        "Oil (Mineral)":     0.0004,
        "Air":               0.0002,
        "Gas (Generic)":     0.0002,
        "Organic Solvent":   0.0002,
        "Brine (NaCl 20%)":  0.0003,
        "Cooling Tower Water":0.0004,
        "Sea Water":         0.0002,
    }
    return table.get(fluid, 0.0002)


def tube_count_from_area(A_req: float, OD_m: float, L: float) -> int:
    """Calculate minimum number of tubes required."""
    A_per_tube = math.pi * OD_m * L
    return max(1, math.ceil(A_req / A_per_tube))


def shell_diameter(N_tubes: int, OD_m: float, pitch_m: float, layout: str) -> float:
    """
    Estimate shell ID from tube bundle geometry.
    Ref: TEMA Standards Appendix; Frank (1978)
    layout: 'Triangular (30°)' → CTP=0.866 | 'Square (90°)' → CTP=1.0
    """
    if "Square" in layout:
        k1 = 0.215; n1 = 2.207   # TEMA bundle constants for square
    else:
        k1 = 0.319; n1 = 2.142   # triangular

    # Ds = OD * (N_tubes / k1)^(1/n1)
    Ds = OD_m * (N_tubes / k1) ** (1.0 / n1)
    return Ds


def dittus_boelter(Re: float, Pr: float, heating: bool = True) -> float:
    """
    Nusselt number by Dittus-Boelter (1930).
    Nu = 0.023 · Re^0.8 · Pr^n  (n=0.4 heating, 0.3 cooling)
    Valid: Re > 4000, 0.7 < Pr < 160, L/D > 10.
    """
    n = 0.4 if heating else 0.3
    return 0.023 * Re**0.8 * Pr**n


def kern_shell_ht(Re_s: float, Pr_s: float) -> float:
    """
    Shell-side j_H factor — Kern (1950) / Colburn (1933).
    Nu_s = j_H · Re_s · Pr_s^(1/3)
    j_H = 0.36 · Re_s^(-0.36)   for Re_s in 2000–1,000,000
    """
    j_H = 0.36 * Re_s**(-0.36)
    return j_H   # caller multiplies by Re·Pr^(1/3)·k/De


def darcy_friction(Re: float, eps_D: float = 0.00015 / 0.019) -> float:
    """
    Darcy-Weisbach friction factor.
    Laminar  : f = 64/Re
    Turbulent: Churchill (1977) composite (smooth/rough)
    eps_D default: commercial steel 0.046mm / 19mm tube
    """
    if Re < 2300:
        return 64.0 / Re
    # Colebrook-White approximation (Swamee & Jain, 1976)
    if Re < 1e4:
        f = 0.046 * Re**(-0.2)  # Petukhov approximation
        return max(f, 0.01)
    try:
        f = (-1.8 * math.log10((eps_D / 3.7)**1.11 + 6.9 / Re))**(-2)
    except Exception:
        f = 0.02
    return max(0.008, f)


def effectiveness_counterflow(NTU: float, Cr: float) -> float:
    """
    ε-NTU for counter-current flow. Kays & London (1984).
    """
    if Cr >= 1.0:
        return NTU / (1.0 + NTU)
    exp = math.exp(-NTU * (1.0 - Cr))
    return (1.0 - exp) / (1.0 - Cr * exp)


def equipment_cost_guthrie(A_m2: float, material: str = "Carbon Steel") -> float:
    """
    Guthrie (1969) cost correlation for shell & tube HX.
    C = a + b * A^c   [USD, 2023 CEPCI adjusted ~700]
    Ref: Coulson & Richardson Vol.6 Chapter 6
    """
    mat_factor = {"Carbon Steel": 1.0, "Stainless Steel 304": 2.0,
                  "Stainless Steel 316": 2.5}.get(material, 1.0)
    a, b, c = 5000, 200, 0.80
    base = a + b * A_m2**c
    return base * mat_factor


# ─────────────────────────────────────────────────────────────────────────────
# 4.  SMART RECOMMENDATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def recommend_hx_type(Q_kW, P_bar, T1, fouling_hot, fouling_cold,
                      hot_fluid, cold_fluid) -> dict:
    """
    Rule-based recommendation.  Returns dict with type, reasons, ref.
    """
    reasons = []
    ref = []

    if P_bar > 20:
        hx = "Shell & Tube"
        reasons.append("✅ High pressure (>20 bar) requires robust TEMA-standard design")
        reasons.append("✅ Shell & tube handles pressures up to 300 bar")
        reasons.append("✅ ASME Sec VIII compliance for pressure vessels")
        ref = ["TEMA 9th Ed.", "ASME Sec VIII"]

    elif Q_kW < 100:
        hx = "Double Pipe"
        reasons.append("✅ Small duty (<100 kW) → double pipe is most cost-effective")
        reasons.append("✅ Simple construction, easy cleaning")
        reasons.append("✅ No shell required — minimal capital cost")
        ref = ["Kern (1950) Ch.6"]

    elif "Slurr" in hot_fluid or "Slurr" in cold_fluid:
        hx = "Spiral"
        reasons.append("✅ Spiral provides single-channel flow path, no dead zones")
        reasons.append("✅ Self-cleaning action for fouling/slurry service")
        reasons.append("✅ Low pressure drop for viscous fluids")
        ref = ["ALFA LAVAL Spiral Handbook", "Rosenblad (1970)"]

    elif "Air" in cold_fluid or "Air" in hot_fluid:
        hx = "Air Cooled (Fin Fan)"
        reasons.append("✅ Air cooling eliminates cooling water cost")
        reasons.append("✅ Finned tubes maximise air-side surface area")
        reasons.append("✅ API 661 compliant design standard")
        ref = ["API 661", "Kern (1950) Ch.15"]

    elif fouling_hot > 0.0003 or fouling_cold > 0.0003:
        hx = "Shell & Tube"
        reasons.append("✅ Fouling service → removable bundle for mechanical cleaning")
        reasons.append("✅ TEMA type AEL or CFU for easy access")
        reasons.append("✅ Tube-side cleaning without shutdown")
        ref = ["TEMA 9th Ed. RGP-T-2.1"]

    elif T1 > 300:
        hx = "Shell & Tube"
        reasons.append("✅ High temperature (>300°C) requires shell & tube")
        reasons.append("✅ Material flexibility (alloy steels, Inconel)")
        reasons.append("✅ Thermal expansion managed by floating head or U-tube")
        ref = ["TEMA 9th Ed.", "API 661"]

    elif 100 <= Q_kW <= 500:
        hx = "Plate & Frame"
        reasons.append("✅ Compact design for moderate duty (100–500 kW)")
        reasons.append("✅ U values 3–5× higher than shell & tube")
        reasons.append("✅ Easy to clean and expand capacity by adding plates")
        ref = ["ALFA LAVAL Handbook", "Cooper (1974)"]

    else:
        hx = "Shell & Tube"
        reasons.append("✅ Shell & tube is the industry workhorse for this duty range")
        reasons.append("✅ Wide temperature and pressure capability")
        reasons.append("✅ Extensive industrial track record and TEMA standards")
        ref = ["Kern (1950)", "TEMA 9th Ed."]

    return {"type": hx, "reasons": reasons, "references": ref}


# ─────────────────────────────────────────────────────────────────────────────
# 5.  SHELL & TUBE FULL DESIGN (33 STEPS)
# ─────────────────────────────────────────────────────────────────────────────

def design_shell_tube(inp: dict) -> dict:
    """
    Complete shell-and-tube HX design following Kern (1950) 28-step method.
    inp keys: T1, T2, t1, t2, mdot_h, mdot_c, hot_fluid, cold_fluid,
              P_bar, OD_mm, length_m, layout, n_passes, baffle_cut_frac,
              shell_type, tema_type, fouling_h, fouling_c, tube_material,
              wall_k, eps_D
    Returns dict with all results + step_log list for display.
    """
    r = {}          # results
    steps = []      # step log [{title, formula, value, unit}]

    def log(title, formula, val, unit=""):
        steps.append({"title": title, "formula": formula,
                       "value": val, "unit": unit})

    T1 = inp["T1"]; T2 = inp["T2"]
    t1 = inp["t1"]; t2 = inp["t2"]
    mdot_h = inp["mdot_h"]
    hot_f  = inp["hot_fluid"]
    cold_f = inp["cold_fluid"]

    T_avg_h = (T1 + T2) / 2.0
    T_avg_c = (t1 + t2) / 2.0

    ph = fluid_properties(hot_f,  T_avg_h)
    pc = fluid_properties(cold_f, T_avg_c)

    # ── STEP 1: Heat duty ────────────────────────────────────────────────────
    Q = mdot_h * ph["Cp"] * (T1 - T2)
    r["Q_W"] = Q;  r["Q_kW"] = Q / 1000.0
    log("STEP 1 — Heat Duty",
        "Q = ṁ_h × Cp_h × (T₁−T₂)",
        f"Q = {mdot_h:.3f} × {ph['Cp']:.1f} × ({T1}−{T2}) = {Q/1000:.2f} kW",
        "kW")

    # ── STEP 2: Cold side flow rate ──────────────────────────────────────────
    if inp.get("mdot_c_given"):
        mdot_c = inp["mdot_c"]
        log("STEP 2 — Cold Flow Rate", "User-supplied", f"ṁ_c = {mdot_c:.3f} kg/s", "kg/s")
    else:
        mdot_c = Q / (pc["Cp"] * (t2 - t1))
        log("STEP 2 — Cold Flow Rate",
            "ṁ_c = Q / (Cp_c × (t₂−t₁))",
            f"ṁ_c = {Q:.1f} / ({pc['Cp']:.1f} × ({t2}−{t1})) = {mdot_c:.3f} kg/s", "kg/s")
    r["mdot_c"] = mdot_c

    # ── STEP 3: Counter-current LMTD ────────────────────────────────────────
    LMTD_cc = lmtd_counter(T1, T2, t1, t2)
    dT1 = T1 - t2;  dT2 = T2 - t1
    r["LMTD_cc"] = LMTD_cc
    log("STEP 3 — Counter-current LMTD",
        "LMTD = (ΔT₁−ΔT₂)/ln(ΔT₁/ΔT₂)",
        f"ΔT₁={dT1:.2f}°C  ΔT₂={dT2:.2f}°C  LMTD={LMTD_cc:.2f}°C", "°C")

    # ── STEP 4: P and R ──────────────────────────────────────────────────────
    P_val = (t2 - t1) / max(1e-6, (T1 - t1))
    R_val = (T1 - T2) / max(1e-6, (t2 - t1))
    r["P_val"] = P_val;  r["R_val"] = R_val
    log("STEP 4 — P and R (Bowman 1940)",
        "P=(t₂−t₁)/(T₁−t₁)   R=(T₁−T₂)/(t₂−t₁)",
        f"P = {P_val:.3f}   R = {R_val:.3f}", "—")

    # ── STEP 5: F-correction factor ──────────────────────────────────────────
    n_passes = inp.get("n_passes", 2)
    F = f_correction_1shell_2pass(P_val, R_val)
    F = min(F, 1.0);  F = max(F, 0.50)
    r["F"] = F
    warn_F = F < 0.75
    log("STEP 5 — F-Correction Factor",
        "Bowman-Mueller-Nagle (1940) analytical",
        f"F = {F:.4f}  {'⚠ F < 0.75 — consider multiple shells' if warn_F else '✓ Acceptable'}", "—")

    # ── STEP 6: Corrected LMTD ──────────────────────────────────────────────
    LMTD_cf = LMTD_cc * F
    r["LMTD_cf"] = LMTD_cf
    log("STEP 6 — Corrected LMTD",
        "LMTD_cf = LMTD × F",
        f"LMTD_cf = {LMTD_cc:.2f} × {F:.4f} = {LMTD_cf:.2f}°C", "°C")

    # ── STEP 7: Estimate U_clean ─────────────────────────────────────────────
    U_clean = u_clean_estimate(hot_f, cold_f)
    r["U_clean"] = U_clean
    log("STEP 7 — U_clean Estimate",
        "From fluid-pair database  [Kern (1950) Table 8]",
        f"U_clean = {U_clean:.0f} W/m²·K", "W/m²·K")

    # ── STEP 8: Fouling resistances ──────────────────────────────────────────
    Rfh = inp.get("fouling_h", fouling_resistance(hot_f))
    Rfc = inp.get("fouling_c", fouling_resistance(cold_f))
    r["Rfh"] = Rfh;  r["Rfc"] = Rfc
    log("STEP 8 — Fouling Resistances",
        "TEMA Table RGP-T-2.1",
        f"R_fh = {Rfh:.5f}  R_fc = {Rfc:.5f} m²·K/W", "m²·K/W")

    # ── STEP 9: U_dirty ──────────────────────────────────────────────────────
    U_dirty = 1.0 / (1.0 / U_clean + Rfh + Rfc)
    r["U_dirty"] = U_dirty
    log("STEP 9 — U_dirty",
        "1/U_dirty = 1/U_clean + R_fh + R_fc",
        f"U_dirty = {U_dirty:.1f} W/m²·K", "W/m²·K")

    # ── STEP 10: Required area ───────────────────────────────────────────────
    A_req = Q / max(1e-3, U_dirty * LMTD_cf)
    r["A_req"] = A_req
    log("STEP 10 — Required Heat Transfer Area",
        "A = Q / (U_dirty × LMTD_cf)",
        f"A = {Q:.1f} / ({U_dirty:.1f} × {LMTD_cf:.2f}) = {A_req:.2f} m²", "m²")

    # ── STEP 11: Tube geometry ───────────────────────────────────────────────
    OD_mm   = inp.get("OD_mm", 19.05)
    OD_m    = OD_mm / 1000.0
    BWG_wall= {15.875: 2.11, 19.05: 2.11, 25.4: 2.77, 31.75: 2.77}.get(OD_mm, 2.11)
    ID_m    = (OD_mm - 2 * BWG_wall) / 1000.0
    L_m     = inp.get("length_m", 3.66)
    layout  = inp.get("layout", "Triangular (30°)")
    pitch_m = 1.25 * OD_m
    wall_k  = inp.get("wall_k", 50.0)   # Carbon steel
    r.update({"OD_m": OD_m, "ID_m": ID_m, "L_m": L_m,
               "pitch_m": pitch_m, "BWG_wall": BWG_wall})
    log("STEP 11 — Tube Geometry",
        "OD, ID (BWG14), pitch = 1.25×OD",
        f"OD={OD_mm}mm  ID={ID_m*1000:.2f}mm  L={L_m}m  Pitch={pitch_m*1000:.2f}mm  Layout:{layout}",
        "mm/m")

    # ── STEP 12 & 13: Tube count ─────────────────────────────────────────────
    A_per_tube = math.pi * OD_m * L_m
    N_tubes    = tube_count_from_area(A_req, OD_m, L_m)
    r["A_per_tube"] = A_per_tube;  r["N_tubes"] = N_tubes
    log("STEP 12 — Area per Tube",
        "A_tube = π × OD × L",
        f"A_tube = π × {OD_m:.5f} × {L_m} = {A_per_tube:.4f} m²", "m²")
    log("STEP 13 — Number of Tubes",
        "N = ceil(A_req / A_tube)",
        f"N_tubes = ⌈{A_req:.2f}/{A_per_tube:.4f}⌉ = {N_tubes}", "—")

    # ── STEP 14: Shell diameter ──────────────────────────────────────────────
    Ds_m = shell_diameter(N_tubes, OD_m, pitch_m, layout)
    r["Ds_m"] = Ds_m
    log("STEP 14 — Shell Inside Diameter",
        "Ds = OD × (N_tubes/k₁)^(1/n₁)  [TEMA bundle constants]",
        f"D_shell = {Ds_m*1000:.1f} mm = {Ds_m:.4f} m", "m")

    # ── STEP 15: Tubes per pass ──────────────────────────────────────────────
    n_passes = max(1, inp.get("n_passes", 2))
    N_per_pass = max(1, math.ceil(N_tubes / n_passes))
    r["N_per_pass"] = N_per_pass
    log("STEP 15 — Tubes per Pass",
        "N_per_pass = N_tubes / N_passes",
        f"{N_tubes} / {n_passes} = {N_per_pass} tubes/pass", "—")

    # ── STEP 16 & 17: Tube side flow area & velocity ─────────────────────────
    A_flow_tube = N_per_pass * math.pi * ID_m**2 / 4.0
    v_tube      = mdot_c / max(1e-9, pc["rho"] * A_flow_tube)
    r["A_flow_tube"] = A_flow_tube;  r["v_tube"] = v_tube
    log("STEP 16 — Tube-Side Flow Area",
        "A_flow = N_per_pass × π×ID²/4",
        f"A_flow = {A_flow_tube:.6f} m²", "m²")
    log("STEP 17 — Tube-Side Velocity",
        "v = ṁ_c / (ρ_c × A_flow)",
        f"v = {v_tube:.3f} m/s  {'✓ 1-3 m/s recommended' if 1<=v_tube<=3 else '⚠ Outside 1-3 m/s range'}",
        "m/s")

    # ── STEP 18-19: Re & Pr tube ─────────────────────────────────────────────
    Re_tube = pc["rho"] * v_tube * ID_m / max(1e-12, pc["mu"])
    Pr_tube = pc["Cp"] * pc["mu"] / max(1e-12, pc["k"])
    r["Re_tube"] = Re_tube;  r["Pr_tube"] = Pr_tube
    log("STEP 18 — Tube-Side Reynolds Number",
        "Re = ρ×v×ID/μ",
        f"Re_tube = {Re_tube:.0f}  → {'Turbulent ✓' if Re_tube > 4000 else ('Transitional ⚠' if Re_tube > 2300 else 'Laminar ⚠')}",
        "—")
    log("STEP 19 — Tube-Side Prandtl Number",
        "Pr = Cp×μ/k",
        f"Pr_tube = {Pr_tube:.2f}", "—")

    # ── STEP 20: Tube-side h_i ───────────────────────────────────────────────
    if Re_tube > 4000:
        Nu_tube = dittus_boelter(Re_tube, Pr_tube, heating=False)
        h_i = Nu_tube * pc["k"] / ID_m
        note = "Dittus-Boelter (1930)"
    elif Re_tube > 2300:
        # transitional — use Gnielinski (1976) approximation
        f_t  = darcy_friction(Re_tube)
        Nu_tube = ((f_t / 8) * (Re_tube - 1000) * Pr_tube /
                   (1 + 12.7 * (f_t / 8)**0.5 * (Pr_tube**(2/3) - 1)))
        h_i  = Nu_tube * pc["k"] / ID_m
        note = "Gnielinski (1976)"
    else:
        Nu_tube = 3.66   # laminar, uniform wall temp
        h_i     = Nu_tube * pc["k"] / ID_m
        note = "Laminar, Nu=3.66"
    r["h_i"] = h_i;  r["Nu_tube"] = Nu_tube
    log("STEP 20 — Tube-Side HTC (h_i)",
        f"Nu={note}: h_i = Nu×k/ID",
        f"Nu={Nu_tube:.1f}  h_i = {h_i:.1f} W/m²·K", "W/m²·K")

    # ── STEP 21: Shell-side equivalent diameter D_e ───────────────────────────
    if "Square" in layout:
        De_m = (4 * (pitch_m**2 - math.pi * OD_m**2 / 4)) / (math.pi * OD_m)
    else:   # triangular
        De_m = (4 * (pitch_m**2 * math.sqrt(3) / 4 - math.pi * OD_m**2 / 8)) / \
               (math.pi * OD_m / 2)
    r["De_m"] = De_m
    log("STEP 21 — Shell-Side Equivalent Diameter",
        "D_e = 4×(flow area)/(wetted perimeter)  [Kern 1950]",
        f"D_e = {De_m*1000:.2f} mm", "mm")

    # ── STEP 22: Shell-side flow area (baffle window) ─────────────────────────
    baffle_cut  = inp.get("baffle_cut_frac", 0.25)
    Bs          = 0.5 * Ds_m   # default baffle spacing = 0.5 × Ds
    A_flow_shell= Ds_m * Bs * (pitch_m - OD_m) / pitch_m
    r["A_flow_shell"] = A_flow_shell;  r["Bs"] = Bs
    log("STEP 22 — Shell-Side Flow Area",
        "A_s = Ds×Bs×(pitch−OD)/pitch",
        f"Bs={Bs*1000:.1f}mm  A_s={A_flow_shell:.6f} m²", "m²")

    # ── STEP 23 & 24 & 25: Shell mass vel, Re, Pr ─────────────────────────────
    G_s      = mdot_h / max(1e-12, A_flow_shell)
    v_shell  = G_s / max(1e-9, ph["rho"])
    Re_shell = De_m * G_s / max(1e-12, ph["mu"])
    Pr_shell = ph["Cp"] * ph["mu"] / max(1e-12, ph["k"])
    r.update({"G_s": G_s, "v_shell": v_shell,
               "Re_shell": Re_shell, "Pr_shell": Pr_shell})
    log("STEP 23 — Shell-Side Mass Velocity",
        "G_s = ṁ_h / A_s",
        f"G_s = {G_s:.2f} kg/m²·s", "kg/m²·s")
    log("STEP 24 — Shell-Side Reynolds Number",
        "Re_s = D_e × G_s / μ_h",
        f"Re_shell = {Re_shell:.0f}  → {'Turbulent ✓' if Re_shell > 2000 else 'Laminar/Trans'}",
        "—")
    log("STEP 25 — Shell-Side Prandtl Number",
        "Pr_s = Cp_h×μ_h/k_h",
        f"Pr_shell = {Pr_shell:.2f}", "—")

    # ── STEP 26: Shell-side h_o (Kern / Colburn j_H) ─────────────────────────
    j_H  = kern_shell_ht(max(10, Re_shell), Pr_shell)
    Nu_s = j_H * Re_shell * Pr_shell**(1/3)
    h_o  = Nu_s * ph["k"] / De_m
    r["j_H"] = j_H;  r["h_o"] = h_o;  r["Nu_shell"] = Nu_s
    log("STEP 26 — Shell-Side HTC (h_o)",
        "j_H=0.36×Re_s^(−0.36)  →  Nu_s=j_H×Re_s×Pr_s^(1/3)  →  h_o=Nu_s×k_h/D_e",
        f"j_H={j_H:.5f}  Nu={Nu_s:.1f}  h_o={h_o:.1f} W/m²·K", "W/m²·K")

    # ── STEP 27: U_calculated + iteration check ────────────────────────────────
    wall_resist = (OD_m * math.log(OD_m / max(1e-9, ID_m))) / (2 * wall_k)
    inv_U_calc  = (1 / max(1, h_i) + 1 / max(1, h_o) +
                   Rfh + Rfc + wall_resist)
    U_calc      = 1.0 / inv_U_calc
    r["U_calc"] = U_calc
    iter_err    = abs(U_calc - U_dirty) / max(1, U_dirty) * 100
    r["iter_err"] = iter_err
    log("STEP 27 — Overall U (Calculated)",
        "1/U_calc = 1/h_i + 1/h_o + R_fh + R_fc + wall_resist",
        f"U_calc = {U_calc:.1f} W/m²·K  (U_dirty={U_dirty:.1f})  "
        f"Δ={iter_err:.1f}%  {'✓ Converged' if iter_err < 5 else '⚠ Iterate'}",
        "W/m²·K")

    # ── STEP 28: Tube-side pressure drop ──────────────────────────────────────
    f_tube   = darcy_friction(Re_tube, eps_D=inp.get("eps_D", 0.046 / ID_m / 1000))
    dP_tube  = (f_tube * L_m / ID_m * ph.get("rho",1) * v_tube**2 / 2 * n_passes
                + 4 * pc["rho"] * v_tube**2 / 2 * n_passes)   # + return loss
    # Use cold fluid for tube side
    dP_tube  = (f_tube * (L_m / ID_m) * pc["rho"] * v_tube**2 / 2 * n_passes
                + 4 * pc["rho"] * v_tube**2 / 2 * n_passes)
    r["dP_tube_Pa"] = dP_tube
    log("STEP 28 — Tube-Side Pressure Drop (Darcy-Weisbach)",
        "ΔP = f×(L/D)×(ρv²/2)×N_passes  +  return losses",
        f"f={f_tube:.4f}  ΔP_tube = {dP_tube/1000:.2f} kPa", "kPa")

    # ── STEP 29: Shell-side pressure drop (Kern method) ───────────────────────
    N_baffles  = max(0, math.floor(L_m / Bs) - 1)
    f_shell    = max(0.001, 0.5 * Re_shell**(-0.2))
    dP_shell   = (f_shell * Ds_m / De_m * ph["rho"] * v_shell**2 / 2
                  * (N_baffles + 1))
    r["N_baffles"] = N_baffles
    r["dP_shell_Pa"] = dP_shell
    log("STEP 29 — Shell-Side Pressure Drop (Kern 1950)",
        "ΔP_s = f_s×(Ds/De)×(ρ_h×v_s²/2)×(N_b+1)",
        f"N_baffles={N_baffles}  f_s={f_shell:.4f}  ΔP_shell={dP_shell/1000:.2f} kPa",
        "kPa")

    # ── STEP 30: Pump power ───────────────────────────────────────────────────
    eta = 0.70   # 70% pump efficiency
    P_tube_W  = dP_tube  * mdot_c / max(0.1, pc["rho"]) / eta
    P_shell_W = dP_shell * mdot_h / max(0.1, ph["rho"]) / eta
    r["P_tube_kW"]  = P_tube_W  / 1000
    r["P_shell_kW"] = P_shell_W / 1000
    log("STEP 30 — Pump Power",
        "Power = ΔP × ṁ / (ρ × η)   η=70%",
        f"Tube-side: {P_tube_W/1000:.3f} kW   Shell-side: {P_shell_W/1000:.3f} kW",
        "kW")

    # ── STEP 31: NTU ─────────────────────────────────────────────────────────
    C_h   = mdot_h * ph["Cp"]
    C_c   = mdot_c * pc["Cp"]
    C_min = min(C_h, C_c)
    C_max = max(C_h, C_c)
    Cr    = C_min / max(1e-6, C_max)
    A_actual = N_tubes * math.pi * OD_m * L_m
    NTU   = U_calc * A_actual / max(1, C_min)
    r.update({"C_h": C_h, "C_c": C_c, "C_min": C_min,
               "C_max": C_max, "Cr": Cr, "NTU": NTU,
               "A_actual": A_actual})
    log("STEP 31 — NTU (Number of Transfer Units)",
        "NTU = U_calc × A_actual / C_min  [Kays & London 1984]",
        f"C_h={C_h:.1f}  C_c={C_c:.1f}  C_r={Cr:.3f}  NTU={NTU:.3f}", "—")

    # ── STEP 32: Effectiveness ────────────────────────────────────────────────
    eps = effectiveness_counterflow(NTU, Cr)
    r["eps"] = eps
    log("STEP 32 — Effectiveness (ε-NTU)",
        "ε = (1−e^(−NTU(1−Cr))) / (1−Cr·e^(−NTU(1−Cr)))",
        f"ε = {eps:.4f} = {eps*100:.1f}%", "%")

    # ── STEP 33: Cost estimate (Guthrie) ──────────────────────────────────────
    mat = inp.get("tube_material", "Carbon Steel")
    C_equip    = equipment_cost_guthrie(A_actual, mat)
    C_install  = C_equip * 2.0
    r["C_equip"]   = C_equip
    r["C_install"] = C_install
    log("STEP 33 — Equipment Cost (Guthrie 1969)",
        "C = (a + b×A^c) × mat_factor   installed = 2× equipment",
        f"Equipment: ${C_equip:,.0f}   Installed: ${C_install:,.0f}", "USD")

    # Wall temperature (average)
    R_tube_wall = 1 / max(1, h_i)
    T_wall = (T_avg_h + T_avg_c) / 2
    r["T_wall"] = T_wall

    # Oversurface
    r["oversurface_pct"] = (A_actual - A_req) / max(1e-6, A_req) * 100
    r["steps"] = steps
    r["warn_F"] = warn_F
    r["ph"]     = ph
    r["pc"]     = pc
    r["mdot_h"] = mdot_h
    return r


# ─────────────────────────────────────────────────────────────────────────────
# 6.  PLATE & FRAME DESIGN
# ─────────────────────────────────────────────────────────────────────────────

def design_plate_frame(inp: dict) -> dict:
    """
    Plate & Frame HX design.
    Ref: ALFA LAVAL Handbook; Cooper (1974); Martin (1996).
    """
    r = {}; steps = []
    def log(t, f, v, u=""): steps.append({"title":t,"formula":f,"value":v,"unit":u})

    T1=inp["T1"]; T2=inp["T2"]; t1=inp["t1"]; t2=inp["t2"]
    mdot_h=inp["mdot_h"]
    T_avg_h=(T1+T2)/2; T_avg_c=(t1+t2)/2
    ph=fluid_properties(inp["hot_fluid"], T_avg_h)
    pc=fluid_properties(inp["cold_fluid"],T_avg_c)

    Q = mdot_h * ph["Cp"] * (T1 - T2)
    mdot_c = Q / max(1, pc["Cp"] * (t2 - t1))
    r["Q_kW"] = Q/1000; r["mdot_c"] = mdot_c

    LMTD_cc = lmtd_counter(T1, T2, t1, t2)
    U_plate  = 2500   # W/m²·K typical PHE (clean)
    Rfh = inp.get("fouling_h", 0.0002); Rfc = inp.get("fouling_c", 0.0002)
    U_dirty  = 1 / (1/U_plate + Rfh + Rfc)
    F = 0.98   # PHE near pure counter-current
    LMTD_cf  = LMTD_cc * F
    A_req    = Q / max(1e-3, U_dirty * LMTD_cf)

    plate_area = inp.get("plate_area", 0.5)   # m² per plate (standard PHE)
    N_plates   = max(4, math.ceil(A_req / plate_area) + 2)   # +2 end plates
    N_channels = N_plates - 1
    D_h = inp.get("gap_mm", 3.0) / 1000 * 2   # hydraulic dia = 2×gap

    # Channel velocity (one fluid uses ~half channels)
    A_ch = inp.get("gap_mm", 3.0) / 1000 * inp.get("plate_width_m", 0.4)
    N_ch_per_fluid = N_channels // 2
    v_ch = mdot_h / max(1e-9, ph["rho"] * A_ch * max(1, N_ch_per_fluid))

    Re_ch = ph["rho"] * v_ch * D_h / max(1e-12, ph["mu"])
    Pr_ch = ph["Cp"] * ph["mu"] / max(1e-12, ph["k"])
    Nu_ch = 0.2 * Re_ch**0.7 * Pr_ch**0.33
    h_ch  = Nu_ch * ph["k"] / max(1e-6, D_h)

    dP_plate = 1.5 * ph["rho"] * v_ch**2 / 2 * N_channels   # PHE pressure drop

    r.update({"A_req": A_req, "N_plates": N_plates, "N_channels": N_channels,
               "U_dirty": U_dirty, "LMTD_cf": LMTD_cf, "F": F,
               "Re_ch": Re_ch, "h_ch": h_ch, "dP_plate_Pa": dP_plate,
               "steps": steps, "Q_W": Q})
    log("PHE — Heat Duty", "Q=ṁ_h×Cp_h×ΔT_h", f"Q={Q/1000:.2f} kW", "kW")
    log("PHE — LMTD", "Counter-current", f"LMTD={LMTD_cc:.2f}°C  F={F}", "°C")
    log("PHE — U_dirty", "1/U=1/U_clean+Rf", f"U_dirty={U_dirty:.1f} W/m²·K", "W/m²·K")
    log("PHE — Area & Plates", "N=ceil(A/A_plate)+2", f"A={A_req:.2f} m²  N_plates={N_plates}", "—")
    log("PHE — Channel Re & h", "Nu=0.2×Re^0.7×Pr^0.33", f"Re={Re_ch:.0f}  h={h_ch:.1f} W/m²·K","W/m²·K")
    log("PHE — Pressure Drop", "ΔP=1.5×(ρv²/2)×N_ch", f"ΔP={dP_plate/1000:.2f} kPa","kPa")
    return r


# ─────────────────────────────────────────────────────────────────────────────
# 7.  DOUBLE PIPE DESIGN
# ─────────────────────────────────────────────────────────────────────────────

def design_double_pipe(inp: dict) -> dict:
    """
    Double-pipe (hairpin) HX design.
    Ref: Kern (1950) Chapter 6.
    """
    r = {}; steps = []
    def log(t, f, v, u=""): steps.append({"title":t,"formula":f,"value":v,"unit":u})

    T1=inp["T1"]; T2=inp["T2"]; t1=inp["t1"]; t2=inp["t2"]
    mdot_h=inp["mdot_h"]
    T_avg_h=(T1+T2)/2; T_avg_c=(t1+t2)/2
    ph=fluid_properties(inp["hot_fluid"],T_avg_h)
    pc=fluid_properties(inp["cold_fluid"],T_avg_c)

    Q = mdot_h * ph["Cp"] * (T1 - T2)
    mdot_c = Q / max(1, pc["Cp"] * (t2 - t1))
    r["Q_kW"] = Q/1000; r["mdot_c"] = mdot_c

    LMTD_cc = lmtd_counter(T1, T2, t1, t2)
    U_est   = 400     # W/m²·K typical double pipe
    Rfh = inp.get("fouling_h", 0.0002); Rfc = inp.get("fouling_c", 0.0002)
    U_dirty  = 1/(1/U_est + Rfh + Rfc)
    A_req    = Q / max(1e-3, U_dirty * LMTD_cc)

    # Inner pipe (tube side — cold fluid)
    inner_OD_in = inp.get("inner_pipe_in", 1.5)   # inches
    inner_OD_m  = inner_OD_in * 0.0254
    inner_ID_m  = inner_OD_m * 0.80    # sch40 approx
    outer_OD_in = inp.get("outer_pipe_in", 3.0)
    outer_ID_m  = outer_OD_in * 0.0254 * 0.87

    # Annulus hydraulic diameter
    De_ann = outer_ID_m - inner_OD_m

    hairpin_L = inp.get("hairpin_L", 6.0)   # m
    A_per_hairpin = math.pi * inner_OD_m * hairpin_L
    N_hairpins = max(1, math.ceil(A_req / A_per_hairpin))

    # Inner tube velocity (cold)
    A_inner = math.pi * inner_ID_m**2 / 4
    v_inner = mdot_c / max(1e-9, pc["rho"] * A_inner)
    Re_inner= pc["rho"] * v_inner * inner_ID_m / max(1e-12, pc["mu"])
    Pr_inner= pc["Cp"] * pc["mu"] / max(1e-12, pc["k"])
    Nu_inner= dittus_boelter(max(10,Re_inner), Pr_inner) if Re_inner>4000 else 3.66
    h_inner = Nu_inner * pc["k"] / inner_ID_m

    # Annulus (hot)
    A_ann   = math.pi * (outer_ID_m**2 - inner_OD_m**2) / 4
    v_ann   = mdot_h / max(1e-9, ph["rho"] * A_ann)
    Re_ann  = ph["rho"] * v_ann * De_ann / max(1e-12, ph["mu"])
    Pr_ann  = ph["Cp"] * ph["mu"] / max(1e-12, ph["k"])
    Nu_ann  = dittus_boelter(max(10,Re_ann), Pr_ann) if Re_ann>4000 else 3.66
    h_ann   = Nu_ann * ph["k"] / De_ann

    dP_inner = darcy_friction(Re_inner) * (hairpin_L*N_hairpins/inner_ID_m) * \
               pc["rho"] * v_inner**2 / 2
    dP_ann   = darcy_friction(Re_ann)   * (hairpin_L*N_hairpins/De_ann) * \
               ph["rho"] * v_ann**2 / 2

    r.update({"A_req":A_req,"N_hairpins":N_hairpins,"U_dirty":U_dirty,
               "LMTD_cc":LMTD_cc,"h_inner":h_inner,"h_ann":h_ann,
               "Re_inner":Re_inner,"Re_ann":Re_ann,
               "dP_inner_Pa":dP_inner,"dP_ann_Pa":dP_ann,
               "inner_OD_m":inner_OD_m,"outer_ID_m":outer_ID_m,
               "steps":steps,"Q_W":Q})
    log("DP — Heat Duty","Q=ṁ_h×Cp_h×ΔT_h",f"Q={Q/1000:.2f} kW","kW")
    log("DP — LMTD","Counter-current",f"LMTD={LMTD_cc:.2f}°C","°C")
    log("DP — Area & Hairpins","A_hairpin=π×OD×L",f"A={A_req:.2f} m²  N={N_hairpins} hairpins","—")
    log("DP — Inner Tube Re/h",f"Re={Re_inner:.0f}",f"h_i={h_inner:.1f} W/m²·K","W/m²·K")
    log("DP — Annulus Re/h",f"Re={Re_ann:.0f}",f"h_o={h_ann:.1f} W/m²·K","W/m²·K")
    log("DP — Pressure Drop","Darcy-Weisbach",
        f"Inner: {dP_inner/1000:.2f} kPa   Annulus: {dP_ann/1000:.2f} kPa","kPa")
    return r


# ─────────────────────────────────────────────────────────────────────────────
# 8.  AIR COOLED (FIN FAN) DESIGN
# ─────────────────────────────────────────────────────────────────────────────

def design_air_cooled(inp: dict) -> dict:
    """
    Air-cooled HX (Fin Fan) design.
    Ref: API 661; Kern (1950) Ch.15; GPSA Engineering Data Book.
    """
    r = {}; steps = []
    def log(t,f,v,u=""): steps.append({"title":t,"formula":f,"value":v,"unit":u})

    T1=inp["T1"]; T2=inp["T2"]
    T_amb = inp.get("T_amb_C", 35.0)   # ambient air temperature
    mdot_h=inp["mdot_h"]
    T_avg_h=(T1+T2)/2
    ph=fluid_properties(inp["hot_fluid"],T_avg_h)

    Q = mdot_h * ph["Cp"] * (T1 - T2)
    r["Q_kW"] = Q/1000

    # Air side
    T_air_out= inp.get("T_air_out_C", min(T2 - 10, T_amb + 20))
    pa = fluid_properties("Air", (T_amb + T_air_out) / 2)
    mdot_air = Q / max(1, pa["Cp"] * (T_air_out - T_amb))

    LMTD_cc = lmtd_counter(T1, T2, T_amb, T_air_out)

    # Finned tube parameters
    fin_density_fpi = inp.get("fin_density_fpi", 10)   # fins per inch
    fin_ht_m        = inp.get("fin_height_mm", 16) / 1000
    tube_OD_m       = inp.get("tube_OD_mm", 25.4) / 1000

    # Extended area ratio (approximate)
    fins_per_m = fin_density_fpi * 39.37
    fin_area_ratio = 1 + 2 * fin_ht_m * fins_per_m
    eta_fin = 0.85   # fin efficiency (typical)
    effective_ratio = 1 + eta_fin * (fin_area_ratio - 1)

    v_face = inp.get("v_face_ms", 2.5)   # face velocity m/s
    D_h_air = 0.012   # hydraulic dia of fin array (m, approximate)
    Re_air  = pa["rho"] * v_face * D_h_air / max(1e-12, pa["mu"])
    Pr_air  = pa["Cp"] * pa["mu"] / max(1e-12, pa["k"])
    h_air_bare = 0.2 * (pa["k"] / D_h_air) * Re_air**0.6 * Pr_air**0.33
    h_air_fin  = h_air_bare * effective_ratio

    # Tube-side (process fluid)
    ID_m = tube_OD_m * 0.83
    A_tube_flow = math.pi * ID_m**2 / 4
    v_tube = mdot_h / max(1e-9, ph["rho"] * A_tube_flow)
    Re_tube = ph["rho"] * v_tube * ID_m / max(1e-12, ph["mu"])
    Pr_tube = ph["Cp"] * ph["mu"] / max(1e-12, ph["k"])
    Nu_tube = dittus_boelter(max(10, Re_tube), Pr_tube)
    h_proc  = Nu_tube * ph["k"] / ID_m

    Rf_proc = inp.get("fouling_h", 0.0002)
    U_eff   = 1 / (1/h_proc + 1/h_air_fin + Rf_proc)
    A_req   = Q / max(1e-3, U_eff * LMTD_cc)
    N_tubes = max(1, math.ceil(A_req / (math.pi * tube_OD_m * 3.0)))   # 3m tube assumed

    # Fan power
    dP_air = 0.5 * pa["rho"] * v_face**2 * (1 + fin_area_ratio * 0.15)
    fan_vol_flow = mdot_air / max(0.1, pa["rho"])
    P_fan_kW = dP_air * fan_vol_flow / max(1, pa["rho"]) / 0.65 / 1000

    r.update({"A_req":A_req,"N_tubes":N_tubes,"U_eff":U_eff,
               "LMTD_cc":LMTD_cc,"h_air_fin":h_air_fin,"h_proc":h_proc,
               "Re_air":Re_air,"Re_tube":Re_tube,
               "dP_air_Pa":dP_air,"P_fan_kW":P_fan_kW,
               "mdot_air":mdot_air,"steps":steps,"Q_W":Q})
    log("AC — Heat Duty","Q=ṁ_h×Cp_h×ΔT_h",f"Q={Q/1000:.2f} kW","kW")
    log("AC — LMTD","Counter-current",f"LMTD={LMTD_cc:.2f}°C","°C")
    log("AC — Air-side h (finned)","h=0.2×(k/Dh)×Re^0.6×Pr^0.33×η_fin",
        f"h_air_fin={h_air_fin:.1f} W/m²·K","W/m²·K")
    log("AC — Process-side h","Dittus-Boelter",f"h_proc={h_proc:.1f} W/m²·K","W/m²·K")
    log("AC — Area","A=Q/(U×LMTD)",f"A={A_req:.2f} m²  N_tubes={N_tubes}","—")
    log("AC — Fan Power","P=ΔP×Q̇_air/(η=65%)",f"P_fan={P_fan_kW:.2f} kW","kW")
    return r


# ─────────────────────────────────────────────────────────────────────────────
# 9.  SPIRAL HEAT EXCHANGER DESIGN
# ─────────────────────────────────────────────────────────────────────────────

def design_spiral(inp: dict) -> dict:
    """
    Spiral HX design.
    Ref: ALFA LAVAL Spiral Handbook; Rosenblad (1970).
    """
    r = {}; steps = []
    def log(t,f,v,u=""): steps.append({"title":t,"formula":f,"value":v,"unit":u})

    T1=inp["T1"]; T2=inp["T2"]; t1=inp["t1"]; t2=inp["t2"]
    mdot_h=inp["mdot_h"]
    T_avg_h=(T1+T2)/2; T_avg_c=(t1+t2)/2
    ph=fluid_properties(inp["hot_fluid"],T_avg_h)
    pc=fluid_properties(inp["cold_fluid"],T_avg_c)

    Q = mdot_h * ph["Cp"] * (T1 - T2)
    mdot_c = Q / max(1, pc["Cp"] * (t2 - t1))
    r["Q_kW"]=Q/1000; r["mdot_c"]=mdot_c

    LMTD_cc = lmtd_counter(T1, T2, t1, t2)
    gap_m   = inp.get("gap_mm", 10) / 1000
    plate_t = inp.get("plate_t_mm", 4) / 1000
    D_h     = gap_m * 2   # hydraulic diameter = 2 × gap
    width   = inp.get("width_m", 1.0)

    # Hot-side channel
    A_flow_h = gap_m * width
    v_h = mdot_h / max(1e-9, ph["rho"] * A_flow_h)
    Re_h= ph["rho"] * v_h * D_h / max(1e-12, ph["mu"])
    Pr_h= ph["Cp"] * ph["mu"] / max(1e-12, ph["k"])
    spiral_corr = 1.15   # spiral flow correction factor (Dean number effect)
    Nu_h = 0.023 * max(10,Re_h)**0.8 * Pr_h**0.33 * spiral_corr
    h_h  = Nu_h * ph["k"] / D_h

    # Cold-side
    A_flow_c = gap_m * width
    v_c = mdot_c / max(1e-9, pc["rho"] * A_flow_c)
    Re_c= pc["rho"] * v_c * D_h / max(1e-12, pc["mu"])
    Pr_c= pc["Cp"] * pc["mu"] / max(1e-12, pc["k"])
    Nu_c= 0.023 * max(10,Re_c)**0.8 * Pr_c**0.33 * spiral_corr
    h_c = Nu_c * pc["k"] / D_h

    Rfh=inp.get("fouling_h",0.0002); Rfc=inp.get("fouling_c",0.0002)
    U_s = 1/(1/h_h + 1/h_c + Rfh + Rfc)
    A_req = Q / max(1e-3, U_s * LMTD_cc)

    # Spiral geometry
    L_channel = A_req / max(1e-6, width)
    # Approximate diameter: L ≈ π * N_turns * D_avg  → D ≈ 2*sqrt(L*(gap+plate_t)/π)
    D_spiral  = 2 * math.sqrt(L_channel * (gap_m + plate_t) / math.pi)

    K_spiral = 3.0   # pressure loss coefficient for spiral
    dP_h = K_spiral * ph["rho"] * v_h**2 / 2 * (L_channel / D_h)
    dP_c = K_spiral * pc["rho"] * v_c**2 / 2 * (L_channel / D_h)

    r.update({"A_req":A_req,"U_s":U_s,"LMTD_cc":LMTD_cc,
               "h_h":h_h,"h_c":h_c,"Re_h":Re_h,"Re_c":Re_c,
               "L_channel":L_channel,"D_spiral":D_spiral,
               "dP_h_Pa":dP_h,"dP_c_Pa":dP_c,
               "steps":steps,"Q_W":Q})
    log("SP — Heat Duty","Q=ṁ_h×Cp_h×ΔT_h",f"Q={Q/1000:.2f} kW","kW")
    log("SP — LMTD","Counter-current",f"LMTD={LMTD_cc:.2f}°C","°C")
    log("SP — Hot-side h","Nu=0.023×Re^0.8×Pr^0.33×1.15",f"h_h={h_h:.1f} W/m²·K","W/m²·K")
    log("SP — Cold-side h","Nu=0.023×Re^0.8×Pr^0.33×1.15",f"h_c={h_c:.1f} W/m²·K","W/m²·K")
    log("SP — U and Area","1/U=1/h_h+1/h_c+Rf",f"U={U_s:.1f}  A={A_req:.2f} m²  D≈{D_spiral:.2f} m","—")
    log("SP — Pressure Drop","ΔP=K_s×(ρv²/2)×(L/D_h)",
        f"Hot: {dP_h/1000:.2f} kPa   Cold: {dP_c/1000:.2f} kPa","kPa")
    return r


# ─────────────────────────────────────────────────────────────────────────────
# 10.  PLOTLY GRAPH GENERATORS
# ─────────────────────────────────────────────────────────────────────────────

PLOTLY_TEMPLATE = "plotly_dark"

def _fig_base(title, xt, yt):
    fig = go.Figure()
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title={"text": title, "font": {"size": 15, "family": "Sora"}},
        xaxis_title=xt, yaxis_title=yt,
        paper_bgcolor="rgba(15,32,39,0.9)",
        plot_bgcolor="rgba(15,32,39,0.9)",
        font={"family": "Sora", "color": "#c8d8e8"},
        margin=dict(l=60, r=30, t=60, b=60),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0.4)", bordercolor="#34e89e",
                    borderwidth=1, font={"size": 11})
    )
    return fig


def graph_temperature_profile(T1, T2, t1, t2, L_m, n=60):
    """Graph 1 — Temperature profile along exchanger. Ref: Kern (1950)."""
    x = np.linspace(0, L_m, n)
    # Counter-current: hot decreases, cold increases
    T_hot  = T1 + (T2 - T1) * x / L_m
    T_cold = t1 + (t2 - t1) * (L_m - x) / L_m   # enters at far end

    LMTD = lmtd_counter(T1, T2, t1, t2)
    fig = _fig_base("🌡 Temperature Profile Along Exchanger", "Length (m)", "Temperature (°C)")
    fig.add_trace(go.Scatter(x=x, y=T_hot, name=f"Hot Fluid ({T1}→{T2}°C)",
                             line=dict(color="#ff5050", width=2.5),
                             hovertemplate="L=%{x:.2f}m  T_hot=%{y:.1f}°C"))
    fig.add_trace(go.Scatter(x=x, y=T_cold, name=f"Cold Fluid ({t1}→{t2}°C)",
                             line=dict(color="#5090ff", width=2.5),
                             hovertemplate="L=%{x:.2f}m  T_cold=%{y:.1f}°C"))
    fig.add_annotation(x=L_m/2, y=(T1+T2+t1+t2)/4,
                       text=f"LMTD = {LMTD:.2f}°C",
                       font=dict(color="#34e89e", size=13, family="JetBrains Mono"),
                       bgcolor="rgba(52,232,158,0.1)", bordercolor="#34e89e",
                       borderpad=6, showarrow=False)
    return fig


def graph_f_factor(P_user=None, R_user=None, n_passes=2):
    """Graph 2 — F-factor correction chart. Ref: Bowman et al. (1940)."""
    P_arr = np.linspace(0.01, 0.99, 80)
    fig = _fig_base("📐 F-Correction Factor — Bowman-Mueller-Nagle (1940)",
                    "P = (t₂−t₁)/(T₁−t₁)", "F Correction Factor")
    R_values = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    colors_r = ["#ff9999","#ffcc66","#66ff99","#66ccff","#cc99ff","#ff99cc"]
    for R, col in zip(R_values, colors_r):
        F_arr = [f_correction_1shell_2pass(p, R) for p in P_arr]
        fig.add_trace(go.Scatter(x=P_arr, y=F_arr, name=f"R={R}",
                                 line=dict(color=col, width=1.8),
                                 hovertemplate=f"R={R}  P=%{{x:.3f}}  F=%{{y:.4f}}"))
    fig.add_hline(y=0.75, line_dash="dash", line_color="#ff6666",
                  annotation_text="F=0.75 Minimum", annotation_font_color="#ff6666")
    if P_user is not None and R_user is not None:
        F_pt = f_correction_1shell_2pass(P_user, R_user)
        fig.add_trace(go.Scatter(x=[P_user], y=[F_pt], mode="markers",
                                 name="Operating Point",
                                 marker=dict(color="#ff0000", size=14, symbol="star"),
                                 hovertemplate=f"P={P_user:.3f}  R={R_user:.3f}  F={F_pt:.4f}"))
    fig.update_layout(yaxis=dict(range=[0.5, 1.02]))
    return fig


def graph_eps_ntu(NTU_pt=None, Cr_pt=None, eps_pt=None):
    """Graph 3 — ε-NTU chart. Ref: Kays & London (1984)."""
    NTU_arr = np.linspace(0, 8, 100)
    fig = _fig_base("⚡ ε-NTU Effectiveness Chart — Kays & London (1984)",
                    "NTU (Number of Transfer Units)", "Effectiveness ε")
    Cr_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    colors_c  = ["#34e89e","#ffd700","#ff9966","#66ccff","#cc99ff"]
    for Cr, col in zip(Cr_values, colors_c):
        eps_arr = [effectiveness_counterflow(n, Cr) for n in NTU_arr]
        fig.add_trace(go.Scatter(x=NTU_arr, y=eps_arr, name=f"Cᵣ={Cr}",
                                 line=dict(color=col, width=2),
                                 hovertemplate=f"Cᵣ={Cr}  NTU=%{{x:.2f}}  ε=%{{y:.4f}}"))
    if NTU_pt is not None and Cr_pt is not None:
        e_pt = eps_pt if eps_pt else effectiveness_counterflow(NTU_pt, Cr_pt)
        fig.add_trace(go.Scatter(x=[NTU_pt], y=[e_pt], mode="markers",
                                 name="Design Point",
                                 marker=dict(color="#ff0000", size=14, symbol="star"),
                                 hovertemplate=f"NTU={NTU_pt:.3f}  ε={e_pt:.4f}"))
    fig.update_layout(yaxis=dict(range=[0, 1.02]))
    return fig


def graph_tube_count(N_tubes_pt=None, Ds_mm_pt=None):
    """Graph 4 — Tube count vs shell diameter. Ref: TEMA Standards."""
    Ds_range = np.linspace(150, 1500, 80)   # mm
    fig = _fig_base("🔧 Tube Count vs Shell Diameter (TEMA)",
                    "Shell Inside Diameter (mm)", "Number of Tubes")
    specs = [("5/8\" OD (15.875mm)", 0.015875, "#ff9999"),
             ("3/4\" OD (19.05mm)",  0.01905,  "#34e89e"),
             ("1\"   OD (25.4mm)",   0.0254,   "#66ccff")]
    for label, OD, col in specs:
        pitch = 1.25 * OD
        N_arr = []
        for Ds_mm in Ds_range:
            Ds = Ds_mm / 1000
            # reverse TEMA formula: N = k1 * (Ds/OD)^n1
            k1, n1 = (0.319, 2.142)
            N_arr.append(int(k1 * (Ds / OD)**n1))
        fig.add_trace(go.Scatter(x=Ds_range, y=N_arr, name=label,
                                 line=dict(color=col, width=2),
                                 hovertemplate=label+" Ds=%{x:.0f}mm N=%{y:.0f}"))
    if N_tubes_pt and Ds_mm_pt:
        fig.add_trace(go.Scatter(x=[Ds_mm_pt], y=[N_tubes_pt], mode="markers",
                                 name="Design Point",
                                 marker=dict(color="#ff0000", size=14, symbol="star")))
    return fig


def graph_moody(Re_pt=None, f_pt=None):
    """Graph 5 — Moody friction factor chart. Ref: Moody (1944)."""
    Re_arr = np.logspace(3, 8, 200)
    fig = _fig_base("📊 Moody Friction Factor Chart — Moody (1944)",
                    "Reynolds Number Re", "Darcy Friction Factor f")
    fig.update_xaxes(type="log"); fig.update_yaxes(type="log")
    eps_D_vals = [0.0, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05]
    colors_m   = ["#34e89e","#ffd700","#ff9966","#66ccff","#ff99cc","#cc99ff","#ffcc66"]
    for eps_D, col in zip(eps_D_vals, colors_m):
        f_arr = [darcy_friction(Re, eps_D) for Re in Re_arr]
        fig.add_trace(go.Scatter(
            x=list(Re_arr), y=f_arr,
            name=f"ε/D={eps_D:.4f}",
            line=dict(color=col, width=1.8),
            hovertemplate=f"ε/D={eps_D}  Re=%{{x:.0f}}  f=%{{y:.5f}}"))
    fig.add_vline(x=2300, line_dash="dash", line_color="yellow",
                  annotation_text="Re=2300", annotation_font_color="yellow")
    fig.add_vline(x=4000, line_dash="dash", line_color="orange",
                  annotation_text="Re=4000", annotation_font_color="orange")
    if Re_pt and f_pt:
        fig.add_trace(go.Scatter(x=[Re_pt], y=[f_pt], mode="markers",
                                 name="Design Point",
                                 marker=dict(color="#ff0000", size=14, symbol="star")))
    return fig


def graph_shell_friction(Re_shell_pt=None, f_shell_pt=None):
    """Graph 6 — Shell-side friction factor. Ref: Kern (1950)."""
    Re_arr = np.logspace(2.5, 6, 150)
    fig = _fig_base("🔩 Shell-Side Friction Factor — Kern (1950)",
                    "Shell-Side Reynolds Number Re_s", "Shell Friction Factor f_s")
    fig.update_xaxes(type="log"); fig.update_yaxes(type="log")
    cuts = [0.15, 0.25, 0.35, 0.45]
    cols = ["#34e89e","#ffd700","#ff9966","#cc99ff"]
    for cut, col in zip(cuts, cols):
        # Kern approximate: f_s ≈ 0.5*Re^-0.2 * (1 + 0.5*cut)
        f_arr = [0.5 * Re**(-0.2) * (1 + 0.5 * cut) for Re in Re_arr]
        fig.add_trace(go.Scatter(x=list(Re_arr), y=f_arr,
                                 name=f"Baffle cut {int(cut*100)}%",
                                 line=dict(color=col, width=2),
                                 hovertemplate=f"Cut={int(cut*100)}%  Re=%{{x:.0f}}  f_s=%{{y:.5f}}"))
    if Re_shell_pt and f_shell_pt:
        fig.add_trace(go.Scatter(x=[Re_shell_pt], y=[f_shell_pt], mode="markers",
                                 name="Design Point",
                                 marker=dict(color="#ff0000", size=14, symbol="star")))
    return fig


def graph_colburn_jH(Re_pt=None, jH_pt=None):
    """Graph 7 — Colburn j_H factor. Ref: Colburn (1933), Kern (1950)."""
    Re_arr = np.logspace(2, 6, 150)
    fig = _fig_base("🔬 Colburn j_H Factor — Colburn (1933)",
                    "Reynolds Number Re_s", "j_H Factor")
    fig.update_xaxes(type="log"); fig.update_yaxes(type="log")
    # Triangular: j_H = 0.36*Re^-0.36; Square: j_H = 0.29*Re^-0.36
    layouts = [("Triangular (30°)", 0.36, "#34e89e"),
               ("Square (90°)",     0.29, "#ffd700"),
               ("Rotated Square",   0.27, "#ff9966")]
    for lbl, coeff, col in layouts:
        jH_arr = [coeff * Re**(-0.36) for Re in Re_arr]
        fig.add_trace(go.Scatter(x=list(Re_arr), y=jH_arr, name=lbl,
                                 line=dict(color=col, width=2),
                                 hovertemplate=lbl+"  Re=%{x:.0f}  j_H=%{y:.5f}"))
    if Re_pt and jH_pt:
        fig.add_trace(go.Scatter(x=[Re_pt], y=[jH_pt], mode="markers",
                                 name="Design Point",
                                 marker=dict(color="#ff0000", size=14, symbol="star")))
    return fig


def graph_dp_vs_flowrate(inp: dict, dP_calc_Pa: float,
                          dP_allow_Pa: float, side: str = "Tube"):
    """Graph 8 — ΔP vs flow rate comparison. Ref: Darcy-Weisbach."""
    mdot_base = inp["mdot_h"] if side == "Shell" else inp.get("mdot_c", inp["mdot_h"])
    if mdot_base is None or mdot_base <= 0:
        mdot_base = 1.0
    flow_arr   = np.linspace(0.1 * mdot_base, 3 * mdot_base, 80)
    dP_arr     = dP_calc_Pa * (flow_arr / mdot_base)**1.8   # turbulent ~1.8 power

    fig = _fig_base(f"📉 ΔP vs Flow Rate ({side} Side) — Darcy-Weisbach",
                    "Flow Rate (kg/s)", "Pressure Drop (kPa)")
    fig.add_trace(go.Scatter(
        x=list(flow_arr), y=list(dP_arr / 1000),
        name="Calculated ΔP", line=dict(color="#ff5050", width=2.5),
        hovertemplate="ṁ=%{x:.2f} kg/s   ΔP=%{y:.2f} kPa"))
    fig.add_hline(y=dP_allow_Pa / 1000, line_dash="dash",
                  line_color="#34e89e", line_width=2,
                  annotation_text=f"Allowable ΔP = {dP_allow_Pa/1000:.1f} kPa",
                  annotation_font_color="#34e89e")
    fig.add_vline(x=mdot_base, line_dash="dot", line_color="#ffd700",
                  annotation_text=f"Design ṁ = {mdot_base:.2f} kg/s",
                  annotation_font_color="#ffd700")
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# 11.  REPORT GENERATORS (PDF · WORD · TXT)
# ─────────────────────────────────────────────────────────────────────────────

FOOTER_TEXT  = "🔬 Developed by ZUNAIR SHAHZAD | Chemical Engineering | UET Lahore (New Campus)"
FOOTER_NOTE  = "(2022-CH-246)"

# ── 11a. PDF Report ──────────────────────────────────────────────────────────

def _pdf_add_footer(canvas_obj, doc):
    """ReportLab page callback — adds coloured footer."""
    canvas_obj.saveState()
    W, H = A4
    y = 18 * mm

    # Background bar
    canvas_obj.setFillColorRGB(0.05, 0.12, 0.18)
    canvas_obj.rect(0, 0, W, y + 4 * mm, fill=1, stroke=0)

    # Green prefix
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColorRGB(0.18, 0.83, 0.50)
    canvas_obj.drawString(20 * mm, y, "🔬 Developed by")

    # White bold name
    canvas_obj.setFont("Helvetica-Bold", 7.5)
    canvas_obj.setFillColorRGB(1, 1, 1)
    canvas_obj.drawString(51 * mm, y, "ZUNAIR SHAHZAD")

    # Yellow separator + dept
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColorRGB(1.0, 0.84, 0.0)
    canvas_obj.drawString(87 * mm, y, "|  Chemical Engineering  |")

    # White institution
    canvas_obj.setFillColorRGB(1, 1, 1)
    canvas_obj.drawString(139 * mm, y, "UET Lahore (New Campus)")

    # Page number
    canvas_obj.setFillColorRGB(0.6, 0.8, 0.9)
    canvas_obj.drawRightString(W - 20 * mm, y, f"Page {doc.page}")
    canvas_obj.restoreState()


def generate_pdf_report(hx_type: str, inp: dict, res: dict) -> bytes:
    """
    Generate a complete multi-page PDF report using ReportLab.
    Returns bytes object ready for st.download_button.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=28*mm,
        title=f"Heat Exchanger Design Report — {hx_type}",
        author="Zunair Shahzad, UET Lahore"
    )

    styles = getSampleStyleSheet()

    # Custom styles
    s_title = ParagraphStyle("HX_Title", parent=styles["Title"],
                             fontSize=22, textColor=colors.HexColor("#1e88e5"),
                             spaceAfter=4, fontName="Helvetica-Bold",
                             alignment=TA_CENTER)
    s_sub = ParagraphStyle("HX_Sub", parent=styles["Normal"],
                           fontSize=10, textColor=colors.HexColor("#90caf9"),
                           spaceAfter=16, alignment=TA_CENTER)
    s_h1 = ParagraphStyle("HX_H1", parent=styles["Heading1"],
                           fontSize=14, textColor=colors.HexColor("#34e89e"),
                           fontName="Helvetica-Bold", spaceAfter=6,
                           borderPad=(0, 0, 2, 0))
    s_h2 = ParagraphStyle("HX_H2", parent=styles["Heading2"],
                           fontSize=11, textColor=colors.HexColor("#ffd700"),
                           fontName="Helvetica-Bold", spaceAfter=4)
    s_body = ParagraphStyle("HX_Body", parent=styles["Normal"],
                            fontSize=9, textColor=colors.HexColor("#c8d8e8"),
                            spaceAfter=4, leading=14)
    s_mono = ParagraphStyle("HX_Mono", parent=styles["Code"],
                            fontSize=8, textColor=colors.HexColor("#64ffda"),
                            backColor=colors.HexColor("#0a1628"),
                            borderColor=colors.HexColor("#34e89e44"),
                            borderPad=4, borderWidth=0.5,
                            spaceAfter=4, leading=13)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    story = []

    # ── Title page ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph(f"🔥 Heat Exchanger Design Report", s_title))
    story.append(Paragraph(f"Type: {hx_type}", s_title))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph(f"Generated: {now}", s_sub))
    story.append(Paragraph("Designed by: Zunair Shahzad (2022-CH-246)", s_sub))
    story.append(Paragraph("Department of Chemical Engineering — UET Lahore (New Campus)", s_sub))
    story.append(HRFlowable(width="100%", thickness=2,
                             color=colors.HexColor("#34e89e"), spaceAfter=12))

    # Disclaimer
    story.append(Paragraph(
        "This report is generated by the Chemical Engineering Assistant. "
        "All calculations follow TEMA 9th Edition, Kern (1950), Kays &amp; London (1984), "
        "and other industry standards cited within. Results should be verified by a "
        "qualified engineer before implementation.",
        s_body))
    story.append(PageBreak())

    # ── Section 1: Process Conditions ──────────────────────────────────────
    story.append(Paragraph("1. Process Conditions (Input Data)", s_h1))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor("#1a5a6e"), spaceAfter=8))

    tdata_inp = [
        ["Parameter", "Value", "Unit"],
        ["Hot Fluid",     inp.get("hot_fluid","—"),    "—"],
        ["Cold Fluid",    inp.get("cold_fluid","—"),   "—"],
        ["T₁ (hot inlet)",  f"{inp.get('T1','')}",    "°C"],
        ["T₂ (hot outlet)", f"{inp.get('T2','')}",    "°C"],
        ["t₁ (cold inlet)", f"{inp.get('t1','')}",    "°C"],
        ["t₂ (cold outlet)",f"{inp.get('t2','')}",    "°C"],
        ["Hot flow rate ṁ_h", f"{inp.get('mdot_h','')}",  "kg/s"],
        ["Operating pressure", f"{inp.get('P_bar','')}",  "bar"],
        ["Allowable ΔP hot",  f"{inp.get('dP_h_max','')}","kPa"],
        ["Allowable ΔP cold", f"{inp.get('dP_c_max','')}","kPa"],
        ["Fouling R_fh",  f"{inp.get('fouling_h',0.0002):.5f}","m²·K/W"],
        ["Fouling R_fc",  f"{inp.get('fouling_c',0.0002):.5f}","m²·K/W"],
    ]
    t_style = TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0), colors.HexColor("#1e3c72")),
        ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 1), (-1, -1), colors.HexColor("#0a1628")),
        ("TEXTCOLOR",   (0, 1), (-1, -1), colors.HexColor("#c8d8e8")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#0a1628"),
                                          colors.HexColor("#0d1f2d")]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#1a5a6e")),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",       (1, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",(0, 0), (-1, -1), 8),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0,0), (-1, -1), 5),
    ])
    t = Table(tdata_inp, colWidths=[80*mm, 60*mm, 30*mm])
    t.setStyle(t_style)
    story.append(t); story.append(Spacer(1, 10*mm))

    # ── Section 2: Step-by-step calculations ───────────────────────────────
    story.append(Paragraph("2. Step-by-Step Calculations", s_h1))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor("#1a5a6e"), spaceAfter=8))

    steps = res.get("steps", [])
    for i, step in enumerate(steps):
        story.append(Paragraph(f"<b>{step['title']}</b>", s_h2))
        story.append(Paragraph(f"Formula: {step['formula']}", s_body))
        story.append(Paragraph(step['value'], s_mono))
        if i % 6 == 5:
            story.append(Spacer(1, 4*mm))

    story.append(PageBreak())

    # ── Section 3: Key Results ─────────────────────────────────────────────
    story.append(Paragraph("3. Key Results Summary", s_h1))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor("#1a5a6e"), spaceAfter=8))

    def _result_row(label, key, unit, fmt=".2f"):
        val = res.get(key, "—")
        if isinstance(val, (int, float)):
            val = f"{val:{fmt}}"
        return [label, str(val), unit]

    res_rows = [["Result Parameter", "Value", "Unit"]]
    if hx_type == "Shell & Tube":
        res_rows += [
            _result_row("Heat Duty Q",         "Q_kW",        "kW"),
            _result_row("LMTD (counter-curr)", "LMTD_cc",     "°C"),
            _result_row("F Correction Factor", "F",            "—",  ".4f"),
            _result_row("Corrected LMTD",      "LMTD_cf",     "°C"),
            _result_row("U_clean (estimated)", "U_clean",      "W/m²·K", ".0f"),
            _result_row("U_dirty (design)",    "U_dirty",      "W/m²·K", ".0f"),
            _result_row("U_calculated",         "U_calc",       "W/m²·K", ".0f"),
            _result_row("Required Area",        "A_req",        "m²"),
            _result_row("Actual Area",          "A_actual",     "m²"),
            _result_row("Oversurface",          "oversurface_pct","%" , ".1f"),
            _result_row("Number of Tubes",      "N_tubes",      "—",  ".0f"),
            _result_row("Shell Diameter",       "Ds_m",         "m",  ".4f"),
            _result_row("Tube OD",              "OD_m",         "m",  ".5f"),
            _result_row("Tube ID",              "ID_m",         "m",  ".5f"),
            _result_row("Tube Length",          "L_m",          "m"),
            _result_row("Baffle Spacing",       "Bs",           "m",  ".4f"),
            _result_row("Number of Baffles",    "N_baffles",    "—",  ".0f"),
            _result_row("Tube-side Velocity",   "v_tube",       "m/s"),
            _result_row("Shell-side Velocity",  "v_shell",      "m/s"),
            _result_row("Re tube-side",         "Re_tube",      "—",  ".0f"),
            _result_row("Re shell-side",        "Re_shell",     "—",  ".0f"),
            _result_row("h_i (tube-side)",      "h_i",          "W/m²·K", ".1f"),
            _result_row("h_o (shell-side)",     "h_o",          "W/m²·K", ".1f"),
            _result_row("Tube ΔP",              "dP_tube_Pa",   "Pa", ".0f"),
            _result_row("Shell ΔP",             "dP_shell_Pa",  "Pa", ".0f"),
            _result_row("NTU",                  "NTU",          "—"),
            _result_row("Effectiveness ε",      "eps",          "—",  ".4f"),
            _result_row("Capacity Ratio Cr",    "Cr",           "—",  ".4f"),
            _result_row("Equipment Cost",       "C_equip",      "USD",".0f"),
            _result_row("Installed Cost",       "C_install",    "USD",".0f"),
        ]
    else:
        for k, v in res.items():
            if k not in ("steps", "ph", "pc") and isinstance(v, (int, float)):
                res_rows.append([k, f"{v:.3f}", "—"])

    t2 = Table(res_rows, colWidths=[90*mm, 60*mm, 20*mm])
    t2.setStyle(t_style)
    story.append(t2); story.append(PageBreak())

    # ── Section 4: Charts (matplotlib) ────────────────────────────────────
    story.append(Paragraph("4. Design Charts", s_h1))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor("#1a5a6e"), spaceAfter=8))

    if hx_type == "Shell & Tube":
        # Embed temperature profile chart
        fig_buf = io.BytesIO()
        T1_=inp["T1"]; T2_=inp["T2"]; t1_=inp["t1"]; t2_=inp["t2"]
        L_=res.get("L_m", 3.66)
        x_  = np.linspace(0, L_, 60)
        Th_ = T1_ + (T2_-T1_)*x_/L_
        Tc_ = t1_ + (t2_-t1_)*(L_-x_)/L_

        fig_, ax_ = plt.subplots(figsize=(7, 3.5))
        fig_.patch.set_facecolor("#0a1628"); ax_.set_facecolor("#0a1628")
        ax_.plot(x_, Th_, color="#ff5050", lw=2, label=f"Hot ({T1_}→{T2_}°C)")
        ax_.plot(x_, Tc_, color="#5090ff", lw=2, label=f"Cold ({t1_}→{t2_}°C)")
        ax_.set_xlabel("Length (m)", color="white"); ax_.set_ylabel("Temp (°C)", color="white")
        ax_.set_title("Temperature Profile", color="#34e89e", fontsize=11)
        ax_.tick_params(colors="white"); ax_.legend(facecolor="#0d1f2d", edgecolor="#34e89e",
                                                      labelcolor="white")
        for spine in ax_.spines.values(): spine.set_edgecolor("#1a5a6e")
        plt.tight_layout()
        plt.savefig(fig_buf, format="PNG", dpi=120, bbox_inches="tight",
                    facecolor="#0a1628")
        plt.close(fig_)
        fig_buf.seek(0)
        story.append(RLImage(fig_buf, width=140*mm, height=70*mm))
        story.append(Spacer(1, 6*mm))

    # ── Section 5: References ──────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("5. Engineering References", s_h1))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor("#1a5a6e"), spaceAfter=8))

    refs = [
        ["Kern, D.Q.", "Process Heat Transfer", "1950", "Basic method, Kern shell-side"],
        ["TEMA Standards", "9th Edition", "2007", "Mechanical design, tube counts"],
        ["ASME", "BPVC Section VIII", "—", "Pressure vessel design"],
        ["Kays & London", "Compact Heat Exchangers, 3rd Ed.", "1984", "ε-NTU method"],
        ["Bowman, Mueller, Nagle", "Ind. Eng. Chem.", "1940", "F-correction factors"],
        ["Dittus & Boelter", "Univ. Calif. Publ. Eng.", "1930", "Tube-side correlation"],
        ["Colburn, A.P.", "Trans. AIChE", "1933", "j_H shell-side method"],
        ["Darcy-Weisbach", "Hydraulic equation", "—", "Pressure drop"],
        ["Crane Co.", "Technical Paper No. 410", "—", "Minor losses"],
        ["API", "Standard 661", "—", "Air-cooled heat exchangers"],
        ["ALFA LAVAL", "PHE Design Handbook", "—", "Plate heat exchangers"],
        ["Coulson & Richardson", "Chemical Eng. Vol. 6", "1999", "Equipment design"],
        ["Guthrie, K.M.", "Chem. Eng.", "1969", "Equipment cost correlations"],
        ["Moody, L.F.", "Trans. ASME", "1944", "Friction factor chart"],
    ]
    ref_data = [["Author", "Title", "Year", "Application"]] + refs
    t_ref = Table(ref_data, colWidths=[40*mm, 55*mm, 18*mm, 57*mm])
    t_ref.setStyle(t_style)
    story.append(t_ref)

    #doc.build(story, onFirstPage=_pdf_add_footer, onLaterPages=_pdf_add_footer)
    return buf.getvalue()


# ── 11b. Word / HTML Report ──────────────────────────────────────────────────

def generate_word_report(hx_type: str, inp: dict, res: dict) -> bytes:
    """
    Generate Word-compatible HTML report (.doc).
    Returns bytes for download.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    steps = res.get("steps", [])

    step_html = ""
    for s in steps:
        step_html += f"""
        <div style='background:#0a1628;border-left:3px solid #34e89e;
                    padding:10px 14px;margin:6px 0;border-radius:4px;'>
          <b style='color:#34e89e;font-size:11pt;'>{s['title']}</b><br>
          <span style='color:#aabbcc;font-size:9pt;'><i>Formula:</i> {s['formula']}</span><br>
          <code style='color:#64ffda;font-size:9.5pt;'>{s['value']}</code>
        </div>"""

    def row(label, key, unit, fmt=".2f"):
        val = res.get(key, "—")
        if isinstance(val, (int, float)): val = f"{val:{fmt}}"
        return f"<tr><td>{label}</td><td><b style='color:#34e89e'>{val}</b></td><td>{unit}</td></tr>"

    if hx_type == "Shell & Tube":
        result_rows = (
            row("Heat Duty Q",          "Q_kW",         "kW")        +
            row("LMTD",                 "LMTD_cc",      "°C")        +
            row("F Factor",             "F",            "—",  ".4f")+
            row("Corrected LMTD",       "LMTD_cf",      "°C")        +
            row("U_clean",              "U_clean",      "W/m²·K",".0f")+
            row("U_dirty",              "U_dirty",      "W/m²·K",".0f")+
            row("U_calculated",          "U_calc",       "W/m²·K",".0f")+
            row("Required Area",         "A_req",        "m²")        +
            row("Actual Area",           "A_actual",     "m²")        +
            row("No. of Tubes",          "N_tubes",      "—",  ".0f")+
            row("Shell Diameter",        "Ds_m",         "m",  ".4f")+
            row("Tube-side v",           "v_tube",       "m/s")       +
            row("Shell-side v",          "v_shell",      "m/s")       +
            row("Re_tube",               "Re_tube",      "—",  ".0f")+
            row("Re_shell",              "Re_shell",     "—",  ".0f")+
            row("h_i",                   "h_i",          "W/m²·K",".1f")+
            row("h_o",                   "h_o",          "W/m²·K",".1f")+
            row("ΔP tube",               "dP_tube_Pa",   "Pa", ".0f")+
            row("ΔP shell",              "dP_shell_Pa",  "Pa", ".0f")+
            row("NTU",                   "NTU",          "—")         +
            row("Effectiveness ε",       "eps",          "—",  ".4f")+
            row("Equipment Cost",        "C_equip",      "USD",".0f")+
            row("Installed Cost",        "C_install",    "USD",".0f")
        )
    else:
        result_rows = ""
        for k, v in res.items():
            if k not in ("steps","ph","pc") and isinstance(v,(int,float)):
                result_rows += f"<tr><td>{k}</td><td><b style='color:#34e89e'>{v:.3f}</b></td><td>—</td></tr>"

    html = f"""<html><head><meta charset='UTF-8'>
    <style>
      body{{background:#0d1f2d;color:#c8d8e8;font-family:Calibri,sans-serif;margin:30px 50px;}}
      h1{{color:#1e88e5;font-size:22pt;border-bottom:2px solid #34e89e;padding-bottom:8px;}}
      h2{{color:#34e89e;font-size:14pt;margin-top:26px;}}
      h3{{color:#ffd700;font-size:11pt;}}
      table{{width:100%;border-collapse:collapse;margin:12px 0;}}
      th{{background:#1e3c72;color:#fff;padding:8px 12px;text-align:left;font-size:10pt;}}
      td{{padding:7px 12px;font-size:9.5pt;border-bottom:1px solid #1a5a6e;}}
      tr:nth-child(even){{background:#0a1628;}}
      .footer{{background:#0a1628;border-top:2px solid #34e89e;padding:12px 20px;
               margin-top:30px;font-size:9pt;text-align:center;}}
      code{{color:#64ffda;font-family:Consolas,monospace;font-size:9.5pt;}}
    </style></head><body>

    <h1>🔥 Heat Exchanger Design Report — {hx_type}</h1>
    <p><b>Generated:</b> {now}<br>
       <b>Designed by:</b> Zunair Shahzad (2022-CH-246)<br>
       <b>Department:</b> Chemical Engineering — UET Lahore (New Campus)</p>

    <h2>1. Process Conditions</h2>
    <table>
      <tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>
      <tr><td>Hot Fluid</td><td>{inp.get('hot_fluid','—')}</td><td>—</td></tr>
      <tr><td>Cold Fluid</td><td>{inp.get('cold_fluid','—')}</td><td>—</td></tr>
      <tr><td>T₁ (hot inlet)</td><td>{inp.get('T1','')}</td><td>°C</td></tr>
      <tr><td>T₂ (hot outlet)</td><td>{inp.get('T2','')}</td><td>°C</td></tr>
      <tr><td>t₁ (cold inlet)</td><td>{inp.get('t1','')}</td><td>°C</td></tr>
      <tr><td>t₂ (cold outlet)</td><td>{inp.get('t2','')}</td><td>°C</td></tr>
      <tr><td>Hot flow ṁ_h</td><td>{inp.get('mdot_h','')}</td><td>kg/s</td></tr>
      <tr><td>Pressure</td><td>{inp.get('P_bar','')}</td><td>bar</td></tr>
    </table>

    <h2>2. Step-by-Step Calculations</h2>
    {step_html}

    <h2>3. Key Results</h2>
    <table>
      <tr><th>Parameter</th><th>Value</th><th>Unit</th></tr>
      {result_rows}
    </table>

    <h2>4. Engineering References</h2>
    <table>
      <tr><th>Author</th><th>Title</th><th>Year</th><th>Application</th></tr>
      <tr><td>Kern, D.Q.</td><td>Process Heat Transfer</td><td>1950</td><td>Basic method</td></tr>
      <tr><td>TEMA</td><td>Standards 9th Edition</td><td>2007</td><td>Mechanical design</td></tr>
      <tr><td>Kays &amp; London</td><td>Compact Heat Exchangers</td><td>1984</td><td>ε-NTU method</td></tr>
      <tr><td>Bowman et al.</td><td>Ind. Eng. Chem.</td><td>1940</td><td>F-correction factors</td></tr>
      <tr><td>Dittus-Boelter</td><td>Univ. Calif. Publ. Eng.</td><td>1930</td><td>Tube-side HTC</td></tr>
      <tr><td>Colburn</td><td>Trans. AIChE</td><td>1933</td><td>Shell-side j_H</td></tr>
      <tr><td>API</td><td>Standard 661</td><td>—</td><td>Air cooled HX</td></tr>
      <tr><td>ALFA LAVAL</td><td>PHE Handbook</td><td>—</td><td>Plate HX</td></tr>
    </table>

    <div class='footer'>
      <span style='color:#2ecc71'>🔬 Developed by</span>
      <b style='color:#fff'> ZUNAIR SHAHZAD </b>
      <span style='color:#ffd700'>| Chemical Engineering |</span>
      <span style='color:#fff'> UET Lahore (New Campus)</span>
    </div>
    </body></html>"""
    return html.encode("utf-8")


# ── 11c. TXT Report ──────────────────────────────────────────────────────────

def generate_txt_report(hx_type: str, inp: dict, res: dict) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "=" * 70,
        f"  HEAT EXCHANGER DESIGN REPORT — {hx_type.upper()}",
        "=" * 70,
        f"  Generated : {now}",
        f"  Designed by: Zunair Shahzad (2022-CH-246)",
        f"  Dept       : Chemical Engineering, UET Lahore (New Campus)",
        "=" * 70, "",
        "SECTION 1 — PROCESS CONDITIONS",
        "-" * 40,
    ]
    for k, v in inp.items():
        if k not in ("fouling_h","fouling_c"):
            lines.append(f"  {k:28s}: {v}")
    lines += ["",
              "SECTION 2 — STEP-BY-STEP CALCULATIONS",
              "-" * 40]
    for s in res.get("steps", []):
        lines += [f"  {s['title']}", f"    Formula: {s['formula']}",
                  f"    Result : {s['value']}", ""]

    lines += ["SECTION 3 — KEY RESULTS", "-" * 40]
    skip = {"steps", "ph", "pc", "warn_F"}
    for k, v in res.items():
        if k not in skip and isinstance(v, (int, float)):
            lines.append(f"  {k:30s}: {v:.4f}")

    lines += ["",
              "SECTION 4 — REFERENCES",
              "-" * 40,
              "  Kern (1950)          - Process Heat Transfer",
              "  TEMA (2007)          - Standards 9th Edition",
              "  Kays & London (1984) - Compact Heat Exchangers (ε-NTU)",
              "  Bowman et al.(1940)  - F-correction factors",
              "  Dittus-Boelter(1930) - Tube-side heat transfer",
              "  Colburn (1933)       - j_H factor method",
              "  Darcy-Weisbach       - Pressure drop",
              "  API 661              - Air cooled heat exchangers",
              "  ALFA LAVAL Handbook  - Plate heat exchangers",
              "  Guthrie (1969)       - Equipment cost correlations",
              "",
              "=" * 70,
              f"  🌟 🔬 Developed by ZUNAIR SHAHZAD | Chemical Engineering | UET Lahore (New Campus) 🌟",
              "=" * 70,
              ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 12.  HELPER UI COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────

def result_card(label: str, value, unit: str = ""):
    """Render a styled result card."""
    if isinstance(value, float):
        if abs(value) >= 1e6:      val_str = f"{value:,.0f}"
        elif abs(value) >= 1000:   val_str = f"{value:,.1f}"
        elif abs(value) >= 10:     val_str = f"{value:.2f}"
        elif abs(value) >= 0.1:    val_str = f"{value:.4f}"
        else:                       val_str = f"{value:.3e}"
    elif isinstance(value, int):
        val_str = f"{value:,}"
    else:
        val_str = str(value)

    st.markdown(f"""
    <div class="result-card">
      <div class="label">{label}</div>
      <div class="value">{val_str}</div>
      <div class="unit">{unit}</div>
    </div>""", unsafe_allow_html=True)


def section_header(icon: str, title: str):
    st.markdown(f"""
    <div class="section-header">
      <h3>{icon} {title}</h3>
    </div>""", unsafe_allow_html=True)


def show_steps(steps: list):
    """Render calculation steps in expandable monospace boxes."""
    with st.expander("📋 View Complete Step-by-Step Calculations", expanded=False):
        for s in steps:
            st.markdown(f"""
            <div class="calc-step">
              <div class="step-title">{s['title']}</div>
              <span class="formula">Formula: {s['formula']}</span><br>
              <span class="result-line">▶ {s['value']}</span>
            </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 13.  MAIN STREAMLIT FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def show_heat_exchanger():
    """
    Main entry point for the Heat Exchanger Designer page.
    Call this from your main app router: show_heat_exchanger()
    """
    st.set_page_config(page_title="Heat Exchanger Designer",
                       page_icon="🔥", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ── Main header ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="main-header">
      <h1>🔥 Industrial Heat Exchanger Designer</h1>
      <p>TEMA · ASME · API 661 · Kern (1950) · Kays & London (1984) · ε-NTU Method</p>
      <p style='font-size:0.82rem;margin-top:4px;opacity:0.6;'>
        Production-grade design tool · 5 exchanger types · 33-step calculations · 8 interactive graphs
      </p>
    </div>""", unsafe_allow_html=True)

    # ── Session state initialisation ────────────────────────────────────────
    if "hx_results" not in st.session_state:
        st.session_state.hx_results = None
    if "hx_inp" not in st.session_state:
        st.session_state.hx_inp = {}
    if "hx_type_sel" not in st.session_state:
        st.session_state.hx_type_sel = None

    # ═══════════════════════════════════════════════════════════════════════
    # A.  INPUT PANEL
    # ═══════════════════════════════════════════════════════════════════════
    section_header("📥", "Process Conditions")

    FLUIDS = ["Water", "Steam", "Oil (Mineral)", "Air",
              "Gas (Generic)", "Organic Solvent", "Brine (NaCl 20%)"]
    FOULING_OPTIONS = {
        "Clean water (0.0001)":        0.0001,
        "Treated cooling water (0.0002)": 0.0002,
        "Cooling tower water (0.0004)": 0.0004,
        "Oil / petroleum (0.0004)":    0.0004,
        "Steam (0.0001)":              0.0001,
        "Sea water (0.0002)":          0.0002,
        "Organic solvent (0.0002)":    0.0002,
        "Gas / air (0.0002)":          0.0002,
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<p class="input-label">🔴 Hot Fluid</p>', unsafe_allow_html=True)
        hot_fluid = st.selectbox("Hot Fluid", FLUIDS, index=0, key="hot_f",
                                  label_visibility="collapsed")
        st.markdown('<p class="input-label">🌡 T₁ — Hot Inlet (°C)</p>', unsafe_allow_html=True)
        T1 = st.number_input("T1", value=150.0, min_value=0.1, key="T1_in",
                              label_visibility="collapsed")
        st.markdown('<p class="input-label">🌡 T₂ — Hot Outlet (°C)</p>', unsafe_allow_html=True)
        T2 = st.number_input("T2", value=90.0, min_value=0.1, key="T2_in",
                              label_visibility="collapsed")
        st.markdown('<p class="input-label">⚖ Hot Flow Rate ṁ_h (kg/s)</p>', unsafe_allow_html=True)
        mdot_h = st.number_input("mdot_h", value=5.0, min_value=0.001, key="mh_in",
                                  label_visibility="collapsed")

    with col2:
        st.markdown('<p class="input-label">🔵 Cold Fluid</p>', unsafe_allow_html=True)
        cold_fluid = st.selectbox("Cold Fluid", FLUIDS, index=0, key="cold_f",
                                   label_visibility="collapsed")
        st.markdown('<p class="input-label">🌡 t₁ — Cold Inlet (°C)</p>', unsafe_allow_html=True)
        t1 = st.number_input("t1", value=30.0, min_value=0.1, key="t1_in",
                              label_visibility="collapsed")
        st.markdown('<p class="input-label">🌡 t₂ — Cold Outlet (°C)</p>', unsafe_allow_html=True)
        t2 = st.number_input("t2", value=70.0, min_value=0.1, key="t2_in",
                              label_visibility="collapsed")
        st.markdown('<p class="input-label">⚖ Cold Flow Rate ṁ_c (kg/s)</p>', unsafe_allow_html=True)
        mdot_c_inp = st.number_input("mdot_c (0 = calculate)", value=8.0,
                                      min_value=0.0, key="mc_in",
                                      label_visibility="collapsed")

    with col3:
        st.markdown('<p class="input-label">🔧 Operating Pressure (bar)</p>', unsafe_allow_html=True)
        P_bar = st.number_input("P_bar", value=10.0, min_value=0.1, key="pbar_in",
                                 label_visibility="collapsed")
        st.markdown('<p class="input-label">⬇ Max ΔP Hot (kPa)</p>', unsafe_allow_html=True)
        dP_h_max = st.number_input("dP_h", value=50.0, min_value=1.0, key="dph_in",
                                    label_visibility="collapsed")
        st.markdown('<p class="input-label">⬇ Max ΔP Cold (kPa)</p>', unsafe_allow_html=True)
        dP_c_max = st.number_input("dP_c", value=50.0, min_value=1.0, key="dpc_in",
                                    label_visibility="collapsed")
        st.markdown('<p class="input-label">🧱 Fouling — Hot Side</p>', unsafe_allow_html=True)
        fouling_h_key = st.selectbox("Fouling H", list(FOULING_OPTIONS.keys()),
                                      index=1, key="fh_sel",
                                      label_visibility="collapsed")
        st.markdown('<p class="input-label">🧱 Fouling — Cold Side</p>', unsafe_allow_html=True)
        fouling_c_key = st.selectbox("Fouling C", list(FOULING_OPTIONS.keys()),
                                      index=1, key="fc_sel",
                                      label_visibility="collapsed")

    fouling_h = FOULING_OPTIONS[fouling_h_key]
    fouling_c = FOULING_OPTIONS[fouling_c_key]

    # ── Validate inputs ──────────────────────────────────────────────────────
    inp_valid = True
    errors = []
    if T1 <= T2:
        errors.append("T₁ must be greater than T₂ (hot inlet > hot outlet)")
        inp_valid = False
    if t2 <= t1:
        errors.append("t₂ must be greater than t₁ (cold outlet > cold inlet)")
        inp_valid = False
    if T1 <= t1:
        errors.append("T₁ must be greater than t₁ (hot inlet > cold inlet) for feasible HX")
        inp_valid = False
    for e in errors:
        st.markdown(f'<div class="error-box">⛔ {e}</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # B.  SMART RECOMMENDATION
    # ═══════════════════════════════════════════════════════════════════════
    if inp_valid:
        Q_est_kW = mdot_h * fluid_properties(hot_fluid,(T1+T2)/2)["Cp"] * (T1-T2) / 1000
        rec = recommend_hx_type(Q_est_kW, P_bar, T1,
                                 fouling_h, fouling_c, hot_fluid, cold_fluid)

        section_header("💡", "Smart Recommendation")
        col_r1, col_r2 = st.columns([2, 1])
        with col_r1:
            reasons_html = "".join(f"<li>{r}</li>" for r in rec["reasons"])
            refs_html    = ", ".join(rec["references"])
            st.markdown(f"""
            <div class="rec-card">
              <h4>Recommended Heat Exchanger Type</h4>
              <div class="rec-type">✅ {rec['type']}</div>
              <ul>{reasons_html}</ul>
              <p style='color:#90caf9;font-size:0.8rem;margin-top:10px;'>
                📚 References: {refs_html}
              </p>
            </div>""", unsafe_allow_html=True)
        with col_r2:
            st.metric("Estimated Duty", f"{Q_est_kW:.1f} kW")
            st.metric("Operating Pressure", f"{P_bar:.1f} bar")
            st.metric("Fouling R_fh", f"{fouling_h:.4f} m²·K/W")

        # ── HX type selector ────────────────────────────────────────────────
        section_header("🔧", "Select Heat Exchanger Type")
        HX_TYPES = ["Shell & Tube", "Plate & Frame", "Double Pipe",
                     "Air Cooled (Fin Fan)", "Spiral"]
        default_idx = HX_TYPES.index(rec["type"]) if rec["type"] in HX_TYPES else 0

        col_acc, col_man = st.columns([1, 2])
        with col_acc:
            if st.button(f"✅ Accept: {rec['type']}", use_container_width=True,
                          type="primary"):
                st.session_state.hx_type_sel = rec["type"]
        with col_man:
            manual_sel = st.selectbox("Or select manually:", HX_TYPES,
                                       index=default_idx, key="hx_man_sel")
            if st.button("🔧 Use Manual Selection", use_container_width=True):
                st.session_state.hx_type_sel = manual_sel

        hx_type = st.session_state.hx_type_sel or rec["type"]
        st.markdown(f'<div class="info-box">🎯 Active design type: <b>{hx_type}</b></div>',
                    unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # C.  TYPE-SPECIFIC DESIGN PARAMETERS
    # ═══════════════════════════════════════════════════════════════════════
        section_header("⚙", "Design Parameters")

        extra_inp = {}

        if hx_type == "Shell & Tube":
            with st.expander("🔩 TEMA / Shell & Tube Configuration", expanded=True):
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown('<p class="input-label">TEMA Type</p>', unsafe_allow_html=True)
                    tema = st.selectbox("TEMA", ["AES","BEM","AEL","CFU","NEN","Custom"],
                                         key="tema_t", label_visibility="collapsed")
                    st.markdown('<p class="input-label">Shell Type</p>', unsafe_allow_html=True)
                    shell_t = st.selectbox("Shell",
                        ["E — One-pass (standard)",
                         "F — Two-pass longitudinal",
                         "G — Split flow",
                         "H — Divided flow",
                         "J — Divided flow (condensers)",
                         "K — Kettle reboiler",
                         "X — Cross flow (gas)"],
                        key="shell_t_sel", label_visibility="collapsed")
                    extra_inp["tema_type"] = tema
                    extra_inp["shell_type"] = shell_t[0]

                with c2:
                    st.markdown('<p class="input-label">Tube OD (mm)</p>', unsafe_allow_html=True)
                    OD_mm = st.selectbox("OD",
                        [15.875, 19.05, 25.4, 31.75],
                        index=1, format_func=lambda x: f'{x} mm ({["5/8","3/4","1","1-1/4"][{15.875:0,19.05:1,25.4:2,31.75:3}[x]]}\")',
                        key="od_sel", label_visibility="collapsed")
                    st.markdown('<p class="input-label">Tube Length (m)</p>', unsafe_allow_html=True)
                    L_m = st.selectbox("Length",
                        [2.44, 3.66, 4.88, 6.10],
                        index=1,
                        format_func=lambda x: f'{x} m ({["8ft","12ft","16ft","20ft"][[2.44,3.66,4.88,6.10].index(x)]})',
                        key="len_sel", label_visibility="collapsed")
                    extra_inp["OD_mm"] = OD_mm
                    extra_inp["length_m"] = L_m

                with c3:
                    st.markdown('<p class="input-label">Tube Layout</p>', unsafe_allow_html=True)
                    layout = st.selectbox("Layout",
                        ["Triangular (30°)", "Rotated Triangular (60°)",
                         "Square (90°)", "Rotated Square (45°)"],
                        key="layout_sel", label_visibility="collapsed")
                    st.markdown('<p class="input-label">Number of Passes</p>', unsafe_allow_html=True)
                    n_passes = st.selectbox("Passes", [1, 2, 4, 6, 8], index=1,
                                             key="pass_sel", label_visibility="collapsed")
                    extra_inp["layout"]   = layout
                    extra_inp["n_passes"] = n_passes

                with c4:
                    st.markdown('<p class="input-label">Baffle Type</p>', unsafe_allow_html=True)
                    baffle_t = st.selectbox("Baffle",
                        ["Single Segmental","Double Segmental",
                         "Triple Segmental","Rod Baffle","Helical"],
                        key="baffle_t_sel", label_visibility="collapsed")
                    st.markdown('<p class="input-label">Baffle Cut (%)</p>', unsafe_allow_html=True)
                    baffle_cut = st.selectbox("Baffle Cut",
                        [15, 25, 35, 45], index=1,
                        format_func=lambda x: f"{x}%",
                        key="bcut_sel", label_visibility="collapsed")
                    st.markdown('<p class="input-label">Tube Material</p>', unsafe_allow_html=True)
                    tube_mat = st.selectbox("Material",
                        ["Carbon Steel", "Stainless Steel 304", "Stainless Steel 316"],
                        key="mat_sel", label_visibility="collapsed")
                    extra_inp["baffle_type"]     = baffle_t
                    extra_inp["baffle_cut_frac"] = baffle_cut / 100
                    extra_inp["tube_material"]   = tube_mat
                    extra_inp["wall_k"] = {"Carbon Steel": 50.0,
                                            "Stainless Steel 304": 16.0,
                                            "Stainless Steel 316": 16.0}[tube_mat]

                # TEMA type information
                TEMA_INFO = {
                    "AES": "General chemical service — removable front cover, single pass E shell, floating S head",
                    "BEM": "High pressure service — bonnet integral, E shell, fixed tubesheet",
                    "AEL": "Fouling/dirty service — AEL type for easy bundle removal and cleaning",
                    "CFU": "Thermal expansion service — CFU with U-tube bundle",
                    "NEN": "Fixed tubesheet, non-removable ends (lowest cost)",
                }
                if tema in TEMA_INFO:
                    st.markdown(f'<div class="info-box">📋 TEMA {tema}: {TEMA_INFO[tema]}</div>',
                                unsafe_allow_html=True)

        elif hx_type == "Plate & Frame":
            with st.expander("🃏 Plate & Frame Configuration", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<p class="input-label">Plate Area (m²)</p>', unsafe_allow_html=True)
                    extra_inp["plate_area"] = st.number_input("Plate area",
                        value=0.5, min_value=0.05, key="pa_in",
                        label_visibility="collapsed")
                    st.markdown('<p class="input-label">Channel Gap (mm)</p>', unsafe_allow_html=True)
                    extra_inp["gap_mm"] = st.selectbox("Gap", [2, 3, 4, 6, 8],
                        index=1, format_func=lambda x: f"{x} mm",
                        key="gap_sel", label_visibility="collapsed")
                with c2:
                    st.markdown('<p class="input-label">Plate Width (m)</p>', unsafe_allow_html=True)
                    extra_inp["plate_width_m"] = st.number_input("Width",
                        value=0.4, min_value=0.1, key="pw_in",
                        label_visibility="collapsed")
                    st.markdown('<p class="input-label">Chevron Angle</p>', unsafe_allow_html=True)
                    st.selectbox("Chevron", ["30° (Low ΔP)", "45° (Medium)", "60° (High HTC)"],
                                  key="chev_sel", label_visibility="collapsed")

        elif hx_type == "Double Pipe":
            with st.expander("🪗 Double Pipe Configuration", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<p class="input-label">Inner Pipe OD (inches)</p>', unsafe_allow_html=True)
                    extra_inp["inner_pipe_in"] = st.selectbox("Inner OD",
                        [1.0, 1.5, 2.0, 2.5, 3.0], index=1,
                        format_func=lambda x: f'{x}"', key="inn_sel",
                        label_visibility="collapsed")
                    st.markdown('<p class="input-label">Outer Pipe OD (inches)</p>', unsafe_allow_html=True)
                    extra_inp["outer_pipe_in"] = st.selectbox("Outer OD",
                        [2.0, 2.5, 3.0, 4.0, 5.0], index=2,
                        format_func=lambda x: f'{x}"', key="out_sel",
                        label_visibility="collapsed")
                with c2:
                    st.markdown('<p class="input-label">Hairpin Length (m)</p>', unsafe_allow_html=True)
                    extra_inp["hairpin_L"] = st.selectbox("Hairpin",
                        [3.0, 4.5, 6.0, 7.5, 9.0], index=2,
                        format_func=lambda x: f"{x} m", key="hp_sel",
                        label_visibility="collapsed")

        elif hx_type == "Air Cooled (Fin Fan)":
            with st.expander("💨 Air Cooled Configuration", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<p class="input-label">Ambient Temperature (°C)</p>', unsafe_allow_html=True)
                    extra_inp["T_amb_C"] = st.number_input("T_amb", value=35.0,
                        key="tamb_in", label_visibility="collapsed")
                    st.markdown('<p class="input-label">Air Outlet Temp (°C)</p>', unsafe_allow_html=True)
                    extra_inp["T_air_out_C"] = st.number_input("T_air_out",
                        value=55.0, key="tao_in", label_visibility="collapsed")
                    st.markdown('<p class="input-label">Fin Density (fins/inch)</p>', unsafe_allow_html=True)
                    extra_inp["fin_density_fpi"] = st.selectbox("Fin density",
                        [2, 4, 6, 8, 10, 12], index=4, key="fin_d_sel",
                        label_visibility="collapsed")
                with c2:
                    st.markdown('<p class="input-label">Air Face Velocity (m/s)</p>', unsafe_allow_html=True)
                    extra_inp["v_face_ms"] = st.selectbox("Face velocity",
                        [1.0, 1.5, 2.0, 2.5, 3.0], index=3, key="vf_sel",
                        label_visibility="collapsed")
                    st.markdown('<p class="input-label">Fin Height (mm)</p>', unsafe_allow_html=True)
                    extra_inp["fin_height_mm"] = st.selectbox("Fin height",
                        [12, 14, 16], index=2, key="fh_h_sel",
                        label_visibility="collapsed")
                    st.markdown('<p class="input-label">Tube OD (mm)</p>', unsafe_allow_html=True)
                    extra_inp["tube_OD_mm"] = st.selectbox("Tube OD AC",
                        [25.4, 31.75, 38.1, 50.8], index=0, key="acod_sel",
                        label_visibility="collapsed")

        elif hx_type == "Spiral":
            with st.expander("🌀 Spiral Configuration", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<p class="input-label">Channel Gap (mm)</p>', unsafe_allow_html=True)
                    extra_inp["gap_mm"] = st.selectbox("Gap SP",
                        [5, 8, 10, 12, 15, 20], index=2,
                        format_func=lambda x: f"{x} mm", key="spgap_sel",
                        label_visibility="collapsed")
                    st.markdown('<p class="input-label">Plate Thickness (mm)</p>', unsafe_allow_html=True)
                    extra_inp["plate_t_mm"] = st.selectbox("Plate t",
                        [3, 4, 5, 6], index=1, format_func=lambda x: f"{x} mm",
                        key="spt_sel", label_visibility="collapsed")
                with c2:
                    st.markdown('<p class="input-label">Channel Width (m)</p>', unsafe_allow_html=True)
                    extra_inp["width_m"] = st.number_input("Width SP",
                        value=1.0, min_value=0.1, key="spw_in",
                        label_visibility="collapsed")

    # ═══════════════════════════════════════════════════════════════════════
    # D.  CALCULATE BUTTON
    # ═══════════════════════════════════════════════════════════════════════
        st.markdown("<br>", unsafe_allow_html=True)
        calc_btn = st.button("🚀 CALCULATE HEAT EXCHANGER",
                              use_container_width=True, type="primary")

        if calc_btn and inp_valid:
            # Build input dict
            full_inp = {
                "T1": T1, "T2": T2, "t1": t1, "t2": t2,
                "mdot_h": mdot_h,
                "mdot_c": mdot_c_inp if mdot_c_inp > 0 else None,
                "mdot_c_given": mdot_c_inp > 0,
                "hot_fluid": hot_fluid, "cold_fluid": cold_fluid,
                "P_bar": P_bar,
                "dP_h_max": dP_h_max, "dP_c_max": dP_c_max,
                "fouling_h": fouling_h, "fouling_c": fouling_c,
                **extra_inp
            }
            if mdot_c_inp > 0:
                full_inp["mdot_c"] = mdot_c_inp

            with st.spinner("⚙ Running industrial-grade calculations…"):
                try:
                    if hx_type == "Shell & Tube":
                        res = design_shell_tube(full_inp)
                    elif hx_type == "Plate & Frame":
                        res = design_plate_frame(full_inp)
                    elif hx_type == "Double Pipe":
                        res = design_double_pipe(full_inp)
                    elif hx_type == "Air Cooled (Fin Fan)":
                        res = design_air_cooled(full_inp)
                    elif hx_type == "Spiral":
                        res = design_spiral(full_inp)
                    else:
                        res = design_shell_tube(full_inp)

                    st.session_state.hx_results = res
                    st.session_state.hx_inp     = full_inp
                    st.session_state.hx_type_sel= hx_type
                    st.success("✅ Design complete! Scroll down for results.")
                except Exception as e:
                    st.error(f"⚠ Calculation error: {e}")
                    import traceback; st.code(traceback.format_exc())

    # ═══════════════════════════════════════════════════════════════════════
    # E.  RESULTS DISPLAY
    # ═══════════════════════════════════════════════════════════════════════
    if st.session_state.hx_results and inp_valid:
        res     = st.session_state.hx_results
        full_inp= st.session_state.hx_inp
        hx_type = st.session_state.hx_type_sel

        # Warnings
        if res.get("warn_F"):
            st.markdown('<div class="warn-box">⚠ F-correction factor < 0.75. '
                        'Consider using multiple shells in series.</div>',
                        unsafe_allow_html=True)
        if hx_type == "Shell & Tube":
            if res.get("v_tube", 0) < 0.5:
                st.markdown('<div class="warn-box">⚠ Tube-side velocity < 0.5 m/s '
                            '— risk of fouling. Reduce tube passes or increase flow.</div>',
                            unsafe_allow_html=True)
            if res.get("v_tube", 0) > 4:
                st.markdown('<div class="warn-box">⚠ Tube-side velocity > 4 m/s '
                            '— risk of erosion. Increase tube count or reduce passes.</div>',
                            unsafe_allow_html=True)
            if res.get("dP_tube_Pa", 0) / 1000 > full_inp.get("dP_c_max", 50):
                st.markdown('<div class="warn-box">⚠ Tube-side ΔP exceeds allowable limit!</div>',
                            unsafe_allow_html=True)
            if res.get("dP_shell_Pa", 0) / 1000 > full_inp.get("dP_h_max", 50):
                st.markdown('<div class="warn-box">⚠ Shell-side ΔP exceeds allowable limit!</div>',
                            unsafe_allow_html=True)

        section_header("📊", "Results")
        tab_th, tab_mech, tab_dp, tab_cost, tab_steps = st.tabs(
            ["🌡 Thermal", "🔩 Mechanical", "💧 Pressure Drop", "💰 Cost", "📋 Calculations"])

        # ── TAB 1: THERMAL ──────────────────────────────────────────────────
        with tab_th:
            cols = st.columns(4)
            thermal_items = [
                ("Heat Duty",         res.get("Q_kW", res.get("Q_W",0)/1000), "kW"),
                ("LMTD",              res.get("LMTD_cc", res.get("LMTD_cf",0)),  "°C"),
                ("F Correction",      res.get("F", 0.98),      "—"),
                ("Corrected LMTD",    res.get("LMTD_cf", res.get("LMTD_cc",0)), "°C"),
                ("U_clean",           res.get("U_clean", 0),   "W/m²·K"),
                ("U_dirty",           res.get("U_dirty", 0),   "W/m²·K"),
                ("U_calculated",      res.get("U_calc", res.get("U_dirty",0)), "W/m²·K"),
                ("Required Area",     res.get("A_req", 0),     "m²"),
                ("NTU",               res.get("NTU", 0),       "—"),
                ("Effectiveness ε",   res.get("eps", 0),       "—"),
                ("Capacity Ratio Cᵣ", res.get("Cr", 0),        "—"),
                ("Oversurface",       res.get("oversurface_pct", 0), "%"),
            ]
            for i, (lbl, val, unit) in enumerate(thermal_items):
                with cols[i % 4]:
                    result_card(lbl, float(val) if val else 0.0, unit)

        # ── TAB 2: MECHANICAL ───────────────────────────────────────────────
        with tab_mech:
            if hx_type == "Shell & Tube":
                cols = st.columns(4)
                mech_items = [
                    ("Number of Tubes",  res.get("N_tubes", 0),            "—"),
                    ("Shell Diameter",   res.get("Ds_m", 0) * 1000,        "mm"),
                    ("Tube Length",      res.get("L_m", 0),                "m"),
                    ("Tube OD",          res.get("OD_m", 0) * 1000,        "mm"),
                    ("Tube ID",          res.get("ID_m", 0) * 1000,        "mm"),
                    ("Tube Pitch",       res.get("pitch_m", 0) * 1000,     "mm"),
                    ("Baffle Spacing",   res.get("Bs", 0) * 1000,          "mm"),
                    ("No. Baffles",      res.get("N_baffles", 0),          "—"),
                    ("Tube-side v",      res.get("v_tube", 0),             "m/s"),
                    ("Shell-side v",     res.get("v_shell", 0),            "m/s"),
                    ("Re_tube",          res.get("Re_tube", 0),            "—"),
                    ("Re_shell",         res.get("Re_shell", 0),           "—"),
                    ("h_i (tube)",       res.get("h_i", 0),                "W/m²·K"),
                    ("h_o (shell)",      res.get("h_o", 0),                "W/m²·K"),
                    ("Wall Temperature", res.get("T_wall", 0),             "°C"),
                ]
                for i, (lbl, val, unit) in enumerate(mech_items):
                    with cols[i % 4]:
                        result_card(lbl, float(val) if val else 0.0, unit)
            elif hx_type == "Plate & Frame":
                c1, c2 = st.columns(2)
                with c1:
                    result_card("Number of Plates", float(res.get("N_plates",0)), "—")
                    result_card("Number of Channels", float(res.get("N_channels",0)), "—")
                    result_card("Channel Re", float(res.get("Re_ch",0)), "—")
                with c2:
                    result_card("Channel h", float(res.get("h_ch",0)), "W/m²·K")
                    result_card("Total Area", float(res.get("A_req",0)), "m²")
                    result_card("U_dirty", float(res.get("U_dirty",0)), "W/m²·K")
            elif hx_type == "Double Pipe":
                c1, c2 = st.columns(2)
                with c1:
                    result_card("Number of Hairpins", float(res.get("N_hairpins",0)), "—")
                    result_card("h_inner (tube)", float(res.get("h_inner",0)), "W/m²·K")
                    result_card("Re inner", float(res.get("Re_inner",0)), "—")
                with c2:
                    result_card("h_annulus", float(res.get("h_ann",0)), "W/m²·K")
                    result_card("Re annulus", float(res.get("Re_ann",0)), "—")
                    result_card("Total Area", float(res.get("A_req",0)), "m²")
            elif hx_type == "Air Cooled (Fin Fan)":
                c1, c2 = st.columns(2)
                with c1:
                    result_card("Tube Count", float(res.get("N_tubes",0)), "—")
                    result_card("h_air (finned)", float(res.get("h_air_fin",0)), "W/m²·K")
                    result_card("Re air", float(res.get("Re_air",0)), "—")
                with c2:
                    result_card("h_process", float(res.get("h_proc",0)), "W/m²·K")
                    result_card("Air mass flow", float(res.get("mdot_air",0)), "kg/s")
                    result_card("Total Area", float(res.get("A_req",0)), "m²")
            elif hx_type == "Spiral":
                c1, c2 = st.columns(2)
                with c1:
                    result_card("Channel Length", float(res.get("L_channel",0)), "m")
                    result_card("Spiral Diameter", float(res.get("D_spiral",0)), "m")
                    result_card("h_hot", float(res.get("h_h",0)), "W/m²·K")
                with c2:
                    result_card("h_cold", float(res.get("h_c",0)), "W/m²·K")
                    result_card("Re hot", float(res.get("Re_h",0)), "—")
                    result_card("Total Area", float(res.get("A_req",0)), "m²")

        # ── TAB 3: PRESSURE DROP ────────────────────────────────────────────
        with tab_dp:
            cols = st.columns(4)
            if hx_type == "Shell & Tube":
                dp_items = [
                    ("ΔP Tube",       res.get("dP_tube_Pa",0)/1000,  "kPa"),
                    ("ΔP Shell",      res.get("dP_shell_Pa",0)/1000, "kPa"),
                    ("Pump Power Tube",  res.get("P_tube_kW",0),     "kW"),
                    ("Pump Power Shell", res.get("P_shell_kW",0),    "kW"),
                ]
            elif hx_type == "Plate & Frame":
                dp_items = [("ΔP Plate",res.get("dP_plate_Pa",0)/1000,"kPa")]
            elif hx_type == "Double Pipe":
                dp_items = [("ΔP Inner", res.get("dP_inner_Pa",0)/1000,"kPa"),
                             ("ΔP Annulus",res.get("dP_ann_Pa",0)/1000,"kPa")]
            elif hx_type == "Air Cooled (Fin Fan)":
                dp_items = [("ΔP Air",  res.get("dP_air_Pa",0)/1000, "kPa"),
                             ("Fan Power",res.get("P_fan_kW",0),      "kW")]
            else:  # Spiral
                dp_items = [("ΔP Hot",  res.get("dP_h_Pa",0)/1000,   "kPa"),
                             ("ΔP Cold", res.get("dP_c_Pa",0)/1000,   "kPa")]

            for i, (lbl, val, unit) in enumerate(dp_items):
                with cols[i % 4]:
                    result_card(lbl, float(val) if val else 0.0, unit)

            # ΔP allowable check
            if hx_type == "Shell & Tube":
                dp_t_kPa = res.get("dP_tube_Pa",0)/1000
                dp_s_kPa = res.get("dP_shell_Pa",0)/1000
                st.markdown(f"""
                <div class="{'info-box' if dp_t_kPa <= full_inp.get('dP_c_max',50) else 'warn-box'}">
                  Tube-side ΔP: {dp_t_kPa:.2f} kPa vs Allowable: {full_inp.get('dP_c_max',50):.1f} kPa —
                  {'✅ OK' if dp_t_kPa <= full_inp.get('dP_c_max',50) else '⚠ EXCEEDS LIMIT'}
                </div>
                <div class="{'info-box' if dp_s_kPa <= full_inp.get('dP_h_max',50) else 'warn-box'}">
                  Shell-side ΔP: {dp_s_kPa:.2f} kPa vs Allowable: {full_inp.get('dP_h_max',50):.1f} kPa —
                  {'✅ OK' if dp_s_kPa <= full_inp.get('dP_h_max',50) else '⚠ EXCEEDS LIMIT'}
                </div>""", unsafe_allow_html=True)

        # ── TAB 4: COST ─────────────────────────────────────────────────────
        with tab_cost:
            c1, c2, c3 = st.columns(3)
            with c1:
                result_card("Equipment Cost",
                            float(res.get("C_equip", equipment_cost_guthrie(res.get("A_req",10)))),
                            "USD")
            with c2:
                eq = res.get("C_equip", equipment_cost_guthrie(res.get("A_req",10)))
                result_card("Installed Cost", float(eq * 2), "USD")
            with c3:
                result_card("Required Area", float(res.get("A_req",0)), "m²")
            st.markdown("""
            <div class="info-box">
              📚 Cost correlation: Guthrie (1969), CEPCI 700 (2023 basis).
              Installed cost = 2.0 × equipment cost (Lang factor).
              Includes: foundation, piping, instrumentation, electrical, painting, insulation.
              Reference: Coulson &amp; Richardson Vol. 6, Chapter 6.
            </div>""", unsafe_allow_html=True)

        # ── TAB 5: CALCULATIONS ─────────────────────────────────────────────
        with tab_steps:
            show_steps(res.get("steps", []))

        # ═══════════════════════════════════════════════════════════════════
        # F.  INTERACTIVE GRAPHS (8 charts)
        # ═══════════════════════════════════════════════════════════════════
        section_header("📈", "Interactive Engineering Charts")

        g_tab1, g_tab2, g_tab3, g_tab4, g_tab5, g_tab6, g_tab7, g_tab8 = st.tabs([
            "🌡 Temp Profile", "📐 F-Factor", "⚡ ε-NTU",
            "🔧 Tube Count", "📊 Moody", "🔩 Shell f",
            "🔬 Colburn j_H", "📉 ΔP vs Flow"])

        with g_tab1:
            fig = graph_temperature_profile(
                full_inp["T1"], full_inp["T2"],
                full_inp["t1"], full_inp["t2"],
                res.get("L_m", 3.66))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="info-box">
              📚 Reference: Kern, D.Q. (1950) Process Heat Transfer, Chapter 3.<br>
              Temperature profile assumes plug flow and constant U along exchanger length.
            </div>""", unsafe_allow_html=True)

        with g_tab2:
            fig = graph_f_factor(res.get("P_val"), res.get("R_val"), n_passes=2)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div class="info-box">
              📌 Operating Point: P = {res.get('P_val',0):.3f},
              R = {res.get('R_val',0):.3f},
              F = {res.get('F',1.0):.4f}<br>
              📚 Reference: Bowman, Mueller &amp; Nagle (1940) Ind. Eng. Chem.
            </div>""", unsafe_allow_html=True)

        with g_tab3:
            fig = graph_eps_ntu(
                NTU_pt=res.get("NTU"),
                Cr_pt=res.get("Cr"),
                eps_pt=res.get("eps"))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div class="info-box">
              📌 Design Point: NTU = {res.get('NTU',0):.3f},
              Cᵣ = {res.get('Cr',0):.3f},
              ε = {res.get('eps',0):.4f} ({res.get('eps',0)*100:.1f}%)<br>
              📚 Reference: Kays &amp; London (1984) Compact Heat Exchangers, 3rd Ed.
            </div>""", unsafe_allow_html=True)

        with g_tab4:
            fig = graph_tube_count(
                N_tubes_pt=res.get("N_tubes"),
                Ds_mm_pt=res.get("Ds_m", 0) * 1000)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div class="info-box">
              📌 Design: N_tubes = {res.get('N_tubes',0)},
              D_shell = {res.get('Ds_m',0)*1000:.1f} mm<br>
              📚 Reference: TEMA Standards 9th Edition, Appendix (tube count tables).
            </div>""", unsafe_allow_html=True)

        with g_tab5:
            Re_t = res.get("Re_tube", 1e4)
            f_t  = darcy_friction(Re_t) if Re_t else 0.02
            fig  = graph_moody(Re_pt=Re_t, f_pt=f_t)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div class="info-box">
              📌 Tube-side: Re = {Re_t:.0f},  f = {f_t:.5f}<br>
              📚 Reference: Moody, L.F. (1944) Trans. ASME 66, p. 671.
              Colebrook-White equation used for turbulent rough pipe friction factor.
            </div>""", unsafe_allow_html=True)

        with g_tab6:
            Re_s = res.get("Re_shell", 1e4)
            f_s  = 0.5 * Re_s**(-0.2) if Re_s else 0.02
            fig  = graph_shell_friction(Re_shell_pt=Re_s, f_shell_pt=f_s)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div class="info-box">
              📌 Shell-side: Re_s = {Re_s:.0f},  f_s = {f_s:.5f}<br>
              📚 Reference: Kern, D.Q. (1950) Process Heat Transfer, shell-side ΔP method.
            </div>""", unsafe_allow_html=True)

        with g_tab7:
            Re_s = res.get("Re_shell", 1e4)
            jH   = res.get("j_H", 0.36 * Re_s**(-0.36)) if Re_s else 0.001
            fig  = graph_colburn_jH(Re_pt=Re_s, jH_pt=jH)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""<div class="info-box">
              📌 Shell-side: Re_s = {Re_s:.0f},  j_H = {jH:.6f}<br>
              📚 Reference: Colburn, A.P. (1933) Trans. AIChE 29, p. 174.
              j_H = h/(G·Cp) × (Cp·μ/k)^(2/3) — dimensionless heat transfer factor.
            </div>""", unsafe_allow_html=True)

        with g_tab8:
            fig = graph_dp_vs_flowrate(
                full_inp,
                res.get("dP_tube_Pa", res.get("dP_h_Pa", 10000)),
                full_inp.get("dP_c_max", 50) * 1000,
                side="Tube")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""<div class="info-box">
              📚 Reference: Darcy-Weisbach equation. Pressure drop scales as ṁ^1.8 in turbulent flow.
              Green dashed line = allowable ΔP limit. Vertical gold line = design flow rate.
            </div>""", unsafe_allow_html=True)

        # ═══════════════════════════════════════════════════════════════════
        # G.  REPORT DOWNLOADS
        # ═══════════════════════════════════════════════════════════════════
        section_header("📥", "Download Professional Reports")
        st.markdown("""<div class="info-box">
          Reports include: complete process conditions, all 33 calculation steps,
          detailed results tables, graph images, engineering references, and professional footer.
        </div>""", unsafe_allow_html=True)

        dcol1, dcol2, dcol3 = st.columns(3)
        with dcol1:
            try:
                pdf_bytes = generate_pdf_report(hx_type, full_inp, res)
                st.download_button(
                    label="🔴 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"HX_Design_{hx_type.replace(' ','_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True)
            except Exception as e:
                st.error(f"PDF error: {e}")

        with dcol2:
            try:
                word_bytes = generate_word_report(hx_type, full_inp, res)
                st.download_button(
                    label="🔵 Download Word Report",
                    data=word_bytes,
                    file_name=f"HX_Design_{hx_type.replace(' ','_')}.doc",
                    mime="application/msword",
                    use_container_width=True)
            except Exception as e:
                st.error(f"Word error: {e}")

        with dcol3:
            try:
                txt_str = generate_txt_report(hx_type, full_inp, res)
                st.download_button(
                    label="🟢 Download TXT Report",
                    data=txt_str.encode("utf-8"),
                    file_name=f"HX_Design_{hx_type.replace(' ','_')}.txt",
                    mime="text/plain",
                    use_container_width=True)
            except Exception as e:
                st.error(f"TXT error: {e}")

    # ═══════════════════════════════════════════════════════════════════════
    # H.  REFERENCES SECTION
    # ═══════════════════════════════════════════════════════════════════════
    section_header("📚", "Engineering References")
    with st.expander("📖 View Complete Reference Table", expanded=False):
        ref_data = {
            "Author": [
                "Kern, D.Q.", "TEMA Standards", "ASME",
                "Kays & London", "Bowman, Mueller & Nagle",
                "Dittus & Boelter", "Colburn, A.P.",
                "Darcy-Weisbach", "Crane Co.",
                "API", "ALFA LAVAL", "Coulson & Richardson",
                "Guthrie, K.M.", "Moody, L.F.",
            ],
            "Title": [
                "Process Heat Transfer", "9th Edition (2007)",
                "Boiler & PV Code Sec VIII",
                "Compact Heat Exchangers, 3rd Ed.",
                "Ind. Eng. Chem. 32, 926–940",
                "Univ. California Publ. Eng. 2(13)",
                "Trans. AIChE 29, 174–210",
                "Hydraulic equation (classical)",
                "Technical Paper No. 410",
                "Standard 661 (Air-cooled HX)",
                "PHE Design Handbook",
                "Chemical Eng. Design Vol.6",
                "Chemical Engineering, Mar 1969",
                "Trans. ASME 66, 671–684",
            ],
            "Year": [
                "1950","2007","—","1984","1940",
                "1930","1933","—","—","—","—","1999","1969","1944"],
            "Application": [
                "Shell-side Kern method, LMTD",
                "Mechanical design, tube counts, baffle standards",
                "Pressure vessel design rules",
                "ε-NTU method, effectiveness correlations",
                "F-correction factors for multipass",
                "Tube-side heat transfer (turbulent)",
                "Shell-side j_H factor method",
                "Pressure drop in pipes (tube/shell side)",
                "Minor losses, valve/fitting Kv factors",
                "Air-cooled heat exchanger design",
                "Plate heat exchanger design guidance",
                "Equipment sizing, cost estimation",
                "Equipment cost correlations (Guthrie method)",
                "Darcy friction factor chart (turbulent/laminar)",
            ],
        }
        import pandas as pd
        st.dataframe(pd.DataFrame(ref_data), use_container_width=True, hide_index=True)

#     # ========== FOOTER ==========
# st.markdown("""
# <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #0f3443, #1a5a6e); border-radius: 10px; margin-top: 2rem;">
# <p style="margin: 0;">
# <span style="color: #2ecc71; font-weight: bold;">🔬</span>
#     <span style="color: #2ecc71;"> Developed by </span>
#         <span style="color: white; font-weight: bold;">ZUNAIR SHAHZAD</span>
#         <span style="color: #FFD700;"> | </span>
#             <span style="color: #FFD700;">Chemical Engineering</span>
#                 <span style="color: #FFD700;"> | </span>
#                     <span style="color: #FFD700;">UET Lahore</span>
#                         </p>
#                         </div>
#                         """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Entry point (when run directly for testing)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    show_heat_exchanger()
