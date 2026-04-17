import streamlit as st
import pandas as pd

def show_formulas():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
        * { font-family: 'Sora', sans-serif; }
        .main-header {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .main-header h1 { color: white; margin: 0; font-size: 2.2rem; }
        .main-header p { color: #34e89e; margin: 0.5rem 0 0 0; }
        .category-card {
            background: #0f2027;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid rgba(52,232,158,0.2);
            margin-bottom: 1rem;
        }
        .category-card:hover {
            transform: translateY(-8px);
            border-color: #34e89e;
            box-shadow: 0 15px 35px rgba(52,232,158,0.2);
        }
        .category-icon { font-size: 3rem; margin-bottom: 0.5rem; }
        .category-title { font-size: 1.3rem; font-weight: bold; margin: 0.5rem 0; }
        .category-desc { font-size: 0.8rem; color: rgba(255,255,255,0.6); }
        .formula-card {
            background: #0f2027;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-left: 4px solid;
            transition: all 0.2s ease;
        }
        .formula-card:hover { transform: translateX(5px); background: #1a2a35; }
        .formula-name { font-weight: bold; font-size: 1rem; }
        .formula-equation {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #34e89e;
            margin-top: 0.25rem;
        }
        .detail-header {
            background: linear-gradient(135deg, #0f3443, #1a5a6e);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        }
        .detail-header h2 { color: white; margin: 0; }
        .equation-box {
            background: #0a1628;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
            border: 1px solid #34e89e;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if "formulas_view" not in st.session_state:
        st.session_state.formulas_view = "dashboard"
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "selected_formula" not in st.session_state:
        st.session_state.selected_formula = None
    
    # Formula Database
    formulas = {
        "Fluid Flow": {
            "color": "#3498db", "icon": "🔵",
            "formulas": [
                {"name": "Reynolds Number", "eq": r"Re = \frac{\rho v D}{\mu}", "desc": "Determines flow regime"},
                {"name": "Darcy-Weisbach", "eq": r"\Delta P = f \frac{L}{D} \frac{\rho v^2}{2}", "desc": "Pressure drop due to friction"},
                {"name": "Bernoulli's Equation", "eq": r"P_1 + \frac{1}{2}\rho v_1^2 + \rho g z_1 = P_2 + \frac{1}{2}\rho v_2^2 + \rho g z_2", "desc": "Energy conservation"},
                {"name": "Hagen-Poiseuille", "eq": r"\Delta P = \frac{128 \mu L Q}{\pi D^4}", "desc": "Laminar flow pressure drop"},
                {"name": "Fanning Friction Factor", "eq": r"f = \frac{\Delta P}{\frac{1}{2}\rho v^2 \frac{L}{D}}", "desc": "Friction factor correlation"},
                {"name": "Pump Power", "eq": r"P = \frac{\rho g Q H}{\eta}", "desc": "Pump power requirement"},
                {"name": "NPSH Available", "eq": r"NPSH_a = \frac{P_s - P_v}{\rho g} + \frac{v^2}{2g} - h_f", "desc": "Net Positive Suction Head"},
                {"name": "Orifice Flow", "eq": r"Q = C_d A_o \sqrt{\frac{2\Delta P}{\rho}}", "desc": "Flow through orifice plate"},
                {"name": "Venturi Meter", "eq": r"Q = C_d \frac{\pi D^2}{4} \sqrt{\frac{2\Delta P}{\rho(1-\beta^4)}}", "desc": "Venturi flow measurement"},
                {"name": "Pitot Tube", "eq": r"v = \sqrt{\frac{2\Delta P}{\rho}}", "desc": "Velocity measurement"},
                {"name": "Minor Losses", "eq": r"h_L = K \frac{v^2}{2g}", "desc": "Losses in fittings and valves"},
                {"name": "Mach Number", "eq": r"Ma = \frac{v}{c}", "desc": "Compressibility indicator"},
                {"name": "Speed of Sound", "eq": r"c = \sqrt{\frac{\gamma R T}{M}}", "desc": "Sound velocity in gas"},
                {"name": "Colebrook Equation", "eq": r"\frac{1}{\sqrt{f}} = -2\log\left(\frac{\epsilon}{3.7D} + \frac{2.51}{Re\sqrt{f}}\right)", "desc": "Turbulent friction factor"},
                {"name": "Swamee-Jain", "eq": r"f = \frac{0.25}{\left[\log\left(\frac{\epsilon}{3.7D} + \frac{5.74}{Re^{0.9}}\right)\right]^2}", "desc": "Explicit friction factor"},
                {"name": "Continuity Equation", "eq": r"\rho_1 A_1 v_1 = \rho_2 A_2 v_2", "desc": "Mass conservation"},
                {"name": "Hydraulic Diameter", "eq": r"D_h = \frac{4A}{P}", "desc": "Non-circular ducts"},
                {"name": "Friction Velocity", "eq": r"v_* = v \sqrt{\frac{f}{8}}", "desc": "Shear velocity"},
                {"name": "Laminar Profile", "eq": r"u(r) = 2v\left[1 - \left(\frac{r}{R}\right)^2\right]", "desc": "Parabolic velocity profile"},
                {"name": "Turbulent Profile", "eq": r"u(r) = v_{max}\left(1 - \frac{r}{R}\right)^{1/n}", "desc": "Power law velocity profile"}
            ]
        },
        "Heat Transfer": {
            "color": "#e74c3c", "icon": "🔴",
            "formulas": [
                {"name": "Fourier's Law", "eq": r"q = -k \frac{dT}{dx}", "desc": "Heat conduction"},
                {"name": "Newton's Law of Cooling", "eq": r"q = h(T_s - T_\infty)", "desc": "Convection"},
                {"name": "Stefan-Boltzmann Law", "eq": r"q = \epsilon \sigma (T_s^4 - T_{surr}^4)", "desc": "Thermal radiation"},
                {"name": "Overall HTC", "eq": r"\frac{1}{U} = \frac{1}{h_i} + \frac{\Delta x}{k} + \frac{1}{h_o}", "desc": "Overall coefficient"},
                {"name": "LMTD Method", "eq": r"Q = U A \Delta T_{lm}", "desc": "Heat exchanger sizing"},
                {"name": "ε-NTU Method", "eq": r"\epsilon = \frac{Q}{Q_{max}}", "desc": "Effectiveness"},
                {"name": "Dittus-Boelter", "eq": r"Nu = 0.023 Re^{0.8} Pr^{n}", "desc": "Turbulent flow"},
                {"name": "Prandtl Number", "eq": r"Pr = \frac{C_p \mu}{k}", "desc": "Momentum/thermal diffusivity"},
                {"name": "Nusselt Number", "eq": r"Nu = \frac{hL}{k}", "desc": "Convective/conduction"},
                {"name": "Grashof Number", "eq": r"Gr = \frac{g \beta (T_s - T_\infty) L^3}{\nu^2}", "desc": "Natural convection"},
                {"name": "Rayleigh Number", "eq": r"Ra = Gr \cdot Pr", "desc": "Buoyancy-driven flow"},
                {"name": "Biot Number", "eq": r"Bi = \frac{hL}{k}", "desc": "Internal/external resistance"},
                {"name": "Fourier Number", "eq": r"Fo = \frac{\alpha t}{L^2}", "desc": "Transient conduction"},
                {"name": "Fin Efficiency", "eq": r"\eta_f = \frac{\tanh(mL)}{mL}", "desc": "Extended surface"},
                {"name": "Log Mean Temperature Difference", "eq": r"\Delta T_{lm} = \frac{(T_1-t_2) - (T_2-t_1)}{\ln\frac{T_1-t_2}{T_2-t_1}}", "desc": "Counter-current LMTD"}
            ]
        },
        "Mass Transfer": {
            "color": "#2ecc71", "icon": "🟢",
            "formulas": [
                {"name": "Fick's First Law", "eq": r"J = -D_{AB} \frac{dC_A}{dx}", "desc": "Steady-state diffusion"},
                {"name": "Fick's Second Law", "eq": r"\frac{\partial C}{\partial t} = D \frac{\partial^2 C}{\partial x^2}", "desc": "Unsteady diffusion"},
                {"name": "Mass Transfer Coefficient", "eq": r"N_A = k_L (C_{Ai} - C_A)", "desc": "Convective mass transfer"},
                {"name": "Sherwood Number", "eq": r"Sh = \frac{k L}{D_{AB}}", "desc": "Mass transfer analog of Nu"},
                {"name": "Schmidt Number", "eq": r"Sc = \frac{\mu}{\rho D_{AB}}", "desc": "Momentum/diffusivity"},
                {"name": "Stanton Number", "eq": r"St_m = \frac{k}{v} Sc^{2/3}", "desc": "Mass transfer Stanton"},
                {"name": "Chilton-Colburn Analogy", "eq": r"j_D = \frac{k}{v} Sc^{2/3} = \frac{f}{2}", "desc": "Momentum/mass analogy"},
                {"name": "Two-Film Theory", "eq": r"\frac{1}{K_G} = \frac{1}{k_G} + \frac{1}{k_L H}", "desc": "Gas-liquid interface"},
                {"name": "Penetration Theory", "eq": r"k_L = \sqrt{\frac{4D_{AB}}{\pi t}}", "desc": "Unsteady diffusion"},
                {"name": "McCabe-Thiele", "eq": r"y = \frac{R}{R+1}x + \frac{x_D}{R+1}", "desc": "Distillation operating line"},
                {"name": "Kremser Equation", "eq": r"\frac{y_{N+1}-y_1}{y_{N+1}-y_1^*} = \frac{A^{N+1}-A}{A^{N+1}-1}", "desc": "Absorption"},
                {"name": "HTU-NTU Method", "eq": r"Z = H_G \cdot N_G + H_L \cdot N_L", "desc": "Packed column height"},
                {"name": "Height of Transfer Unit", "eq": r"H_G = \frac{G}{k_G a P}", "desc": "Gas phase HTU"},
                {"name": "Number of Transfer Units", "eq": r"N_G = \int \frac{dy}{y - y^*}", "desc": "Gas phase NTU"}
            ]
        },
        "Reactor Design": {
            "color": "#f39c12", "icon": "🟡",
            "formulas": [
                {"name": "Batch Reactor", "eq": r"t = \int_0^X \frac{dX}{-r_A}", "desc": "Batch design equation"},
                {"name": "CSTR Design", "eq": r"\tau = \frac{V}{v_0} = \frac{X}{-r_A}", "desc": "CSTR design"},
                {"name": "PFR Design", "eq": r"\tau = \int_0^X \frac{dX}{-r_A}", "desc": "Plug flow reactor"},
                {"name": "Space Time", "eq": r"\tau = \frac{V}{v_0}", "desc": "Residence time"},
                {"name": "Arrhenius Equation", "eq": r"k = A e^{-E_a/RT}", "desc": "Temperature dependence"},
                {"name": "Rate Law", "eq": r"-r_A = k C_A^n", "desc": "Power law kinetics"},
                {"name": "Conversion", "eq": r"X = \frac{N_{A0} - N_A}{N_{A0}}", "desc": "Fractional conversion"},
                {"name": "Van't Hoff Equation", "eq": r"\frac{d \ln K}{dT} = \frac{\Delta H_R}{RT^2}", "desc": "Temperature on equilibrium"},
                {"name": "Thiele Modulus", "eq": r"\phi = L \sqrt{\frac{k}{D_e}}", "desc": "Catalyst effectiveness"},
                {"name": "Damköhler Number", "eq": r"Da = \frac{k C_A^{n-1} V}{v_0}", "desc": "Reaction/flow rate"},
                {"name": "Selectivity", "eq": r"S = \frac{r_{desired}}{r_{undesired}}", "desc": "Product selectivity"},
                {"name": "Yield", "eq": r"Y = \frac{\text{moles desired}}{\text{moles reacted}}", "desc": "Product yield"},
                {"name": "CSTR in Series", "eq": r"\tau = \sum_{i=1}^n \frac{X_i - X_{i-1}}{-r_{Ai}}", "desc": "Multiple CSTRs"},
                {"name": "Recycle Reactor", "eq": r"\tau = \frac{V}{v_0} = (1+R) \int_{X_0}^{X_f} \frac{dX}{-r_A}", "desc": "Recycle configuration"},
                {"name": "Autothermal Reactor", "eq": r"T_{out} = T_{in} + \frac{(-\Delta H_R) C_{A0} X}{\rho C_p}", "desc": "Heat balance"}
            ]
        },
        "Thermodynamics": {
            "color": "#e67e22", "icon": "🟠",
            "formulas": [
                {"name": "Ideal Gas Law", "eq": r"PV = nRT", "desc": "Equation of state"},
                {"name": "First Law", "eq": r"\Delta U = Q - W", "desc": "Energy conservation"},
                {"name": "Second Law", "eq": r"\Delta S_{univ} \geq 0", "desc": "Entropy increase"},
                {"name": "Enthalpy", "eq": r"H = U + PV", "desc": "Heat content"},
                {"name": "Entropy Change", "eq": r"\Delta S = \int \frac{dQ_{rev}}{T}", "desc": "Reversible entropy"},
                {"name": "Gibbs Free Energy", "eq": r"G = H - TS", "desc": "Spontaneity indicator"},
                {"name": "Carnot Efficiency", "eq": r"\eta_{max} = 1 - \frac{T_C}{T_H}", "desc": "Maximum thermal efficiency"},
                {"name": "Clausius-Clapeyron", "eq": r"\frac{dP}{dT} = \frac{\Delta H_{vap}}{T \Delta V}", "desc": "Vapor pressure"},
                {"name": "Antoine Equation", "eq": r"\log_{10} P = A - \frac{B}{T + C}", "desc": "Vapor pressure correlation"},
                {"name": "Raoult's Law", "eq": r"P_A = x_A P_A^{sat}", "desc": "Ideal liquid-vapor"},
                {"name": "Henry's Law", "eq": r"P_A = H_A x_A", "desc": "Gas solubility"},
                {"name": "Van der Waals", "eq": r"\left(P + \frac{a}{V^2}\right)(V-b) = RT", "desc": "Real gas EOS"},
                {"name": "Peng-Robinson", "eq": r"P = \frac{RT}{V-b} - \frac{a\alpha}{V(V+b) + b(V-b)}", "desc": "Cubic EOS"},
                {"name": "Compressibility Factor", "eq": r"Z = \frac{PV}{nRT}", "desc": "Ideal gas deviation"},
                {"name": "Joule-Thomson", "eq": r"\mu_{JT} = \left(\frac{\partial T}{\partial P}\right)_H", "desc": "Isenthalpic expansion"},
                {"name": "Fugacity", "eq": r"f = \phi P", "desc": "Effective pressure"},
                {"name": "Activity Coefficient", "eq": r"\gamma_i = \frac{f_i}{x_i f_i^0}", "desc": "Non-ideality"},
                {"name": "Residual Property", "eq": r"G^R = G - G^{IG}", "desc": "Deviation from ideal"}
            ]
        }
    }
    
    # Dashboard View
    if st.session_state.formulas_view == "dashboard":
        st.markdown("""
            <div class="main-header">
                <h1>📚 Chemical Engineering Formulas</h1>
                <p>Complete reference library with equations, symbols, and applications</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.info("📖 Select a subject below to browse formulas. Click any formula to view detailed information.")
        
        cols = st.columns(3)
        categories = list(formulas.keys())
        
        for i, cat in enumerate(categories):
            with cols[i % 3]:
                color = formulas[cat]["color"]
                icon = formulas[cat]["icon"]
                count = len(formulas[cat]["formulas"])
                
                st.markdown(f"""
                    <div class="category-card" style="border-color: {color}40;">
                        <div class="category-icon">{icon}</div>
                        <div class="category-title" style="color: {color};">{cat}</div>
                        <div class="category-desc">{count} formulas</div>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Browse {cat}", key=f"btn_{cat}", use_container_width=True):
                    st.session_state.formulas_view = "category"
                    st.session_state.selected_category = cat
                    st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
        
        total = sum(len(data["formulas"]) for data in formulas.values())
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📚 Subjects", len(categories))
        col2.metric("📐 Formulas", total)
        col3.metric("📖 References", "15+")
        col4.metric("🎓 Level", "Professional")
    
    # Category View
    elif st.session_state.formulas_view == "category":
        cat = st.session_state.selected_category
        color = formulas[cat]["color"]
        icon = formulas[cat]["icon"]
        
        if st.button("← Back to Dashboard", use_container_width=False):
            st.session_state.formulas_view = "dashboard"
            st.session_state.selected_category = None
            st.rerun()
        
        st.markdown(f"""
            <div class="detail-header">
                <h2 style="color: {color};">{icon} {cat} Formulas</h2>
                <p style="color: rgba(255,255,255,0.7);">Click on any formula to view details</p>
            </div>
        """, unsafe_allow_html=True)
        
        for formula in formulas[cat]["formulas"]:
            with st.expander(f"**{formula['name']}**", expanded=False):
                st.latex(formula['eq'])
                st.caption(f"📌 **Purpose:** {formula['desc']}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #0f3443, #1a5a6e); border-radius: 10px; margin-top: 2rem;">
            <p style="margin: 0;">
                <span style="color: #2ecc71; font-weight: bold;">🔬</span>
                <span style="color: #2ecc71;"> Developed by </span>
                <span style="color: white; font-weight: bold;">ZUNAIR SHAHZAD</span>
                <span style="color: #FFD700;"> | </span>
                <span style="color: #FFD700;">Chemical Engineering</span>
                <span style="color: #FFD700;"> | </span>
                <span style="color: white;">UET Lahore (New Campus)</span>
            </p>
        </div>
    """, unsafe_allow_html=True)