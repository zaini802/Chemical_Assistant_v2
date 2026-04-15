import streamlit as st
from PIL import Image
import os
import base64
import io

def show_sidebar():
    with st.sidebar:
        # More space on top
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("## 📚 **NAVIGATION**")
        st.markdown("---")

        page = st.radio(
            "Select Module",
            [
                "🏠 **Home**",
                "📊 **Reynolds Number**",
                "🔥 **Heat Transfer**",
                "📉 **Pressure Drop**",
                "🔄 **Unit Converter**",
                "🌡️ **Heat Exchanger**",
                "⚠️ **Safety Analyzer**",
                "📚 **Formulas**",
                "💡 **Concepts**",
                "💬 **Chatbot**"
            ],
            label_visibility="collapsed"
        )

        # Custom CSS for radio buttons
        st.markdown("""
        <style>
        .stRadio > div {
            gap: 8px;
        }
        .stRadio label {
            font-weight: 700 !important;
            font-size: 14px !important;
            color: #e0e0e0 !important;
                padding: 6px 10px !important;
                border-radius: 8px !important;
                transition: all 0.2s ease !important;
            }
            .stRadio label:hover {
                background-color: rgba(52, 232, 158, 0.1) !important;
            }
            .stRadio label[data-checked="true"] {
                background-color: #34e89e !important;
                    color: #0f2027 !important;
                        font-weight: bold !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

        st.markdown("---")

                    # Stylish Sidebar Info
        st.markdown(
                        """
                        <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #0f3443, #1a5a6e); border-radius: 12px; margin-top: 10px;'>
                        <p style='font-size: 14px; font-weight: bold; color: #34e89e; margin: 5px 0;'>
                            🔥 Developed by <span style='color: white;'>ZUNAIR SHAHZAD</span>
                            </p>
                            <p style='font-size: 16px; font-weight: bold; color: #FFD700; margin: 4px 0; text-shadow: 0 0 5px rgba(255,215,0,0.5);'>
                                🎓 <strong>Chemical Engineering</strong>
                                </p>
                                <p style='font-size: 16px; font-weight: bold; color: #FFD700; margin: 4px 0 8px 0; text-shadow: 0 0 5px rgba(255,215,0,0.5);'>
                                    <strong>UET Lahore</strong>
                                    </p>
                                    <p style='font-size: 12px; margin: 8px 0;'>
                                    📧 <a href='mailto:eng.zunairshahzad@gmail.com' style='color: #34e89e; text-decoration: none; font-weight: bold;'>eng.zunairshahzad@gmail.com</a><br>
                                        📞 <a href='https://wa.me/923074274294' style='color: #34e89e; text-decoration: none; font-weight: bold;'>+92 307 4274294</a>
                                            </p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                        # Language selector
        st.markdown("<p style='font-weight: bold; color: #ff6666; margin-bottom: 5px; margin-top: 10px;'>🌐 LANGUAGE</p>", unsafe_allow_html=True)
        st.selectbox("", ["English", "Urdu", "Arabic", "Hindi"], label_visibility="collapsed")

        return page