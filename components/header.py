import streamlit as st

def show_header():
    st.set_page_config(page_title="ChemEng Assistant", layout="wide", page_icon="🧪")

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72, #2a5298);
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;">
    <h1 style="color: white; text-align: center; margin: 0;">
    🧪 Chemical Engineering Assistant
    </h1>
    <p style="color: #e0e0e0; text-align: center; margin: 0.5rem 0 0 0;">
        Your All-in-One ChemE Tool
        </p>
        </div>
        """, unsafe_allow_html=True)