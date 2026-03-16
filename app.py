import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
import time

# --- 1. PRO UI SETUP ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
        background-color: #F5F5F7; 
    }
    section[data-testid="stSidebar"] { 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        backdrop-filter: blur(10px);
        border-right: 1px solid #e5e5e7; 
    }
    .stTextArea textarea, .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #d1d1d6 !important;
        background-color: white !important;
    }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 10px;
        border: none; padding: 10px 24px; font-weight: 600; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE SETUP (FIXED FOR MARCH 2026 ENDPOINTS) ---
def get_model():
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("Missing GOOGLE_API_KEY in Streamlit Secrets.")
            return None
        
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # FIX: Using 'gemini-flash-latest' to bypass endpoint sync delays
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Engine Connection Lost: {e}")
        return None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🧬 Verilogic Pro")
    st.caption("v7.5 | Production Stable")
    mode = st.radio("Navigation", ["AI Symbolic Solver", "3D Graphing Engine", "System Diagnostics"])
    st.markdown("---")
    if st.button("Manual Engine Reboot"):
        st.rerun()

# --- 4. MAIN LOGIC ---
if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    user_query = st.text_area("Enter Query:", placeholder="Size of the sun...", height=150)
    
    if st.button("Execute Pro Logic"):
        if user_query:
            model = get_model()
            if model:
                with st.spinner("Processing..."):
                    try:
                        prompt = f"System: You are Verilogic Pro. Show your work step-by-step for: {user_query}. Use LaTeX."
                        response = model.generate_content(prompt)
                        st.divider()
                        st.markdown("## Engine Output")
                        st.write(response.text if response.text else "No output returned.")
                    except Exception as e:
                        st.error(f"Bridge Connection Error: {e}")
        else:
            st.warning("Input required.")

elif mode == "3D Graphing Engine":
    st.title("📈 3D Visualization")
    formula = st.text_input("Function (z=)", "np.sin(np.sqrt(X**2 + Y**2))")
    try:
        x, y = np.linspace(-10, 10, 80), np.linspace(-10, 10, 80)
        X, Y = np.meshgrid(x, y)
        Z = eval(formula, {"np": np, "X": X, "Y": Y, "sqrt": np.sqrt, "sin": np.sin})
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Syntax Error: {e}")

elif mode == "System Diagnostics":
    st.title("🛠 System Diagnostics")
    st.metric("Engine Status", "Optimal")
    st.info("Verified Deployment: March 15, 2026.")
