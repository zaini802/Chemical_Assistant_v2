import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_pdf_report(result_type, result_value, unit, inputs, categories, values):
    """Generate PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1e3c72'),
        alignment=1,
        spaceAfter=30
    )
    story.append(Paragraph("Heat Transfer Calculator Report", title_style))
    story.append(Spacer(1, 12))
    
    # Date and Time
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Result Summary
    story.append(Paragraph("Result Summary", styles['Heading2']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Target Variable:</b> {result_type}", styles['Normal']))
    story.append(Paragraph(f"<b>Calculated Value:</b> {result_value:.6f} {unit}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Input Values
    story.append(Paragraph("Input Values", styles['Heading2']))
    story.append(Spacer(1, 10))
    for key, val in inputs.items():
        story.append(Paragraph(f"<b>{key}:</b> {val}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Sensitivity Analysis
    story.append(Paragraph("Sensitivity Analysis (+20% on each input)", styles['Heading2']))
    story.append(Spacer(1, 10))
    for i, cat in enumerate(categories):
        story.append(Paragraph(f"{cat}: {values[i]:.6f}", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_word_report(result_type, result_value, unit, inputs, categories, values):
    """Generate Word/HTML report"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Heat Transfer Calculator Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #1e3c72; text-align: center; }}
            h2 {{ color: #2a5298; margin-top: 30px; }}
            .result {{ font-size: 18px; font-weight: bold; color: #34e89e; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #1e3c72; color: white; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <h1>🔥 Heat Transfer Calculator Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>📊 Result Summary</h2>
        <p><strong>Target Variable:</strong> {result_type}</p>
        <p class="result"><strong>Calculated Value:</strong> {result_value:.6f} {unit}</p>
        
        <h2>📥 Input Values</h2>
        <table>
            <tr><th>Parameter</th><th>Value</th></tr>
    """
    for key, val in inputs.items():
        html_content += f"<tr><td>{key}</td><td>{val}</td></tr>"
    
    html_content += f"""
        </table>
        
        <h2>📈 Sensitivity Analysis (+20% on each input)</h2>
        <table>
            <tr><th>Scenario</th><th>Value</th></tr>
    """
    for i, cat in enumerate(categories):
        html_content += f"<tr><td>{cat}</td><td>{values[i]:.6f}</td></tr>"
    
    html_content += f"""
        </table>
        
        <h2>📐 Formula Used</h2>
        <p><strong>Q = U × A × ΔT</strong></p>
        
        <div class="footer">
            <p>Developed by ZUNAIR SHAHZAD | Chemical Engineering | UET Lahore</p>
        </div>
    </body>
    </html>
    """
    return html_content

def create_txt_report(result_type, result_value, unit, inputs, categories, values):
    """Generate TXT report"""
    report_lines = []
    report_lines.append("="*60)
    report_lines.append("HEAT TRANSFER CALCULATOR REPORT")
    report_lines.append("="*60)
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("RESULT SUMMARY")
    report_lines.append("-"*60)
    report_lines.append(f"Target Variable: {result_type}")
    report_lines.append(f"Calculated Value: {result_value:.6f} {unit}")
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("INPUT VALUES")
    report_lines.append("-"*60)
    for key, val in inputs.items():
        report_lines.append(f"{key}: {val}")
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("SENSITIVITY ANALYSIS (+20% on each input)")
    report_lines.append("-"*60)
    for i, cat in enumerate(categories):
        report_lines.append(f"{cat}: {values[i]:.6f}")
    report_lines.append("")
    report_lines.append("-"*60)
    report_lines.append("Developed by ZUNAIR SHAHZAD | Chemical Engineering | UET Lahore")
    report_lines.append("="*60)
    return "\n".join(report_lines)

def create_download_section(result_type, result_value, unit, inputs, categories, values):
    """Create download buttons for PDF, Word, and TXT"""
    st.markdown("---")
    st.subheader("📥 Download Report")
    
    col1, col2, col3 = st.columns(3)
    
    # PDF Download
    pdf_buffer = create_pdf_report(result_type, result_value, unit, inputs, categories, values)
    b64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode()
    pdf_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="heat_transfer_report.pdf" style="text-decoration: none;"><button style="background-color: #e74c3c; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">📕 PDF Report</button></a>'
    
    # Word/HTML Download
    html_content = create_word_report(result_type, result_value, unit, inputs, categories, values)
    b64_html = base64.b64encode(html_content.encode()).decode()
    word_link = f'<a href="data:application/msword;base64,{b64_html}" download="heat_transfer_report.doc" style="text-decoration: none;"><button style="background-color: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">📘 Word Report</button></a>'
    
    # TXT Download
    txt_content = create_txt_report(result_type, result_value, unit, inputs, categories, values)
    b64_txt = base64.b64encode(txt_content.encode()).decode()
    txt_link = f'<a href="data:file/txt;base64,{b64_txt}" download="heat_transfer_report.txt" style="text-decoration: none;"><button style="background-color: #2ecc71; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;">📄 TXT Report</button></a>'
    
    with col1:
        st.markdown(pdf_link, unsafe_allow_html=True)
    with col2:
        st.markdown(word_link, unsafe_allow_html=True)
    with col3:
        st.markdown(txt_link, unsafe_allow_html=True)

def show_heat_transfer():
    st.header("🔥 Heat Transfer Calculator")
    st.markdown("### Q = U × A × ΔT")
    
    find_var = st.selectbox(
        "What do you want to find?",
        ["Find Q", "Find U", "Find A", "Find ΔT"]
    )
    
    st.markdown("---")
    st.subheader("Enter Values")
    
    if find_var == "Find Q":
        col1, col2 = st.columns(2)
        with col1:
            U = st.number_input("U (W/m²·K)", value=500.0, step=10.0, key="U_input")
            A = st.number_input("A (m²)", value=10.0, step=1.0, key="A_input")
        with col2:
            dT = st.number_input("ΔT (°C)", value=50.0, step=5.0, key="dT_input")
        
        if st.button("📊 Calculate Q", type="primary"):
            Q_watts = U * A * dT
            st.session_state['q_result'] = Q_watts
            st.session_state['result_type'] = "Q"
            st.session_state['U_val'] = U
            st.session_state['A_val'] = A
            st.session_state['dT_val'] = dT
            st.session_state['unit'] = "Watts (W)"
            st.success(f"### ✅ Q = {Q_watts:.4f} W")
    
    elif find_var == "Find U":
        col1, col2 = st.columns(2)
        with col1:
            Q = st.number_input("Q (W)", value=250000.0, step=10000.0, key="Q_input")
            A = st.number_input("A (m²)", value=10.0, step=1.0, key="A_input")
        with col2:
            dT = st.number_input("ΔT (°C)", value=50.0, step=5.0, key="dT_input")
        
        if st.button("📊 Calculate U", type="primary"):
            U_result = Q / (A * dT)
            st.session_state['u_result'] = U_result
            st.session_state['result_type'] = "U"
            st.session_state['Q_val'] = Q
            st.session_state['A_val'] = A
            st.session_state['dT_val'] = dT
            st.session_state['unit'] = "W/m²·K"
            st.success(f"### ✅ U = {U_result:.4f} W/m²·K")
    
    elif find_var == "Find A":
        col1, col2 = st.columns(2)
        with col1:
            Q = st.number_input("Q (W)", value=250000.0, step=10000.0, key="Q_input")
            U = st.number_input("U (W/m²·K)", value=500.0, step=10.0, key="U_input")
        with col2:
            dT = st.number_input("ΔT (°C)", value=50.0, step=5.0, key="dT_input")
        
        if st.button("📊 Calculate A", type="primary"):
            A_result = Q / (U * dT)
            st.session_state['a_result'] = A_result
            st.session_state['result_type'] = "A"
            st.session_state['Q_val'] = Q
            st.session_state['U_val'] = U
            st.session_state['dT_val'] = dT
            st.session_state['unit'] = "m²"
            st.success(f"### ✅ A = {A_result:.4f} m²")
    
    else:
        col1, col2 = st.columns(2)
        with col1:
            Q = st.number_input("Q (W)", value=250000.0, step=10000.0, key="Q_input")
            U = st.number_input("U (W/m²·K)", value=500.0, step=10.0, key="U_input")
        with col2:
            A = st.number_input("A (m²)", value=10.0, step=1.0, key="A_input")
        
        if st.button("📊 Calculate ΔT", type="primary"):
            dT_result = Q / (U * A)
            st.session_state['dt_result'] = dT_result
            st.session_state['result_type'] = "dT"
            st.session_state['Q_val'] = Q
            st.session_state['U_val'] = U
            st.session_state['A_val'] = A
            st.session_state['unit'] = "°C"
            st.success(f"### ✅ ΔT = {dT_result:.4f} °C")
    
    # ========== POST-CALCULATION RESULTS ==========
    result_type = st.session_state.get('result_type', None)
    
    if result_type == "Q":
        q_watts = st.session_state.get('q_result', 0)
        U = st.session_state.get('U_val', 500)
        A = st.session_state.get('A_val', 10)
        dT = st.session_state.get('dT_val', 50)
        
        st.markdown("---")
        st.subheader("🔄 View Q in Different Units")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Watts (W)", f"{q_watts:.4f}")
        with col2:
            st.metric("Kilowatts (kW)", f"{q_watts / 1000:.4f}")
        with col3:
            st.metric("Megawatts (MW)", f"{q_watts / 1_000_000:.4f}")
        
        # Auto Graph
        st.markdown("---")
        st.subheader("📊 Sensitivity Analysis (+20% on each input)")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ['Current Q', 'U +20%', 'A +20%', 'ΔT +20%']
        values = [
            q_watts,
            (U * 1.2) * A * dT,
            U * (A * 1.2) * dT,
            U * A * (dT * 1.2)
        ]
        colors = ['#34e89e', '#2a5298', '#ff6666', '#ffcc00']
        bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=1.5)
        ax.set_ylabel('Q (Watts)')
        ax.set_title('How +20% change affects Q')
        ax.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                    f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        st.pyplot(fig)
        plt.close(fig)
        
        with st.expander("📐 Formula"):
            st.markdown(f"**Q = U × A × ΔT** = {U} × {A} × {dT} = {q_watts:.2f} W")
        
        # Download Section
        inputs = {"U (W/m²·K)": U, "A (m²)": A, "ΔT (°C)": dT}
        create_download_section("Q", q_watts, "Watts (W)", inputs, categories, values)
    
    elif result_type == "U":
        u_result = st.session_state.get('u_result', 0)
        Q = st.session_state.get('Q_val', 250000)
        A = st.session_state.get('A_val', 10)
        dT = st.session_state.get('dT_val', 50)
        
        st.markdown("---")
        st.subheader("🔄 View U in Different Units")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("W/m²·K", f"{u_result:.4f}")
        with col2:
            st.metric("W/m²·°C", f"{u_result:.4f}")
        with col3:
            st.metric("kcal/h·m²·°C", f"{u_result / 1.163:.4f}")
        with col4:
            st.metric("BTU/h·ft²·°F", f"{u_result / 5.678:.4f}")
        
        st.markdown("---")
        st.subheader("📊 Sensitivity Analysis (+20% on each input)")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ['Current U', 'Q +20%', 'A +20%', 'ΔT +20%']
        values = [
            u_result,
            (Q * 1.2) / (A * dT),
            Q / ((A * 1.2) * dT),
            Q / (A * (dT * 1.2))
        ]
        colors = ['#34e89e', '#2a5298', '#ff6666', '#ffcc00']
        bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=1.5)
        ax.set_ylabel('U (W/m²·K)')
        ax.set_title('How +20% change affects U')
        ax.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                    f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        st.pyplot(fig)
        plt.close(fig)
        
        with st.expander("📐 Formula"):
            st.markdown(f"**U = Q / (A × ΔT)** = {Q} / ({A} × {dT}) = {u_result:.4f} W/m²·K")
        
        inputs = {"Q (W)": Q, "A (m²)": A, "ΔT (°C)": dT}
        create_download_section("U", u_result, "W/m²·K", inputs, categories, values)
    
    elif result_type == "A":
        a_result = st.session_state.get('a_result', 0)
        Q = st.session_state.get('Q_val', 250000)
        U = st.session_state.get('U_val', 500)
        dT = st.session_state.get('dT_val', 50)
        
        st.markdown("---")
        st.subheader("🔄 View Area in Different Units")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("m²", f"{a_result:.4f}")
        with col2:
            st.metric("cm²", f"{a_result * 10000:.4f}")
        with col3:
            st.metric("ft²", f"{a_result / 0.092903:.4f}")
        
        st.markdown("---")
        st.subheader("📊 Sensitivity Analysis (+20% on each input)")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ['Current A', 'Q +20%', 'U +20%', 'ΔT +20%']
        values = [
            a_result,
            (Q * 1.2) / (U * dT),
            Q / ((U * 1.2) * dT),
            Q / (U * (dT * 1.2))
        ]
        colors = ['#34e89e', '#2a5298', '#ff6666', '#ffcc00']
        bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=1.5)
        ax.set_ylabel('Area (m²)')
        ax.set_title('How +20% change affects Area')
        ax.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                    f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        st.pyplot(fig)
        plt.close(fig)
        
        with st.expander("📐 Formula"):
            st.markdown(f"**A = Q / (U × ΔT)** = {Q} / ({U} × {dT}) = {a_result:.4f} m²")
        
        inputs = {"Q (W)": Q, "U (W/m²·K)": U, "ΔT (°C)": dT}
        create_download_section("A", a_result, "m²", inputs, categories, values)
    
    elif result_type == "dT":
        dt_result = st.session_state.get('dt_result', 0)
        Q = st.session_state.get('Q_val', 250000)
        U = st.session_state.get('U_val', 500)
        A = st.session_state.get('A_val', 10)
        
        st.markdown("---")
        st.subheader("🔄 View ΔT in Different Units")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("°C", f"{dt_result:.4f}")
        with col2:
            st.metric("K", f"{dt_result + 273.15:.4f}")
        with col3:
            st.metric("°F", f"{(dt_result * 9/5) + 32:.4f}")
        
        st.markdown("---")
        st.subheader("📊 Sensitivity Analysis (+20% on each input)")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ['Current ΔT', 'Q +20%', 'U +20%', 'A +20%']
        values = [
            dt_result,
            (Q * 1.2) / (U * A),
            Q / ((U * 1.2) * A),
            Q / (U * (A * 1.2))
        ]
        colors = ['#34e89e', '#2a5298', '#ff6666', '#ffcc00']
        bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=1.5)
        ax.set_ylabel('ΔT (°C)')
        ax.set_title('How +20% change affects ΔT')
        ax.grid(axis='y', alpha=0.3)
        
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                    f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        st.pyplot(fig)
        plt.close(fig)
        
        with st.expander("📐 Formula"):
            st.markdown(f"**ΔT = Q / (U × A)** = {Q} / ({U} × {A}) = {dt_result:.4f} °C")
        
        inputs = {"Q (W)": Q, "U (W/m²·K)": U, "A (m²)": A}
        create_download_section("ΔT", dt_result, "°C", inputs, categories, values)
    
    # Reference Table
    with st.expander("📚 Typical U Values for Reference"):
        st.markdown("""
        | Fluid Pair | U Range (W/m²·K) |
        |------------|------------------|
        | Water to Water | 800 - 1500 |
        | Water to Oil | 100 - 400 |
        | Steam to Water | 1000 - 3000 |
        | Gas to Gas | 10 - 50 |
        """)
    
    st.markdown("---")
    st.caption("💡 **Tip:** Calculate first, then download report in PDF, Word, or TXT format")
