import streamlit as st
from PIL import Image
import os

def show_sidebar():
    with st.sidebar:
        # Profile picture at top
        img_path = r"D:/My_Projects/Chemical_Assistant_v2/images/zunair.jpeg"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, width=140)
            st.markdown("""
                <style>
                .stImage {
                    display: flex;
                    justify-content: center !important;
                }
                .stImage img {
                    border-radius: 50% !important;
                    border: 4px solid #34e89e !important;
                    object-fit: cover;
                    width: 140px;
                    height: 140px;
                }
                </style>
            """, unsafe_allow_html=True)
        else:
            st.warning("Photo nahi mili")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
<div style='background: linear-gradient(135deg, #dc2626, #b91c1c);
padding: 12px;
border-radius: 12px;
text-align: center;
margin-bottom: 10px;
border: 1px solid #34e89e;
box-shadow: 0 2px 8px rgba(0,0,0,0.2);'>
<h3 style='color: white; margin: 0; font-weight: bold;'>📚 NAVIGATION</h3>
</div>
""", unsafe_allow_html=True)
        st.markdown("---")

        # Stylish CSS for navigation (SIRF EK BAAR)
        st.markdown("""
        <style>
        .stRadio > div {
            background: rgba(15,32,39,0.4);
            border-radius: 16px;
            padding: 8px;
        }
        .stRadio label {
            background: rgba(15,32,39,0.8) !important;
            border-radius: 12px !important;
            margin: 6px 0 !important;
            padding: 12px 16px !important;
            border: 1px solid rgba(52,232,158,0.2) !important;
            transition: all 0.3s ease !important;
        }
        .stRadio label:hover {
            background: linear-gradient(135deg, #1e3c72, #2a5298) !important;
            transform: translateX(8px);
            border-color: #34e89e !important;
        }
        .stRadio label[data-checked="true"] {
            background: linear-gradient(135deg, #34e89e, #1a5a6e) !important;
            border-left: 4px solid #FFD700 !important;
            box-shadow: 0 4px 15px rgba(52,232,158,0.3) !important;
        }
        .stRadio label p {
            font-weight: 600 !important;
            font-size: 14px !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

        page = st.radio(
            "Select Module",
            [
                "🏠 Home",
                "📊 Reynolds Number",
                "🔥 Heat Transfer",
                "📉 Pressure Drop",
                "🔄 Unit Converter",
                "🌡️ Heat Exchanger",
                #"⚠️ Safety Analyzer",
                #"📚 Formulas",
                #"💡 Concepts",
                "💬 EngiChat"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        st.markdown("""
        <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #0f3443, #1a5a6e); border-radius: 12px; margin-top: 10px;'>
            <p style='font-size: 14px; font-weight: bold; color: #34e89e; margin: 5px 0;'>
                🔥 Developed by <span style='color: white;'>ZUNAIR SHAHZAD</span>
            </p>
            <p style='font-size: 16px; font-weight: bold; color: #FFD700; margin: 4px 0;'>
                🎓 <strong>Chemical Engineering</strong>
            </p>
            <p style='font-size: 16px; font-weight: bold; color: #FFD700; margin: 4px 0 8px 0;'>
                <strong>UET Lahore</strong>
            </p>
            <p style='font-size: 12px; margin: 8px 0;'>
                📧 <a href='mailto:eng.zunairshahzad@gmail.com' style='color: #34e89e; text-decoration: none; font-weight: bold;'>eng.zunairshahzad@gmail.com</a><br>
                📞 <a href='https://wa.me/923074274294' style='color: #34e89e; text-decoration: none; font-weight: bold;'>+92 307 4274294</a>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # st.markdown("""
        # <p style='font-weight: bold; color: #ff6666; margin-bottom: 5px; margin-top: 10px;'>
        #     🌐 LANGUAGE
        # </p>
        # """, unsafe_allow_html=True)

        # st.selectbox("", ["English", "Urdu", "Hindi", "Arabic", "Spanish", "French", "German", "Chinese", "Turkish", "Russian"], label_visibility="collapsed")

        page_map = {
            "🏠 Home": "Home",
            "📊 Reynolds Number": "Reynolds Number",
            "🔥 Heat Transfer": "Heat Transfer",
            "📉 Pressure Drop": "Pressure Drop",
            "🔄 Unit Converter": "Unit Converter",
            "🌡️ Heat Exchanger": "Heat Exchanger",
            #"⚠️ Safety Analyzer": "Safety Analyzer",
            #"📚 Formulas": "Formulas",
            #"💡 Concepts": "Concepts",
            "💬 EngiChat": "EngiChat"
        }

        return page_map[page]
