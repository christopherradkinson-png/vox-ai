import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
import sympy
import pandas as pd
from PIL import Image
from fpdf import FPDF
import io

# --- 1. APPLE "LIQUID GLASS" DESIGN SYSTEM ---
def apply_apple_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F5F5F7;
    }
    
    /* Frosted Glass Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Main Apple Card */
    .block-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 40px !important;
        margin-top: 20px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px rgba(0,0,0,0.05);
    }

    /* Rounded Apple Buttons */
    div.stButton > button {
        background: #007AFF;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background: #0056b3;
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE ENGINE AUTH ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # 2026 Stable Model
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🔑 Vault Error: API Key missing or invalid.")
    st.stop()

# --- 3. SIDEBAR NAVIGATION & SETTINGS ---
apply_apple_ui()

st.sidebar.title(" Verilogic Pro")
st.sidebar.caption("v126.0 | Pro Intelligence")

# Navigation
app_mode = st.sidebar.radio("Navigation", 
    ["AI CAS Solver", "3D Graphing Engine", "Matrix & Linear Algebra", "Unit Converter Pro"])

# Integrated Settings Menu
with st.sidebar.expander("⚙️ System Settings"):
    st.write("Engine Customization")
    ai_precision = st.select_slider("AI Precision", options=["Creative", "Balanced", "Exact"], value="Exact")
    ui_glass = st.toggle("Liquid Glass UI", value=True)
    if st.button("Purge Cache"):
        st.cache_data.clear()
        st.toast("System cache cleared.")

# --- 4. MODULES ---

# MODULE: AI CAS SOLVER (WOLFRAM STYLE)
if app_mode == "AI CAS Solver":
    st.title("∫ AI Symbolic Solver")
    st.markdown("Enter any mathematical expression for a **Step-by-Step** analysis.")
    
    math_input = st.text_area("Input Expression:", "integrate(sin(x) * exp(x), x)", help="Use Python syntax: x**2 for x²")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Solve Step-by-Step"):
            with st.spinner("Analyzing Logic..."):
                response = model.generate_content(f"Solve this math problem step-by-step using LaTeX for the formulas: {math_input}")
                st.markdown(response.text)
    
    with col2:
        if st.button("Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Verilogic Pro Math Report", ln=True, align='C')
            pdf.multi_cell(0, 10, txt=f"Expression: {math_input}")
            st.download_button("Download Result", data=pdf.output(dest='S').encode('latin-1'), file_name="math_report.pdf")

# MODULE: 3D GRAPHING (DESMOS STYLE)
elif app_mode == "3D Graphing Engine":
    st.title("📈 3D Graphing Engine")
    formula = st.text_input("Function z = f(x, y)", "sin(sqrt(x**2 + y**2))")
    
    # Grid Generation
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    
    try:
        # Safe eval for math
        Z = eval(formula.replace('sin', 'np.sin').replace('sqrt', 'np.sqrt').replace('cos', 'np.cos'))
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Blues')])
        fig.update_layout(
            title=f'Surface Plot: {formula}',
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
            width=800, height=700,
            margin=dict(l=0, r=0, b=0, t=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Syntax Error: {e}")

# MODULE: MATRIX & LINEAR ALGEBRA
elif app_mode == "Matrix & Linear Algebra":
    st.title("🔢 Matrix Engine")
    st.write("Enter your matrix rows separated by commas.")
    
    raw_m = st.text_area("Matrix A", "1, 0, 0\n0, 1, 0\n0, 0, 1")
    
    if st.button("Calculate Determinant"):
        try:
            matrix_a = np.array([list(map(float, row.split(','))) for row in raw_m.split('\n')])
            det = np.linalg.det(matrix_a)
            st.metric("Determinant", f"{det:.4f}")
            st.write("Inverse Matrix:")
            st.write(np.linalg.inv(matrix_a))
        except:
            st.error("Please ensure the matrix is square and formatted correctly.")

# MODULE: UNIT CONVERTER PRO
elif app_mode == "Unit Converter Pro":
    st.title("⚖️ Precision Converter")
    
    val = st.number_input("Value to Convert", value=1.0)
    category = st.selectbox("Category", ["Length", "Mass", "Temperature"])
    
    if category == "Length":
        units = {"Meters to Feet": 3.28084, "Feet to Meters": 0.3048, "KM to Miles": 0.621371}
        mode = st.selectbox("Conversion", list(units.keys()))
        st.subheader(f"Result: {val * units[mode]:.4f}")

st.sidebar.markdown("---")
st.sidebar.caption("📡 System Status: Online")
