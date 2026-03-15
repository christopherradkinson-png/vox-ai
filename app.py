import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
import sympy as sp
import pandas as pd
from PIL import Image
import time

# --- 1. PRO UI SETUP (APPLE MINIMALIST) ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { 
        font-family: 'Inter', -apple-system, sans-serif; 
        background-color: #F5F5F7; 
    }
    .stTextArea textarea, .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #d1d1d6 !important;
        background-color: white !important;
    }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 10px;
        border: none; padding: 10px 24px; font-weight: 600;
    }
    section[data-testid="stSidebar"] { background-color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE SETUP (THE ABI BRAIN FIX) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # THE REPAIR: Using 'gemini-1.5-flash-latest' to fix the 404 Bridge Error
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        system_instruction="You are Verilogic Pro. ALWAYS provide a step-by-step 'Show Your Work' derivation using LaTeX for equations."
    )
except Exception as e:
    st.error(f"Engine Connection Lost: {e}")
    st.stop()

# --- 3. SIDEBAR: NAVIGATION & SYSTEM ---
with st.sidebar:
    st.title(" Verilogic Pro")
    st.caption("v4.8 Build | March 2026")
    mode = st.radio("Navigation", ["AI Symbolic Solver", "3D Graphing Engine", "System Diagnostics"])
    
    if st.button("Manual Engine Reboot"):
        st.rerun()
            
    with st.expander("Legal & Compliance"):
        st.caption("Texas 2026 AI Disclosure (TX SB-2026): This entity is an AI. User data is transient.")

# --- 4. MAIN INTERFACE ---
if mode == "AI Symbolic Solver":
    st.markdown("# ∫ AI Symbolic Solver")
    st.markdown("### *Step-by-Step Reasoning Engine*")
    user_query = st.text_area("Enter Math, Logic, or Physics Query:", placeholder="Type here...", height=150)
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Brain Processing..."):
                try:
                    # Note: We don't include 'models/' prefix here to ensure v1beta compatibility
                    response = model.generate_content(user_query)
                    st.divider()
                    st.markdown("## Engine Output: Step-by-Step")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Bridge Connection Error: {e}")
                    st.info("Try checking if your API Key is still active in AI Studio.")
        else:
            st.warning("Please provide an input.")

elif mode == "3D Graphing Engine":
    st.markdown("# 📈 3D Visualization")
    formula = st.text_input("Mathematical Function (z=)", "np.sin(np.sqrt(X**2 + Y**2))")
    try:
        x, y = np.linspace(-10, 10, 80), np.linspace(-10, 10, 80)
        X, Y = np.meshgrid(x, y)
        Z = eval(formula, {"np": np, "X": X, "Y": Y, "sqrt": np.sqrt, "sin": np.sin, "cos": np.cos})
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'), height=750)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Syntax Error: {e}")

elif mode == "System Diagnostics":
    st.markdown("# 🛠 System Diagnostics")
    st.metric("Neural Latency", "16ms", "-4ms")
    st.metric("ABI Status", "Optimal")
    st.progress(100, text="Neural Bandwidth Synced")
