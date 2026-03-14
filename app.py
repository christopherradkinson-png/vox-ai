import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
import sympy
import pandas as pd

# --- 1. CLEAN APPLE PRO UI (STABLE VERSION) ---
def apply_clean_theme():
    st.markdown("""
    <style>
    /* San Francisco Style Font */
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Clean Blue Buttons (Apple Blue) */
    div.stButton > button {
        background-color: #007AFF;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        width: 100%;
    }
    
    /* Fixing the "Ghost Text" / Placeholder Issue */
    .stTextArea textarea {
        background-color: #F2F2F7 !important;
        color: #1C1C1E !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE HANDSHAKE ---
# This version uses a direct, stable call to avoid the 404/Red Error
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Using the most globally compatible model name for 2026
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("🔑 API Key Missing or Invalid in Secrets.")
    st.stop()

# --- 3. APP STRUCTURE ---
apply_clean_theme()
st.sidebar.title(" Verilogic Pro")
app_mode = st.sidebar.selectbox("Navigation", ["AI CAS Solver", "3D Graphing", "Matrix Engine"])

# --- MODULE: AI CAS SOLVER ---
if app_mode == "AI CAS Solver":
    st.title("∫ AI Symbolic Solver")
    
    # Input Area - Fixed Placeholder
    math_query = st.text_area("Enter Math or Logic:", value="", placeholder="e.g., integrate(sin(x)) or Calculate the size of the moon", height=150)
    
    if st.button("Execute Pro Logic"):
        if math_query:
            with st.spinner("🧠 Analyzing..."):
                try:
                    # Clearer prompt to ensure no formatting errors
                    response = model.generate_content(f"Solve this accurately and show steps: {math_query}")
                    st.markdown("### Engine Output")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Engine Error: {e}")
        else:
            st.warning("Please enter a query first.")

# --- MODULE: 3D GRAPHING ---
elif app_mode == "3D Graphing":
    st.title("📈 3D Visualization")
    formula = st.text_input("z = ", "sin(x) * cos(y)")
    try:
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = eval(formula.replace('sin', 'np.sin').replace('cos', 'np.cos').replace('^', '**'))
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Check Math Syntax (e.g., use x**2 for x²)")

st.sidebar.markdown("---")
st.sidebar.caption("System Status: **Active**")
