import streamlit as st

def show_footer():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col2:
        st.caption("Made with ❤️ using Streamlit | ChemEng Assistant")