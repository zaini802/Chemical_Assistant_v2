import streamlit as st
import math

def show_pressure_drop():
    # Custom CSS for better styling
    st.markdown("""
        <style>
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
        }
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
        
        Re = (rho * v * D) / mu
        
        if Re < 2000:
            flow_type = "🟢 Laminar Flow"
            flow_desc = "Smooth, orderly flow. Low friction. Good for viscous fluids."
            flow_color = "#2ecc71"
        elif Re < 4000:
            flow_type = "🟡 Transitional Flow"
            flow_desc = "Unstable flow. May switch between laminar and turbulent."
            flow_color = "#f39c12"
        else:
            flow_type = "🔴 Turbulent Flow"
            flow_desc = "Chaotic flow with eddies. Higher friction but better mixing."
            flow_color = "#e74c3c"
        
        st.markdown('<div class="section-header"><h3>📊 Results</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="result-box">
                    <p style="margin: 0; font-size: 0.9rem;">Reynolds Number (Re)</p>
                    <p class="result-number">{Re:,.0f}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="result-box" style="border-color: {flow_color};">
                    <p style="margin: 0; font-size: 0.9rem;">Flow Type</p>
                    <p class="result-number" style="color: {flow_color}; font-size: 1.2rem;">{flow_type}</p>
                    <p style="margin: 0; font-size: 0.8rem;">{flow_desc}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.info("""
        **⏳ Coming in Phase 2:**
        - Friction Factor (f) calculation
        - Pressure Drop (ΔP) in Pa, kPa, bar, psi
        - Head Loss (h_f) in meters
        - Pump Power in Watts, kW, HP
        """)
    
    # ========== FOOTER ==========
    st.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #0f3443, #1a5a6e); border-radius: 10px;">
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