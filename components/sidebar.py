import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 📚 **NAVIGATION**")
        st.markdown("---")

        page = st.radio(
            "Select Module",
            [
                "🏠 Home",
                "📊 Reynolds Number",
                "🔥 Heat Transfer",
                "📉 Pressure Drop",
                "🔄 Unit Converter",
                "🌡️ Heat Exchanger",
                "⚠️ Safety Analyzer",
                "📚 Formulas",
                "💡 Concepts",
                "💬 Chatbot"
            ],
            label_visibility="collapsed"
        )

        st.markdown("""
        <style>
        .stRadio > div { gap: 8px; }
        .stRadio label {
            font-weight: 700 !important;
            font-size: 15px !important;
            color: #e0e0e0 !important;
                padding: 8px 12px !important;
                border-radius: 8px !important;
                transition: all 0.2s ease !important;
            }
            .stRadio label:hover {
                background-color: rgba(52, 232, 158, 0.15) !important;
                color: #34e89e !important;
                }
                .stRadio label[data-checked="true"] {
                    background-color: #34e89e !important;
                        color: #0f2027 !important;
                            font-weight: 900 !important;
                        }
                        /* Radio button text bold karne ke liye */
                        .stRadio label p {
                            font-weight: 700 !important;
                            font-size: 15px !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)

        st.markdown("---")

                        # ✅ Yeh ab with st.sidebar: ke ANDAR hai
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

        st.markdown("""
                                            <p style='font-weight: bold; color: #ff6666;
                                                margin-bottom: 5px; margin-top: 10px;'>
                                                🌐 LANGUAGE</p>
                                                """, unsafe_allow_html=True)

        st.selectbox("", ["English", "Urdu", "Arabic", "Hindi"],
                                                label_visibility="collapsed")

        page_map = {
                                                    "🏠 Home": "Home",
                                                    "📊 Reynolds Number": "Reynolds Number",
                                                    "🔥 Heat Transfer": "Heat Transfer",
                                                    "📉 Pressure Drop": "Pressure Drop",
                                                    "🔄 Unit Converter": "Unit Converter",
                                                    "🌡️ Heat Exchanger": "Heat Exchanger",
                                                    "⚠️ Safety Analyzer": "Safety Analyzer",
                                                    "📚 Formulas": "Formulas",
                                                    "💡 Concepts": "Concepts",
                                                    "💬 Chatbot": "Chatbot"
                                                }

        return page_map[page]