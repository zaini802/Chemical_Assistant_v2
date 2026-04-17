import streamlit as st
import os
import base64
from components.header import show_header
from components.sidebar import show_sidebar
from components.footer import show_footer
from pages.home import show_home
from pages.reynolds import show_reynolds

st.set_page_config(page_title="ChemEng Assistant", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
    background-color: #34e89e !important;
        color: #0f2027 !important;
            font-weight: bold;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Floating Bot GIF
current_dir = os.path.dirname(__file__)
bot_path = os.path.join(current_dir, "images", "bot.gif")
if os.path.exists(bot_path):
    with open(bot_path, "rb") as f:
        bot_base64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div style="position: fixed; top: 15px; left: 15px; z-index: 9999;">
        <img src="data:image/gif;base64,{bot_base64}" width="70px">
        </div>
                """, unsafe_allow_html=True)

show_header()
page = show_sidebar()

if page == "Home":
                    show_home()
elif page == "Reynolds Number":
                    show_reynolds()
elif page == "Heat Transfer":
    from pages.heat_transfer import show_heat_transfer
    show_heat_transfer()
elif page == "Pressure Drop":
    from pages.Pressure_drop.phase_2 import show_pressure_drop_phase2
    show_pressure_drop_phase2()
elif page == "Heat Exchanger":
    from pages.heat_exchanger import show_heat_exchanger
    show_heat_exchanger()    
elif page == "Chatbot":
    from pages.chatbot import show_chatbot
    show_chatbot()
else:
    st.header(page)
    st.info(f"✅ {page} page — Coming soon!")

    show_footer()