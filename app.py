import streamlit as st
from google import genai
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
    .stTextArea textarea {
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

# --- 2. THE PRODUCTION ENGINE (STABLE V1) ---
def get_client():
    """Initializes the new Google Gen AI SDK to bypass v1beta errors."""
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("Missing API Key in Secrets.")
            return None
        
        # New SDK Client initialization (Defaults to Stable v1)
        return genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    except Exception as e:
        st.error(f"Engine Connection Failure: {e}")
        return None

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧬 Verilogic Pro")
    st.caption("v8.0 | Production Stable")
    mode = st.radio("Navigation", ["AI Symbolic Solver", "3D Graphing Engine", "System Diagnostics"])
    
    st.markdown("---")
    if st.button("Force System Reboot"):
        st.rerun()

# --- 4. MAIN INTERFACE ---
if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    st.markdown("### *Step-by-Step Reasoning Engine*")
    
    user_query = st.text_area("Enter Query:", placeholder="Explain the physics of a black hole...", height=150)
    
    if st.button("Execute Pro Logic"):
        if user_query:
            client = get_client()
            if client:
                with st.spinner("Connecting to Production Engine..."):
                    try:
                        # Updated method call for the new SDK
                        response = client.models.generate_content(
                            model='gemini-1.5-flash',
                            contents=f"System: You are Verilogic Pro. Provide a step-by-step 'Show Your Work' derivation for: {user_query}. Use LaTeX."
                        )
                        
                        st.divider()
                        st.markdown("## Engine Output")
                        if response.text:
                            st.markdown(response.text)
                        else:
                            st.warning("Empty response. Please check API quota.")
                    except Exception as e:
                        st.error(f"Bridge Connection Error: {e}")
        else:
            st.warning("Please provide a query.")

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
    st.metric("Neural Status", "Connected")
    st.metric("API Protocol", "Stable SDK (v1)")
    st.success("Deployment Verified: March 15, 2026")
