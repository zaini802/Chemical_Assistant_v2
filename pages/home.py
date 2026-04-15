import streamlit as st

def show_home():
    st.header("🏠 Welcome to Chemical Engineering Assistant")
    st.write("Select a module from the left sidebar to get started.")
    
    st.markdown("### Available Modules:")
    st.markdown("""
    - **Reynolds Number** – Flow type calculator
    - **Heat Transfer** – Q = UAΔT
    - **Pressure Drop** – ΔP calculation
    - **Unit Converter** – Convert between units
    - **Heat Exchanger** – LMTD, NTU, Effectiveness
    - **Safety Analyzer** – Chemical safety data
    - **Chatbot** – AI assistant for ChemE questions
    """)
