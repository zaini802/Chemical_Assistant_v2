import streamlit as st

def show_header():
    st.set_page_config(page_title="ChemEng Assistant", layout="wide", page_icon="🧪")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f3443, #34e89e);
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    text-align: center;">
    <h1 style="color: white; margin: 0;">🧪 Chemical Engineering Assistant</h1>
    <p style="color: #f0f0f0; margin: 0.5rem 0 0 0;">Professional ChemE Design & Analysis Suite</p>
        </div>
        """, unsafe_allow_html=True)