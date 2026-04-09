import streamlit as st
from components.header import show_header
from components.sidebar import show_sidebar
from components.footer import show_footer
from pages.home import show_home
from pages.heat_exchanger import show_heat_exchanger
from pages.unit_converter import show_unit_converter
from pages.chatbot import show_chatbot

show_header()
page = show_sidebar()

if page == "🏠 Home":
    show_home()
elif page == "🌡️ Heat Exchanger":
    show_heat_exchanger()
elif page == "🔄 Unit Converter":
    show_unit_converter()
elif page == "💬 Chatbot":
    show_chatbot()

    show_footer()