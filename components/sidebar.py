import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.markdown("## 📚 Navigation")
        st.markdown("---")

        page = st.radio(
            "Select Module",
            ["🏠 Home", "🌡️ Heat Exchanger", "🔄 Unit Converter", "💬 Chatbot"],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.caption("💡 Tip: Select a module to get started")

        return page