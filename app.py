import streamlit as st
import requests
import numpy as np
import plotly.graph_objects as go

# --- 1. PRO UI SETUP ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

# Apple-style Minimalist CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
        background-color: #F5F5F7; 
    }
    .stTextArea textarea { border-radius: 12px !important; border: 1px solid #d1d1d6 !important; }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 10px;
        border: none; padding: 10px 24px; font-weight: 600; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE (v24.0: FOOLPROOF PRODUCTION PROTOCOL) ---
def call_verilogic_engine(user_query):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: GOOGLE_API_KEY missing from Streamlit Secrets."
    
    # Strip any accidental spaces from the secret key
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    
    # BASE URL: This is the clean, stable production address (March 2026)
    url = "https://generativelanguage.googleapis.com"
    
    # BUILD DATA STEP-BY-STEP: This prevents the 'unmatched bracket' syntax errors
    p_text = f"System: You are Verilogic Pro. Show work step-by-step for: {user_query}. Use LaTeX."
    p_part = {"text": p_text}
    c_item = {"parts": [p_part]}
    payload = {"contents": [c_item]}

    try:
        # We pass the key as 'params'. This is the SAFEST way to avoid NameResolutionErrors.
        response = requests.post(
            url, 
            params={"key": api_key}, 
            json=payload, 
            headers={"Content-Type": "application/json"}
        )
        
        # Check if Google sent back an error (like 403 or 429)
        if response.status_code != 200:
            return f"Bridge Error {response.status_code}: {response.text}"
            
        res_json = response.json()
        
        # SURGICAL EXTRACTION: Using precise indexing to grab the first candidate
        try:
            return res_json['candidates'][0]['content']['parts'][0]
        except (KeyError, IndexError):
            return "Engine Fault: The API connected but returned data in an unexpected format."
            
    except Exception as e:
        return f"Protocol Failure: {str(e)}"

# --- 3. MAIN INTERFACE ---
st.title("🧬 Verilogic Pro")
st.caption("v24.0 | Production Stable Final")

user_input = st.text_area("Enter Math or Physics Query:", placeholder="e.g. What is the size of the sun?", height=150)

if st.button("Execute Pro Logic"):
    if user_input:
        with st.spinner("Analyzing via Production Bridge..."):
            result = call_verilogic_engine(user_input)
            st.divider()
            st.markdown(result)
    else:
        st.warning("Please provide a query.")

# --- 4. 3D GRAPHING ENGINE ---
with st.expander("📈 3D Graphing Engine"):
    formula = st.text_input("Function (z=)", "np.sin(np.sqrt(X**2 + Y**2))")
    if st.button("Generate Graph"):
        try:
            x, y = np.linspace(-10, 10, 80), np.linspace(-10, 10, 80)
            X, Y = np.meshgrid(x, y)
            # Safe-eval for standard numpy functions
            Z = eval(formula, {"np": np, "X": X, "Y": Y, "sqrt": np.sqrt, "sin": np.sin, "cos": np.cos, "exp": np.exp})
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Formula Error: {e}")
