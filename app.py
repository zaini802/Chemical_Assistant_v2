import streamlit as st
from components.header import show_header
from components.sidebar import show_sidebar
from components.footer import show_footer
from pages.home import show_home

st.set_page_config(page_title="ChemEng Assistant", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

show_header()
page = show_sidebar()

if page == "Home":
    show_home()
elif page == "Chatbot":
    from pages.chatbot import show_chatbot
    show_chatbot()
else:
    st.header(page)
    st.info(f"✅ {page} page — Coming soon!")

    show_footer()