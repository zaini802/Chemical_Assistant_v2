import streamlit as st

def show_home():
    # Custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');
        
        .welcome-box {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .welcome-title {
            font-size: 2rem;
            font-weight: 700;
            color: white;
            margin-bottom: 0.5rem;
        }
        .welcome-subtitle {
            font-size: 1rem;
            color: #34e89e;
        }
        .module-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.2rem;
            margin: 1.5rem 0;
        }
        .module-card {
            background: linear-gradient(135deg, #0f2027, #1a2a35);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(52,232,158,0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .module-card:hover {
            transform: translateY(-5px);
            border-color: #34e89e;
            box-shadow: 0 10px 25px rgba(52,232,158,0.25);
        }
        .module-icon {
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
        }
        .module-name {
            font-size: 1rem;
            font-weight: 700;
            color: #34e89e;
            margin-bottom: 0.3rem;
        }
        .module-desc {
            font-size: 0.75rem;
            color: rgba(255,255,255,0.6);
            margin-bottom: 0.5rem;
        }
        .module-equation {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            color: #FFD700;
            background: rgba(0,0,0,0.3);
            padding: 0.2rem;
            border-radius: 6px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Welcome Box
#     st.markdown("""
# #         <div class="welcome-box">
# #             <div class="welcome-title">🧪 Chemical Engineering Assistant</div>
#             <div class="welcome-subtitle">Welcome to your All-in-One ChemE Tool</div>
#         </div>
#     """, unsafe_allow_html=True)
    
    # Available Modules
    st.markdown("### 📌 Available Modules")
    
    modules = [
        ("🌡️", "Heat Exchanger", "LMTD, NTU, ε design", "LMTD | NTU | ε"),
        ("📊", "Reynolds Number", "Flow regime calculator", "Re = ρvD/μ"),
        ("🔥", "Heat Transfer", "Q = U × A × ΔT", "Q = U × A × ΔT"),
        ("📉", "Pressure Drop", "ΔP calculation", "ΔP = f × L/D × ρv²/2"),
        ("🔄", "Unit Converter", "100+ engineering units", "Length | Temp | Pressure"),
    ]
    
    cols = st.columns(3)
    for i, (icon, name, desc, eq) in enumerate(modules):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="module-card">
                    <div class="module-icon">{icon}</div>
                    <div class="module-name">{name}</div>
                    <div class="module-desc">{desc}</div>
                    <div class="module-equation">{eq}</div>
                </div>
            """, unsafe_allow_html=True)
            # if st.button(f"Launch {name}", key=name, use_container_width=True):
            #     st.session_state.page = name
            #     st.rerun()
    
    # Stats
    # st.markdown("---")
    # col1, col2, col3, col4 = st.columns(4)
    # col1.metric("📚 Formulas", "50+")
    # col2.metric("🔄 Converters", "20+")
    # col3.metric("⚙️ Modules", "5+")
    # col4.metric("🎓 Status", "Active")
    
    # Colorful Footer
    st.markdown("""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #0f3443, #1a5a6e); border-radius: 10px; margin-top: 1.5rem;">
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
