import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_reynolds():
    st.header("📊 Reynolds Number Calculator")
    st.markdown("**Re = ρ × v × d / μ**")

    with st.expander("ℹ️ What is Reynolds Number?"):
        st.markdown("""
        - **Re < 2000** → Laminar Flow (smooth, orderly)
        - **2000 < Re < 4000** → Transitional Flow (unstable)
        - **Re > 4000** → Turbulent Flow (chaotic, mixing)
        """)

        # Inputs - expander ke BAHAR
        col1, col2 = st.columns(2)

        with col1:
            rho = st.number_input("Density ρ (kg/m³)", value=1000.0, step=10.0)
            v = st.number_input("Velocity v (m/s)", value=1.0, step=0.1)

            with col2:
                d = st.number_input("Diameter d (m)", value=0.05, step=0.01)
                mu = st.number_input("Viscosity μ (Pa·s)", value=0.001, step=0.0001, format="%.4f")

                if st.button("Calculate Reynolds Number", type="primary"):
                    if mu > 0:
                        Re = (rho * v * d) / mu
                        st.success(f"### ✅ Reynolds Number = {Re:,.2f}")

                        # Flow type
                        if Re < 2000:
                            st.info("🟢 **Flow Type:** Laminar Flow")
                            flow_color = "green"
                            flow_type = "Laminar"
                        elif Re < 4000:
                            st.warning("🟡 **Flow Type:** Transitional Flow")
                            flow_color = "orange"
                            flow_type = "Transitional"
                        else:
                            st.error("🔴 **Flow Type:** Turbulent Flow")
                            flow_color = "red"
                            flow_type = "Turbulent"

                            # Graph - if/elif ke BAAD (sab cases mein dikhega)
                            st.markdown("---")
                            st.subheader("📈 Reynolds Number Visualization")

                            fig, ax = plt.subplots(figsize=(8, 2))

                            ax.axvspan(0, 2000, alpha=0.3, color='green', label='Laminar')
                            ax.axvspan(2000, 4000, alpha=0.3, color='orange', label='Transitional')
                            ax.axvspan(4000, max(5000, Re + 1000), alpha=0.3, color='red', label='Turbulent')

                            ax.plot(Re, 0.5, 'bo', markersize=12, label=f'Re = {Re:.0f}')
                            ax.axvline(x=Re, color='blue', linestyle='--', linewidth=2)

                            ax.set_xlim(0, max(5000, Re + 1000))
                            ax.set_yticks([])
                            ax.set_xlabel('Reynolds Number (Re)')
                            ax.set_title('Flow Regime')
                            ax.legend(loc='upper right')

                            st.pyplot(fig)
                            plt.close(fig)

                            # Detailed Analysis
                            st.markdown("---")
                            st.subheader("📋 Detailed Analysis")

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Reynolds Number", f"{Re:,.2f}")
                                with col2:
                                    st.metric("Flow Type", flow_type)
                                    with col3:
                                        if Re < 2000:
                                            st.metric("Recommendation", "Increase velocity or diameter")
                                        elif Re > 4000:
                                            st.metric("Recommendation", "Check for pressure drop")
                                        else:
                                            st.metric("Recommendation", "Monitor flow conditions")
                    else:
                        st.error("❌ Viscosity must be greater than 0!")