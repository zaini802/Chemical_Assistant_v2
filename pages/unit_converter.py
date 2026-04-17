import streamlit as st
import math

def show_unit_converter():
    # Custom CSS for professional styling
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
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
        }
        .main-header p {
            color: #34e89e;
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
        }
        .section-header {
            background: linear-gradient(135deg, #0f3443, #1a5a6e);
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0 1rem 0;
        }
        .section-header h3 {
            color: #34e89e;
            margin: 0;
            font-size: 1.1rem;
            font-weight: 600;
        }
        .category-btn {
            background: #0f2027;
            border: 1px solid #34e89e44;
            border-radius: 10px;
            padding: 0.75rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            margin: 0.25rem;
        }
        .category-btn:hover {
            transform: translateY(-3px);
            border-color: #34e89e;
            box-shadow: 0 5px 15px rgba(52,232,158,0.2);
        }
        .category-btn.active {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            border-color: #34e89e;
        }
        .category-btn .icon {
            font-size: 1.8rem;
            margin-bottom: 0.25rem;
        }
        .category-btn .label {
            color: white;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .input-box {
            background: #0f2027;
            border: 1px solid #34e89e44;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .result-card {
            background: #0f2027;
            border: 1px solid #34e89e;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        .result-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(52,232,158,0.2);
        }
        .result-value {
            font-size: 1.6rem;
            font-weight: bold;
            color: #34e89e;
            font-family: 'JetBrains Mono', monospace;
        }
        .result-unit {
            font-size: 0.8rem;
            color: rgba(255,255,255,0.6);
            margin-top: 0.25rem;
        }
        .checkbox-group {
            background: #0f2027;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .stCheckbox > label {
            color: #e0e0e0 !important;
            font-size: 0.85rem !important;
        }
        .stCheckbox > label[data-checked="true"] {
            color: #34e89e !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
        <div class="main-header">
            <h1>🔄 Unit Converter</h1>
            <p>Professional Engineering Unit Conversion Tool</p>
        </div>
    """, unsafe_allow_html=True)
    
    # ========== UNIT DATABASE ==========
    # Conversion to SI base units
    units_db = {
        "Temperature": {
            "to_si": {
                "°C": lambda x: x + 273.15,
                "°F": lambda x: (x - 32) * 5/9 + 273.15,
                "K": lambda x: x,
                "°R": lambda x: x * 5/9
            },
            "from_si": {
                "°C": lambda x: x - 273.15,
                "°F": lambda x: (x - 273.15) * 9/5 + 32,
                "K": lambda x: x,
                "°R": lambda x: x * 9/5
            },
            "units": ["°C", "°F", "K", "°R"]
        },
        "Pressure": {
            "to_si": {
                "Pa": 1, "kPa": 1000, "MPa": 1e6, "bar": 1e5, "mbar": 100,
                "atm": 101325, "psi": 6894.76, "torr": 133.322, "mmHg": 133.322,
                "kg/cm²": 98066.5, "mmH₂O": 9.80665
            },
            "units": ["Pa", "kPa", "MPa", "bar", "mbar", "atm", "psi", "torr", "mmHg", "kg/cm²", "mmH₂O"]
        },
        "Length": {
            "to_si": {
                "m": 1, "cm": 0.01, "mm": 0.001, "km": 1000, "in": 0.0254,
                "ft": 0.3048, "yd": 0.9144, "mile": 1609.34
            },
            "units": ["m", "cm", "mm", "km", "in", "ft", "yd", "mile"]
        },
        "Area": {
            "to_si": {
                "m²": 1, "cm²": 0.0001, "mm²": 1e-6, "km²": 1e6,
                "ft²": 0.092903, "in²": 0.00064516, "ha": 10000, "acre": 4046.86
            },
            "units": ["m²", "cm²", "mm²", "km²", "ft²", "in²", "ha", "acre"]
        },
        "Volume": {
            "to_si": {
                "m³": 1, "L": 0.001, "mL": 1e-6, "ft³": 0.0283168,
                "gal (US)": 0.00378541, "gal (UK)": 0.00454609, "bbl": 0.158987
            },
            "units": ["m³", "L", "mL", "ft³", "gal (US)", "gal (UK)", "bbl"]
        },
        "Mass": {
            "to_si": {
                "kg": 1, "g": 0.001, "mg": 1e-6, "t": 1000, "lb": 0.453592, "oz": 0.0283495
            },
            "units": ["kg", "g", "mg", "t", "lb", "oz"]
        },
        "Time": {
            "to_si": {"s": 1, "min": 60, "h": 3600, "d": 86400, "wk": 604800},
            "units": ["s", "min", "h", "d", "wk"]
        },
        "Energy": {
            "to_si": {
                "J": 1, "kJ": 1000, "cal": 4.184, "kcal": 4184,
                "Wh": 3600, "kWh": 3.6e6, "BTU": 1055.06
            },
            "units": ["J", "kJ", "cal", "kcal", "Wh", "kWh", "BTU"]
        },
        "Density": {
            "to_si": {"kg/m³": 1, "g/cm³": 1000, "lb/ft³": 16.0185},
            "units": ["kg/m³", "g/cm³", "lb/ft³"]
        },
        "Dynamic Viscosity": {
            "to_si": {"Pa·s": 1, "cP": 0.001, "P": 0.1},
            "units": ["Pa·s", "cP", "P"]
        },
        "Kinematic Viscosity": {
            "to_si": {"m²/s": 1, "cSt": 1e-6, "St": 0.0001},
            "units": ["m²/s", "cSt", "St"]
        },
        "Thermal Conductivity": {
            "to_si": {"W/m·K": 1, "kcal/h·m·°C": 1.163, "BTU/h·ft·°F": 1.73073},
            "units": ["W/m·K", "kcal/h·m·°C", "BTU/h·ft·°F"]
        },
        "Specific Heat": {
            "to_si": {"J/kg·K": 1, "kJ/kg·K": 1000, "cal/g·°C": 4184, "BTU/lb·°F": 4186.8},
            "units": ["J/kg·K", "kJ/kg·K", "cal/g·°C", "BTU/lb·°F"]
        },
        "Volumetric Flow": {
            "to_si": {
                "m³/s": 1, "L/s": 0.001, "m³/h": 0.000277778,
                "L/min": 1.66667e-5, "gal/min": 6.309e-5
            },
            "units": ["m³/s", "L/s", "m³/h", "L/min", "gal/min"]
        },
        "Mass Flow": {
            "to_si": {"kg/s": 1, "kg/h": 0.000277778, "lb/s": 0.453592, "lb/h": 0.000125998},
            "units": ["kg/s", "kg/h", "lb/s", "lb/h"]
        },
        "Force": {
            "to_si": {"N": 1, "kN": 1000, "lbf": 4.44822, "kgf": 9.80665},
            "units": ["N", "kN", "lbf", "kgf"]
        },
        "Power": {
            "to_si": {"W": 1, "kW": 1000, "MW": 1e6, "hp": 745.7, "BTU/hr": 0.293071},
            "units": ["W", "kW", "MW", "hp", "BTU/hr"]
        },
        "Angle": {
            "to_si": {"deg": 0.0174533, "rad": 1, "grad": 0.015708},
            "units": ["deg", "rad", "grad"]
        }
    }
    
    # Add from_si conversion for non-temperature categories
    for cat, data in units_db.items():
        if cat != "Temperature" and "from_si" not in data:
            data["from_si"] = {unit: 1/factor for unit, factor in data["to_si"].items()}
    
    # Category groups
    categories = {
        "Basic": ["Temperature", "Pressure", "Length", "Area", "Volume", "Mass", "Time", "Energy"],
        "Material": ["Density", "Dynamic Viscosity", "Kinematic Viscosity", "Thermal Conductivity", "Specific Heat"],
        "Flow": ["Volumetric Flow", "Mass Flow"],
        "Mechanics": ["Force", "Power", "Angle"]
    }
    
    # ========== UI: Category Selection ==========
    st.markdown('<div class="section-header"><h3>📂 Step 1: Select Category</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    selected_category = st.session_state.get("selected_category", "Basic")
    
    with col1:
        if st.button("🔧 Basic", use_container_width=True, type="primary" if selected_category == "Basic" else "secondary"):
            st.session_state.selected_category = "Basic"
            st.rerun()
    with col2:
        if st.button("🧪 Material", use_container_width=True, type="primary" if selected_category == "Material" else "secondary"):
            st.session_state.selected_category = "Material"
            st.rerun()
    with col3:
        if st.button("💧 Flow", use_container_width=True, type="primary" if selected_category == "Flow" else "secondary"):
            st.session_state.selected_category = "Flow"
            st.rerun()
    with col4:
        if st.button("⚙️ Mechanics", use_container_width=True, type="primary" if selected_category == "Mechanics" else "secondary"):
            st.session_state.selected_category = "Mechanics"
            st.rerun()
    
    # ========== UI: Property Selection ==========
    st.markdown('<div class="section-header"><h3>📊 Step 2: Select Property</h3></div>', unsafe_allow_html=True)
    
    current_cat = st.session_state.get("selected_category", "Basic")
    available_props = categories[current_cat]
    selected_prop = st.selectbox("", available_props, key="prop_select", label_visibility="collapsed")
    
    # ========== UI: Input Value and Unit ==========
    st.markdown('<div class="section-header"><h3>📝 Step 3: Enter Value</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        value = st.number_input("", value=1.0, step=0.1, format="%.6f", key="input_value", label_visibility="collapsed")
    with col2:
        input_unit = st.selectbox("", units_db[selected_prop]["units"], key="input_unit", label_visibility="collapsed")
    
    # ========== UI: Output Unit Selection (Checkboxes) ==========
    st.markdown('<div class="section-header"><h3>☑️ Step 4: Select Output Units</h3></div>', unsafe_allow_html=True)
    st.caption("Select which units you want to see in results")
    
    all_units = units_db[selected_prop]["units"]
    selected_units = []
    
    cols = st.columns(4)
    for i, unit in enumerate(all_units):
        with cols[i % 4]:
            #if st.checkbox(unit, key=f"out_{selected_prop}_{unit}", value=(unit != input_unit)):
            if st.checkbox(unit, key=f"out_{selected_prop}_{unit}", value=False):
                selected_units.append(unit)
    
    # ========== Convert Button ==========
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        convert_clicked = st.button("🔄 CONVERT", type="primary", use_container_width=True)
    
    # ========== Results Display ==========
    if convert_clicked:
        if not selected_units:
            st.warning("⚠️ Please select at least one output unit!")
        else:
            st.markdown('<div class="section-header"><h3>📥 Results</h3></div>', unsafe_allow_html=True)
            
            # Convert input to SI
            prop_data = units_db[selected_prop]
            if selected_prop == "Temperature":
                si_value = prop_data["to_si"][input_unit](value)
            else:
                si_value = value * prop_data["to_si"][input_unit]
            
            # Display results for selected units
            results_per_row = 3
            for i in range(0, len(selected_units), results_per_row):
                cols = st.columns(results_per_row)
                for j, unit in enumerate(selected_units[i:i+results_per_row]):
                    with cols[j]:
                        if selected_prop == "Temperature":
                            result = prop_data["from_si"][unit](si_value)
                        else:
                            result = si_value * prop_data["from_si"][unit]
                        
                        st.markdown(f"""
                            <div class="result-card">
                                <div class="result-value">{result:.6g}</div>
                                <div class="result-unit">{unit}</div>
                            </div>
                        """, unsafe_allow_html=True)
            
            # Show conversion formula info
            with st.expander("📐 Conversion Details"):
                st.markdown(f"**Input:** {value} {input_unit}")
                st.markdown(f"**SI Value:** {si_value:.6g}")
                st.markdown(f"**Output Units:** {', '.join(selected_units)}")
    
    # ========== Reference Section ==========
    with st.expander("📚 Reference Standards"):
        st.markdown("""
        | Standard | Description |
        |----------|-------------|
        | **NIST SP 811** | Guide for the Use of the International System of Units (SI) |
        | **ISO 80000** | Quantities and units - International standards |
        | **ASME PTC 19.1** | Test Uncertainty - Measurement instruments |
        | **IEEE/ASTM SI 10** | American National Standard for Metric Practice |
        """)
    
    # ========== Footer ==========
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