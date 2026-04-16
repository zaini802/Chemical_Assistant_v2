import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_pdf_report(result_type, result_value, unit, inputs, categories, values, fig=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1e3c72'), alignment=1, spaceAfter=30)
    story.append(Paragraph("Heat Transfer Calculator Report", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Result Summary", styles['Heading2']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Target Variable:</b> {result_type}", styles['Normal']))
    story.append(Paragraph(f"<b>Calculated Value:</b> {result_value:.6f} {unit}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Input Values", styles['Heading2']))
    story.append(Spacer(1, 10))
    for key, val in inputs.items():
        story.append(Paragraph(f"<b>{key}:</b> {val}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Sensitivity Analysis (+20% on each input)", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    table_data = [["Scenario", "Value"]]
    for i, cat in enumerate(categories):
        table_data.append([cat, f"{values[i]:.6f}"])
    
    table = Table(table_data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    
    if fig is not None:
        story.append(Paragraph("Graph: Sensitivity Analysis", styles['Heading2']))
        story.append(Spacer(1, 10))
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img = RLImage(img_buffer, width=6*inch, height=3*inch)
        story.append(img)
        story.append(Spacer(1, 10))
    
    # Footer with Colorful Bold (SIRF EK BAAR)
    story.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#34e89e'),
        alignment=1,
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph("🔬 Developed by ZUNAIR SHAHZAD | Chemical Engineering | UET Lahore 🔬", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_word_report(result_type, result_value, unit, inputs, categories, values, fig=None):
    graph_base64 = ""
    if fig is not None:
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        graph_base64 = base64.b64encode(buf.getvalue()).decode()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>Heat Transfer Calculator Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #1e3c72; text-align: center; }}
        h2 {{ color: #2a5298; margin-top: 30px; }}
        .result {{ font-size: 18px; font-weight: bold; color: #34e89e; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #1e3c72; color: white; }}
        .footer {{ margin-top: 50px; text-align: center; font-size: 12px; }}
        .graph {{ text-align: center; margin: 20px 0; }}
        .graph img {{ max-width: 100%; height: auto; }}
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
        <h2>📈 Sensitivity Analysis</h2>
        <table>
            <tr><th>Scenario</th><th>Value</th></tr>
    """
    for i, cat in enumerate(categories):
        html_content += f"<tr><td>{cat}</td><td>{values[i]:.6f}</td></tr>"
    
    html_content += f"""
        </table>
    """
    
    if graph_base64:
        html_content += f'<h2>📉 Sensitivity Graph</h2><div class="graph"><img src="data:image/png;base64,{graph_base64}"></div>'
    
    html_content += f"""
        <h2>📐 Formula Used</h2>
        <p><strong>Q = U × A × ΔT</strong></p>
        <div class="footer"><p style="color: #34e89e; font-weight: bold;">🔬 Developed by ZUNAIR SHAHZAD | Chemical Engineering | UET Lahore 🔬</p></div>
    </body>
    </html>
    """
    return html_content

def create_txt_report(result_type, result_value, unit, inputs, categories, values):
    report = f"""========================================
HEAT TRANSFER CALCULATOR REPORT
========================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RESULT SUMMARY
--------------
Target Variable: {result_type}
Calculated Value: {result_value:.6f} {unit}

INPUT VALUES
-------------
"""
    for key, val in inputs.items():
        report += f"{key}: {val}\n"
    
    report += f"""
SENSITIVITY ANALYSIS (+20% on each input)
-----------------------------------------
"""
    for i, cat in enumerate(categories):
        report += f"{cat}: {values[i]:.6f}\n"
    
    report += """
-----------------------------------------
🔬 Developed by ZUNAIR SHAHZAD | Chemical Engineering | UET Lahore 🔬
========================================="""
    return report

def create_download_section(result_type, result_value, unit, inputs, categories, values, fig):
    st.markdown("---")
    st.subheader("📥 Download Report")
    
    col1, col2, col3 = st.columns(3)
    
    pdf_buffer = create_pdf_report(result_type, result_value, unit, inputs, categories, values, fig)
    b64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode()
    with col1:
        st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="heat_transfer_report.pdf"><button style="background:#e74c3c; color:white; padding:10px; border:none; border-radius:8px;">📕 PDF Report</button></a>', unsafe_allow_html=True)
    
    html_content = create_word_report(result_type, result_value, unit, inputs, categories, values, fig)
    b64_html = base64.b64encode(html_content.encode()).decode()
    with col2:
        st.markdown(f'<a href="data:application/msword;base64,{b64_html}" download="heat_transfer_report.doc"><button style="background:#3498db; color:white; padding:10px; border:none; border-radius:8px;">📘 Word Report</button></a>', unsafe_allow_html=True)
    
    txt_content = create_txt_report(result_type, result_value, unit, inputs, categories, values)
    b64_txt = base64.b64encode(txt_content.encode()).decode()
    with col3:
        st.markdown(f'<a href="data:file/txt;base64,{b64_txt}" download="heat_transfer_report.txt"><button style="background:#2ecc71; color:white; padding:10px; border:none; border-radius:8px;">📄 TXT Report</button></a>', unsafe_allow_html=True)

def show_heat_transfer():
    st.header("🔥 Heat Transfer Calculator")
    st.markdown("### Q = U × A × ΔT")
    
    find_var = st.selectbox("What do you want to find?", ["Find Q", "Find U", "Find A", "Find ΔT"])
    st.markdown("---")
    st.subheader("Enter Values")
    
    if find_var == "Find Q":
        col1, col2 = st.columns(2)
        with col1:
            U = st.number_input("U (W/m²·K)", value=500.0, step=10.0)
            A = st.number_input("A (m²)", value=10.0, step=1.0)
        with col2:
            dT = st.number_input("ΔT (°C)", value=50.0, step=5.0)
        
        if st.button("📊 Calculate Q", type="primary"):
            Q_watts = U * A * dT
            st.session_state['q_result'] = Q_watts
            st.session_state['result_type'] = "Q"
            st.session_state['U_val'] = U
            st.session_state['A_val'] = A
            st.session_state['dT_val'] = dT
            st.success(f"### ✅ Q = {Q_watts:.4f} W")
    
    elif find_var == "Find U":
        col1, col2 = st.columns(2)
        with col1:
            Q = st.number_input("Q (W)", value=250000.0, step=10000.0)
            A = st.number_input("A (m²)", value=10.0, step=1.0)
        with col2:
            dT = st.number_input("ΔT (°C)", value=50.0, step=5.0)
        
        if st.button("📊 Calculate U", type="primary"):
            U_result = Q / (A * dT)
            st.session_state['u_result'] = U_result
            st.session_state['result_type'] = "U"
            st.session_state['Q_val'] = Q
            st.session_state['A_val'] = A
            st.session_state['dT_val'] = dT
            st.success(f"### ✅ U = {U_result:.4f} W/m²·K")
    
    elif find_var == "Find A":
        col1, col2 = st.columns(2)
        with col1:
            Q = st.number_input("Q (W)", value=250000.0, step=10000.0)
            U = st.number_input("U (W/m²·K)", value=500.0, step=10.0)
        with col2:
            dT = st.number_input("ΔT (°C)", value=50.0, step=5.0)
        
        if st.button("📊 Calculate A", type="primary"):
            A_result = Q / (U * dT)
            st.session_state['a_result'] = A_result
            st.session_state['result_type'] = "A"
            st.session_state['Q_val'] = Q
            st.session_state['U_val'] = U
            st.session_state['dT_val'] = dT
            st.success(f"### ✅ A = {A_result:.4f} m²")
    
    else:
        col1, col2 = st.columns(2)
        with col1:
            Q = st.number_input("Q (W)", value=250000.0, step=10000.0)
            U = st.number_input("U (W/m²·K)", value=500.0, step=10.0)
        with col2:
            A = st.number_input("A (m²)", value=10.0, step=1.0)
        
        if st.button("📊 Calculate ΔT", type="primary"):
            dT_result = Q / (U * A)
            st.session_state['dt_result'] = dT_result
            st.session_state['result_type'] = "dT"
            st.session_state['Q_val'] = Q
            st.session_state['U_val'] = U
            st.session_state['A_val'] = A
            st.success(f"### ✅ ΔT = {dT_result:.4f} °C")
    
    result_type = st.session_state.get('result_type', None)
    
    if result_type == "Q":
        q_watts = st.session_state.get('q_result', 0)
        U = st.session_state.get('U_val', 500)
        A = st.session_state.get('A_val', 10)
        dT = st.session_state.get('dT_val', 50)
        
        st.markdown("---")
        st.subheader("🔄 View Q in Different Units")
        c1, c2, c3 = st.columns(3)
        c1.metric("Watts (W)", f"{q_watts:.4f}")
        c2.metric("Kilowatts (kW)", f"{q_watts/1000:.4f}")
        c3.metric("Megawatts (MW)", f"{q_watts/1e6:.4f}")
        
        st.markdown("---")
        st.subheader("📊 Sensitivity Analysis (+20% on each input)")
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ['Current Q', 'U+20%', 'A+20%', 'ΔT+20%']
        values = [q_watts, (U*1.2)*A*dT, U*(A*1.2)*dT, U*A*(dT*1.2)]
        ax.bar(categories, values, color=['#34e89e','#2a5298','#ff6666','#ffcc00'])
        ax.set_ylabel('Q (Watts)')
        ax.set_title('How +20% change affects Q')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        inputs = {"U (W/m²·K)": U, "A (m²)": A, "ΔT (°C)": dT}
        create_download_section("Q", q_watts, "Watts (W)", inputs, categories, values, fig)
        plt.close(fig)
    
    elif result_type == "U":
        u_result = st.session_state.get('u_result', 0)
        Q = st.session_state.get('Q_val', 250000)
        A = st.session_state.get('A_val', 10)
        dT = st.session_state.get('dT_val', 50)
        
        st.markdown("---")
        st.subheader("🔄 View U in Different Units")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("W/m²·K", f"{u_result:.4f}")
        c2.metric("W/m²·°C", f"{u_result:.4f}")
        c3.metric("kcal/h·m²·°C", f"{u_result/1.163:.4f}")
        c4.metric("BTU/h·ft²·°F", f"{u_result/5.678:.4f}")
        
        st.markdown("---")
        st.subheader("📊 Sensitivity Analysis (+20% on each input)")
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ['Current U', 'Q+20%', 'A+20%', 'ΔT+20%']
        values = [u_result, (Q*1.2)/(A*dT), Q/((A*1.2)*dT), Q/(A*(dT*1.2))]
        ax.bar(categories, values, color=['#34e89e','#2a5298','#ff6666','#ffcc00'])
        ax.set_ylabel('U (W/m²·K)')
        ax.set_title('How +20% change affects U')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        inputs = {"Q (W)": Q, "A (m²)": A, "ΔT (°C)": dT}
        create_download_section("U", u_result, "W/m²·K", inputs, categories, values, fig)
        plt.close(fig)
    
    elif result_type == "A":
        a_result = st.session_state.get('a_result', 0)
        Q = st.session_state.get('Q_val', 250000)
        U = st.session_state.get('U_val', 500)
        dT = st.session_state.get('dT_val', 50)
        
        st.markdown("---")
        st.subheader("🔄 View Area in Different Units")
        c1, c2, c3 = st.columns(3)
        c1.metric("m²", f"{a_result:.4f}")
        c2.metric("cm²", f"{a_result*10000:.4f}")
        c3.metric("ft²", f"{a_result/0.092903:.4f}")
        
        st.markdown("---")
        st.subheader("📊 Sensitivity Analysis (+20% on each input)")
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ['Current A', 'Q+20%', 'U+20%', 'ΔT+20%']
        values = [a_result, (Q*1.2)/(U*dT), Q/((U*1.2)*dT), Q/(U*(dT*1.2))]
        ax.bar(categories, values, color=["#34e8cd",'#2a5298','#ff6666','#ffcc00'])
        ax.set_ylabel('Area (m²)')
        ax.set_title('How +20% change affects Area')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        inputs = {"Q (W)": Q, "U (W/m²·K)": U, "ΔT (°C)": dT}
        create_download_section("A", a_result, "m²", inputs, categories, values, fig)
        plt.close(fig)
    
    elif result_type == "dT":
        dt_result = st.session_state.get('dt_result', 0)
        Q = st.session_state.get('Q_val', 250000)
        U = st.session_state.get('U_val', 500)
        A = st.session_state.get('A_val', 10)
        
        st.markdown("---")
        st.subheader("🔄 View ΔT in Different Units")
        c1, c2, c3 = st.columns(3)
        c1.metric("°C", f"{dt_result:.4f}")
        c2.metric("K", f"{dt_result+273.15:.4f}")
        c3.metric("°F", f"{(dt_result*9/5)+32:.4f}")
        
        st.markdown("---")
        st.subheader("📊 Sensitivity Analysis (+20% on each input)")
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ['Current ΔT', 'Q+20%', 'U+20%', 'A+20%']
        values = [dt_result, (Q*1.2)/(U*A), Q/((U*1.2)*A), Q/(U*(A*1.2))]
        ax.bar(categories, values, color=['#34e89e',"#2a5d98",'#ff6666','#ffcc00'])
        ax.set_ylabel('ΔT (°C)')
        ax.set_title('How +20% change affects ΔT')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
        
        inputs = {"Q (W)": Q, "U (W/m²·K)": U, "A (m²)": A}
        create_download_section("ΔT", dt_result, "°C", inputs, categories, values, fig)
        plt.close(fig)
    
    with st.expander("📚 Typical U Values"):
        st.markdown("| Fluid Pair | U (W/m²·K) |\n|---|---|\n| Water-Water | 800-1500 |\n| Water-Oil | 100-400 |\n| Steam-Water | 1000-3000 |")
