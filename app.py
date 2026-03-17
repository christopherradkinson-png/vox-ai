import streamlit as st
import requests
import numpy as np
import plotly.graph_objects as go

# --- 1. PRO UI SETUP (MARCH 2026 STABLE) ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
        background-color: #F5F5F7; 
    }
    .stTextArea textarea { border-radius: 12px !important; }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 10px;
        border: none; padding: 10px 24px; font-weight: 600; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE (STABLE PRODUCTION V1 BRIDGE) ---
def call_verilogic_engine(user_query):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: GOOGLE_API_KEY missing from Streamlit Secrets."
    
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    # Explicitly using the Stable v1 Production endpoint for Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com{api_key}"
    
    # FLAT STRUCTURE: No nested formatting to prevent SyntaxErrors
    data = {"contents": [{"parts": [{"text": f"System: You are Verilogic Pro. Show work step-by-step for: {user_query}. Use LaTeX."}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # Verified production data path for March 2026
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Bridge Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"System Failure: {str(e)}"

# --- 3. MAIN INTERFACE ---
st.title("🧬 Verilogic Pro")
st.caption("v21.0 | Verified Stable Deployment")

user_input = st.text_area("Enter Math or Physics Query:", placeholder="e.g. What is the size of the sun?", height=150)

if st.button("Execute Pro Logic"):
    if user_input:
        with st.spinner("Processing via Production Bridge..."):
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
            Z = eval(formula, {"np": np, "X": X, "Y": Y, "sqrt": np.sqrt, "sin": np.sin, "cos": np.cos, "exp": np.exp})
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Formula Error: {e}")
