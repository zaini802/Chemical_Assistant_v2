import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.markdown("## 📚 Navigation")
        st.markdown("---")

        page = st.radio(
            "Select Module",
            [
                "Home",
                "Reynolds Number",
                "Heat Transfer",
                "Pressure Drop",
                "Unit Converter",
                "Heat Exchanger",
                "Safety Analyzer",
                "Formulas",
                "Concepts",
                "Chatbot"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.caption("💡 Tip: Select a module to get started")

        return page