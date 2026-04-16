import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_pressure_drop_phase2():
    # Custom CSS for better styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

        * { font-family: 'Sora', sans-serif; }

        .main-header {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 1.8rem;
        }
        .main-header p {
            color: #34e89e;
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
        }
        .section-header {
            background: linear-gradient(135deg, #0f3443, #1a5a6e);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin: 1rem 0 0.5rem 0;
        }
        .section-header h3 {
            color: #34e89e;
            margin: 0;
            font-size: 1.2rem;
        }
        .result-box {
            background: linear-gradient(135deg, #0f2027, #203a43);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #34e89e;
        }
        .result-number {
            font-size: 2rem;
            font-weight: bold;
            color: #34e89e;
            font-family: 'JetBrains Mono', monospace;
        }
        .dp-unit-box {
            background: linear-gradient(135deg, #0f2027, #203a43);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #2a5298;
            margin: 4px;
        }
        .dp-unit-number {
            font-size: 1.6rem;
            font-weight: bold;
            color: #34e89e;
            font-family: 'JetBrains Mono', monospace;
        }
        .dp-unit-label {
            color: #aaa;
            font-size: 0.85rem;
            margin-top: 4px;
        }
        .friction-box {
            background: linear-gradient(135deg, #0f2027, #203a43);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            border: 1px solid #f39c12;
            margin: 0.5rem 0;
        }
        .friction-number {
            font-size: 2.2rem;
            font-weight: bold;
            color: #f39c12;
            font-family: 'JetBrains Mono', monospace;
        }
        .head-box {
            background: linear-gradient(135deg, #0f2027, #203a43);
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #9b59b6;
            text-align: center;
        }
        .head-number {
            font-size: 1.8rem;
            font-weight: bold;
            color: #9b59b6;
            font-family: 'JetBrains Mono', monospace;
        }
        .power-box {
            background: linear-gradient(135deg, #0f2027, #203a43);
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #e74c3c;
            text-align: center;
        }
        .power-number {
            font-size: 1.4rem;
            font-weight: bold;
            color: #e74c3c;
            font-family: 'JetBrains Mono', monospace;
        }
        .flowrate-bar {
            background: linear-gradient(135deg, #0f2027, #203a43);
            padding: 0.7rem 1.2rem;
            border-radius: 8px;
            border: 1px solid #1abc9c;
            margin-top: 0.5rem;
            text-align: center;
        }
        .ref-table th { background: #1a3a5c; color: #34e89e; }
        </style>
    """, unsafe_allow_html=True)

    # Main Header
    st.markdown("""
        <div class="main-header">
            <h1>📉 Pressure Drop & Head Loss Calculator</h1>
            <p>Darcy-Weisbach Equation: ΔP = f × (L/D) × (ρv²/2)</p>
        </div>
    """, unsafe_allow_html=True)

    # ========== WHAT CAN YOU CALCULATE? ==========
    with st.expander("ℹ️ What can you calculate here?", expanded=True):
        st.markdown("""
        | # | Calculation | Description |
        |---|--------------|-------------|
        | 1 | **Pressure Drop (ΔP)** | Pressure loss due to friction in the pipe |
        | 2 | **Head Loss (h_f)** | Pressure drop converted to meters of fluid column |
        | 3 | **Pump Power** | Power required to overcome pressure drop |
        | 4 | **Reynolds Number (Re)** | Determines flow type: Laminar, Transitional, or Turbulent |
        | 5 | **Friction Factor (f)** | Pipe roughness effect on pressure drop |
        """)

    st.markdown("---")

    # ========== MODE SELECTION ==========
    st.markdown('<div class="section-header"><h3>📌 Select Calculation Mode</h3></div>', unsafe_allow_html=True)
    mode = st.radio(
        "",
        [
            "🔬 Find Pressure Drop (ΔP) — Most Common",
            "⚡ Find Velocity (v) — When ΔP is Known",
            "📏 Find Diameter (D) — Pipe Sizing",
            "📐 Find Length (L) — Maximum Pipe Length"
        ],
        help="Choose what you want to calculate based on available inputs"
    )

    st.markdown("---")

    # ========== INPUT PARAMETERS ==========
    st.markdown('<div class="section-header"><h3>📥 Input Parameters</h3></div>', unsafe_allow_html=True)
    st.caption("These are the values you need to provide. Each parameter affects the pressure drop.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p style="color: #ff6666; font-weight: bold;">📐 Pipe Geometry</p>', unsafe_allow_html=True)
        L = st.number_input("Pipe Length (L)", value=100.0, step=10.0, help="Meters (m) — Longer pipe = more pressure drop")
        D = st.number_input("Pipe Diameter (D)", value=0.1, step=0.01, help="Meters (m) — Smaller diameter = more pressure drop")
        epsilon = st.number_input("Pipe Roughness (ε)", value=0.05, step=0.01, help="mm (Steel = 0.05) — Rougher pipe = more friction")

        st.markdown('<p style="color: #ff6666; font-weight: bold; margin-top: 1rem;">🌊 Fluid Properties</p>', unsafe_allow_html=True)
        rho = st.number_input("Fluid Density (ρ)", value=1000.0, step=10.0, help="kg/m³ — Water = 1000, Oil ≈ 800-900")
        mu = st.number_input("Fluid Viscosity (μ)", value=0.001, step=0.0001, format="%.4f", help="Pa·s — Water = 0.001, Oil ≈ 0.01-0.1")

    with col2:
        st.markdown('<p style="color: #ff6666; font-weight: bold;">💨 Flow Conditions</p>', unsafe_allow_html=True)
        v = st.number_input("Flow Velocity (v)", value=2.0, step=0.1, help="m/s — Higher velocity = more pressure drop")
        g = 9.81
        st.caption(f"⚡ Gravity (g) = {g} m/s² (constant)")

        st.markdown('<p style="color: #ff6666; font-weight: bold; margin-top: 1rem;">🔧 Optional: Minor Losses</p>', unsafe_allow_html=True)
        st.caption("(Coming in Phase 4) — Elbows, valves, fittings add extra pressure drop")

    # ========== CALCULATE BUTTON ==========
    st.markdown("---")
    if st.button("🔬 Calculate Pressure Drop", type="primary", use_container_width=True):

        # ========== INPUT VALIDATION ==========
        errors = []
        if L <= 0:
            errors.append("❌ Pipe Length (L) must be greater than 0")
        if D <= 0:
            errors.append("❌ Pipe Diameter (D) must be greater than 0")
        if rho <= 0:
            errors.append("❌ Fluid Density (ρ) must be greater than 0")
        if mu <= 0:
            errors.append("❌ Fluid Viscosity (μ) must be greater than 0")
        if v <= 0:
            errors.append("❌ Flow Velocity (v) must be greater than 0")

        if errors:
            for err in errors:
                st.error(err)
        else:
            # ========== CALCULATIONS ==========
            # 1. Reynolds Number
            Re = (rho * v * D) / mu

            # 2. Flow Type
            if Re < 2000:
                flow_type = "🟢 LAMINAR FLOW"
                flow_desc = "Smooth, orderly flow. Low friction. Good for viscous fluids."
                flow_color = "#2ecc71"
            elif Re < 4000:
                flow_type = "🟡 TRANSITIONAL FLOW"
                flow_desc = "Unstable flow. May switch between laminar and turbulent."
                flow_color = "#f39c12"
            else:
                flow_type = "🔴 TURBULENT FLOW"
                flow_desc = "Chaotic flow with eddies. Higher friction but better mixing."
                flow_color = "#e74c3c"

            # 3. Friction Factor
            epsilon_m = epsilon / 1000.0  # mm → meters
            relative_roughness = epsilon_m / D

            if Re < 2000:
                f = 64 / Re
                f_ref = "Hagen-Poiseuille (1839-1840) — Laminar flow"
            elif Re >= 4000:
                # Swamee-Jain
                f = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (Re ** 0.9))) ** 2
                f_ref = "Swamee-Jain (1976) — Turbulent flow"
            else:
                # Linear interpolation
                f_lam = 64 / 2000
                f_turb = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (4000 ** 0.9))) ** 2
                t = (Re - 2000) / (4000 - 2000)
                f = f_lam + t * (f_turb - f_lam)
                f_ref = "Linear interpolation between Laminar & Turbulent"

            # 4. Pressure Drop (Darcy-Weisbach)
            dP_Pa = f * (L / D) * (rho * v ** 2 / 2)
            dP_kPa = dP_Pa / 1000
            dP_bar = dP_Pa / 100000
            dP_psi = dP_Pa * 0.000145038

            # 5. Head Loss
            h_f = dP_Pa / (rho * g)

            # 6. Flow Rate
            A = math.pi * D ** 2 / 4
            Q = v * A
            Q_Ls = Q * 1000  # L/s

            # 7. Pump Power (η = 0.7)
            eta = 0.7
            P_W = (dP_Pa * Q) / eta
            P_kW = P_W / 1000
            P_HP = P_kW * 1.341

            # ========== RESULTS DISPLAY ==========

            # --- Reynolds Number & Flow Type ---
            st.markdown('<div class="section-header"><h3>📊 Reynolds Number & Flow Type</h3></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                    <div class="result-box">
                        <p style="margin:0; font-size:0.85rem; color:#aaa;">🔢 REYNOLDS NUMBER</p>
                        <p class="result-number">{Re:,.0f}</p>
                        <p style="margin:0; font-size:0.75rem; color:#aaa;">Re = ρ × v × D / μ</p>
                    </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                    <div class="result-box" style="border-color:{flow_color};">
                        <p style="margin:0; font-size:0.85rem; color:#aaa;">🎯 FLOW TYPE</p>
                        <p class="result-number" style="color:{flow_color}; font-size:1.3rem;">{flow_type}</p>
                        <p style="margin:0; font-size:0.78rem; color:#ccc;">{flow_desc}</p>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- Friction Factor ---
            st.markdown('<div class="section-header"><h3>🔧 Friction Factor (f)</h3></div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="friction-box">
                    <p style="margin:0; font-size:0.85rem; color:#aaa;">DARCY FRICTION FACTOR</p>
                    <p class="friction-number">f = {f:.6f}</p>
                    <p style="margin:0; font-size:0.8rem; color:#ccc;">📚 Reference: {f_ref}</p>
                    <p style="margin:0; font-size:0.78rem; color:#aaa; margin-top:4px;">Relative Roughness (ε/D) = {relative_roughness:.6f}</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- Pressure Drop ---
            st.markdown('<div class="section-header"><h3>📉 Pressure Drop (ΔP)</h3></div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            units = [
                (c1, f"{dP_Pa:,.1f}", "Pa"),
                (c2, f"{dP_kPa:,.3f}", "kPa"),
                (c3, f"{dP_bar:.5f}", "bar"),
                (c4, f"{dP_psi:.4f}", "psi"),
            ]
            for col, val, unit in units:
                with col:
                    st.markdown(f"""
                        <div class="dp-unit-box">
                            <p class="dp-unit-number">{val}</p>
                            <p class="dp-unit-label">{unit}</p>
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- Head Loss & Pump Power ---
            st.markdown('<div class="section-header"><h3>⚡ Head Loss & Pump Power</h3></div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                    <div class="head-box">
                        <p style="margin:0; font-size:0.85rem; color:#aaa;">📏 HEAD LOSS</p>
                        <p class="head-number">{h_f:.3f} meters</p>
                        <p style="margin:0; font-size:0.75rem; color:#aaa;">h_f = ΔP / (ρ × g) — Bernoulli (1738)</p>
                    </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                    <div class="power-box">
                        <p style="margin:0; font-size:0.85rem; color:#aaa;">⚡ PUMP POWER (η = 70%)</p>
                        <p class="power-number">{P_W:,.1f} W &nbsp;|&nbsp; {P_kW:.3f} kW &nbsp;|&nbsp; {P_HP:.3f} HP</p>
                        <p style="margin:0; font-size:0.75rem; color:#aaa;">Power = (ΔP × Q) / η</p>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="flowrate-bar">
                    💡 <strong style="color:#1abc9c;">Flow Rate (Q):</strong>
                    <span style="color:white;"> {Q:.5f} m³/s</span>
                    &nbsp;|&nbsp;
                    <span style="color:#34e89e;"> {Q_Ls:.3f} L/s</span>
                    &nbsp;&nbsp;
                    <span style="color:#aaa; font-size:0.8rem;">Q = v × A,&nbsp; A = π × D² / 4</span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ========== GRAPHS ==========
            st.markdown('<div class="section-header"><h3>📈 Visual Analysis</h3></div>', unsafe_allow_html=True)

            tab1, tab2, tab3, tab4 = st.tabs([
                "🗺️ Moody Chart",
                "📉 ΔP vs Flow Rate",
                "📏 ΔP vs Diameter",
                "🌊 Head Loss vs Velocity"
            ])

            # ---- GRAPH 1: Moody Chart ----
            with tab1:
                st.caption("Interactive Moody Chart — Red dot shows your current operating point.")
                Re_range = np.logspace(3, 8, 500)
                eD_values = [0.00001, 0.0001, 0.001, 0.005, 0.01, 0.02, 0.05]
                colors_moody = ["#3498db","#2ecc71","#f39c12","#e74c3c","#9b59b6","#1abc9c","#e67e22"]

                fig1 = go.Figure()

                # Laminar line
                Re_lam = np.linspace(600, 2000, 100)
                fig1.add_trace(go.Scatter(
                    x=Re_lam, y=64/Re_lam,
                    mode='lines', name='Laminar (f=64/Re)',
                    line=dict(color='#34e89e', width=2.5, dash='dash')
                ))

                # Turbulent curves
                for eD, clr in zip(eD_values, colors_moody):
                    f_vals = []
                    for r in Re_range:
                        if r < 4000:
                            f_vals.append(None)
                        else:
                            fv = 0.25 / (math.log10(eD / 3.7 + 5.74 / (r ** 0.9))) ** 2
                            f_vals.append(fv)
                    fig1.add_trace(go.Scatter(
                        x=Re_range, y=f_vals,
                        mode='lines', name=f'ε/D = {eD}',
                        line=dict(color=clr, width=1.5)
                    ))

                # User point
                fig1.add_trace(go.Scatter(
                    x=[Re], y=[f],
                    mode='markers+text',
                    name='Your Point',
                    marker=dict(color='red', size=14, symbol='circle', line=dict(color='white', width=2)),
                    text=[f"  Re={Re:,.0f}<br>  f={f:.5f}"],
                    textposition='top right',
                    textfont=dict(color='red', size=11)
                ))

                # Dashed lines from point
                fig1.add_shape(type='line', x0=Re, x1=Re, y0=0.008, y1=f,
                               line=dict(color='red', dash='dot', width=1))
                fig1.add_shape(type='line', x0=1e3, x1=Re, y0=f, y1=f,
                               line=dict(color='red', dash='dot', width=1))

                fig1.update_layout(
                    title=dict(text="🗺️ Moody Chart — Friction Factor vs Reynolds Number", font=dict(color='#34e89e', size=14)),
                    xaxis=dict(type='log', title='Reynolds Number (Re)', gridcolor='#1a3a5c', color='white',
                               range=[3, 8]),
                    yaxis=dict(type='log', title='Friction Factor (f)', gridcolor='#1a3a5c', color='white',
                               range=[-2.1, -0.9]),
                    paper_bgcolor='#0f2027',
                    plot_bgcolor='#0f2027',
                    font=dict(color='white'),
                    legend=dict(bgcolor='#1a3a5c', bordercolor='#34e89e', borderwidth=1),
                    height=500
                )
                st.plotly_chart(fig1, use_container_width=True)
                st.caption("📚 Reference: Lewis Ferry Moody (1944) — ASME Transactions")

            # ---- GRAPH 2: ΔP vs Flow Rate ----
            with tab2:
                Q_range = np.linspace(0.001, Q * 3, 200)
                v_range = Q_range / A
                Re_range2 = rho * v_range * D / mu

                dP_range = []
                for vi, Rei in zip(v_range, Re_range2):
                    if Rei < 2000:
                        fi = 64 / Rei
                    elif Rei >= 4000:
                        fi = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (Rei ** 0.9))) ** 2
                    else:
                        f_l = 64 / 2000
                        f_t = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (4000 ** 0.9))) ** 2
                        t = (Rei - 2000) / 2000
                        fi = f_l + t * (f_t - f_l)
                    dP_range.append(fi * (L / D) * (rho * vi ** 2 / 2))

                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=Q_range, y=dP_range,
                    mode='lines', name='ΔP Curve',
                    line=dict(color='#34e89e', width=2.5),
                    fill='tozeroy', fillcolor='rgba(52,232,158,0.08)'
                ))
                fig2.add_trace(go.Scatter(
                    x=[Q], y=[dP_Pa],
                    mode='markers+text',
                    name='Current Point',
                    marker=dict(color='red', size=12, symbol='star'),
                    text=[f"  Q={Q:.4f} m³/s<br>  ΔP={dP_Pa:,.1f} Pa"],
                    textposition='top right',
                    textfont=dict(color='red', size=10)
                ))
                fig2.update_layout(
                    title=dict(text="📉 Pressure Drop vs Flow Rate", font=dict(color='#34e89e', size=14)),
                    xaxis=dict(title='Flow Rate Q (m³/s)', gridcolor='#1a3a5c', color='white'),
                    yaxis=dict(title='Pressure Drop ΔP (Pa)', gridcolor='#1a3a5c', color='white'),
                    paper_bgcolor='#0f2027', plot_bgcolor='#0f2027',
                    font=dict(color='white'), height=420,
                    legend=dict(bgcolor='#1a3a5c')
                )
                st.plotly_chart(fig2, use_container_width=True)

            # ---- GRAPH 3: ΔP vs Diameter ----
            with tab3:
                D_range = np.linspace(0.01, D * 4, 200)
                dP_D = []
                for Di in D_range:
                    Rei = rho * v * Di / mu
                    eD_i = epsilon_m / Di
                    if Rei < 2000:
                        fi = 64 / Rei
                    elif Rei >= 4000:
                        fi = 0.25 / (math.log10(eD_i / 3.7 + 5.74 / (Rei ** 0.9))) ** 2
                    else:
                        f_l = 64 / 2000
                        f_t = 0.25 / (math.log10(eD_i / 3.7 + 5.74 / (4000 ** 0.9))) ** 2
                        t = (Rei - 2000) / 2000
                        fi = f_l + t * (f_t - f_l)
                    dP_D.append(fi * (L / Di) * (rho * v ** 2 / 2))

                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=D_range, y=dP_D,
                    mode='lines', name='ΔP vs D',
                    line=dict(color='#9b59b6', width=2.5),
                    fill='tozeroy', fillcolor='rgba(155,89,182,0.08)'
                ))
                fig3.add_trace(go.Scatter(
                    x=[D], y=[dP_Pa],
                    mode='markers+text',
                    name='Current Point',
                    marker=dict(color='red', size=12, symbol='star'),
                    text=[f"  D={D} m<br>  ΔP={dP_Pa:,.1f} Pa"],
                    textposition='top right',
                    textfont=dict(color='red', size=10)
                ))
                fig3.update_layout(
                    title=dict(text="📏 Pressure Drop vs Pipe Diameter", font=dict(color='#9b59b6', size=14)),
                    xaxis=dict(title='Diameter D (m)', gridcolor='#1a3a5c', color='white'),
                    yaxis=dict(title='Pressure Drop ΔP (Pa)', gridcolor='#1a3a5c', color='white'),
                    paper_bgcolor='#0f2027', plot_bgcolor='#0f2027',
                    font=dict(color='white'), height=420,
                    legend=dict(bgcolor='#1a3a5c')
                )
                st.plotly_chart(fig3, use_container_width=True)

            # ---- GRAPH 4: Head Loss vs Velocity ----
            with tab4:
                v_arr = np.linspace(0.1, v * 3, 200)
                hf_arr = []
                for vi in v_arr:
                    Rei = rho * vi * D / mu
                    if Rei < 2000:
                        fi = 64 / Rei
                    elif Rei >= 4000:
                        fi = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (Rei ** 0.9))) ** 2
                    else:
                        f_l = 64 / 2000
                        f_t = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / (4000 ** 0.9))) ** 2
                        t = (Rei - 2000) / 2000
                        fi = f_l + t * (f_t - f_l)
                    dPi = fi * (L / D) * (rho * vi ** 2 / 2)
                    hf_arr.append(dPi / (rho * g))

                fig4 = go.Figure()
                fig4.add_trace(go.Scatter(
                    x=v_arr, y=hf_arr,
                    mode='lines', name='Head Loss Curve',
                    line=dict(color='#f39c12', width=2.5),
                    fill='tozeroy', fillcolor='rgba(243,156,18,0.08)'
                ))
                fig4.add_trace(go.Scatter(
                    x=[v], y=[h_f],
                    mode='markers+text',
                    name='Current Point',
                    marker=dict(color='red', size=12, symbol='star'),
                    text=[f"  v={v} m/s<br>  h_f={h_f:.3f} m"],
                    textposition='top right',
                    textfont=dict(color='red', size=10)
                ))
                fig4.update_layout(
                    title=dict(text="🌊 Head Loss vs Flow Velocity", font=dict(color='#f39c12', size=14)),
                    xaxis=dict(title='Velocity v (m/s)', gridcolor='#1a3a5c', color='white'),
                    yaxis=dict(title='Head Loss h_f (m)', gridcolor='#1a3a5c', color='white'),
                    paper_bgcolor='#0f2027', plot_bgcolor='#0f2027',
                    font=dict(color='white'), height=420,
                    legend=dict(bgcolor='#1a3a5c')
                )
                st.plotly_chart(fig4, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ========== REFERENCES ==========
            with st.expander("📚 Scientific References & Equations Used"):
                st.markdown("""
                | Formula | Reference | Year |
                |---------|-----------|------|
                | **Darcy-Weisbach** ΔP = f(L/D)(ρv²/2) | Henry Darcy, Julius Weisbach | 1845–1850 |
                | **Reynolds Number** Re = ρvD/μ | Osborne Reynolds | 1883 |
                | **Hagen-Poiseuille** f = 64/Re | Gotthilf Hagen, Jean Poiseuille | 1839–1840 |
                | **Swamee-Jain** Explicit f for turbulent | P.K. Swamee, A.K. Jain | 1976 |
                | **Moody Chart** f vs Re diagram | Lewis Ferry Moody | 1944 |
                | **Bernoulli** h_f = ΔP/(ρg) | Daniel Bernoulli | 1738 |
                """)

    # ========== FOOTER ==========
    st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #0f3443, #1a5a6e); border-radius: 10px; margin-top: 2rem;">
            <p style="margin: 0;">
                <span style="color: #2ecc71; font-weight: bold;">🔬</span>
                <span style="color: #2ecc71;"> Developed by </span>
                <span style="color: white; font-weight: bold;">ZUNAIR SHAHZAD</span>
                <span style="color: #FFD700;"> | </span>
                <span style="color: #FFD700;">Chemical Engineering</span>
                <span style="color: #FFD700;"> | </span>
                <span style="color: #FFD700;">UET Lahore</span>
            </p>
        </div>
    """, unsafe_allow_html=True)
