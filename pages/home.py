import streamlit as st

def show_home():
    st.write("🏭 Chemical Engineering Assistant")
    st.write("Welcome to your All-in-One ChemE Tool")
    st.markdown("---")
    st.markdown("### Available Modules:")
    st.markdown("- 🌡️ Heat Exchanger")
    st.markdown("- 📊 Reynolds Number")
    st.markdown("- ⚠️ Safety Analyzer")
    st.markdown("- 🔄 Unit Converter")
    st.markdown("- 💬 Chatbot")
    st.markdown("---")
    st.info("Select a module from the left sidebar")
