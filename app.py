import streamlit as st
import requests
import numpy as np
import plotly.graph_objects as go

# --- 1. PRO UI SETUP ---
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

# --- 2. THE ENGINE (v19.0: PATH CORRECTED) ---
def call_verilogic_engine(user_input):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: GOOGLE_API_KEY missing from Streamlit Secrets."
    
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    
    # CORRECTED MARCH 2026 PRODUCTION URL
    # We use v1beta but with the explicitly stable 'flash' model path
    url = f"https://generativelanguage.googleapis.com{api_key}"
    
    payload = {
        "contents":
        }]
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # If we get another 404, we catch the HTML and show a clean message
        if response.status_code != 200:
            return f"BRIDGE ERROR {response.status_code}: Google refused the connection. Please verify your API Key is active in Google AI Studio."
            
        data = response.json()
        
        # Surgical extraction of the answer
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]
        else:
            return "Engine connected but returned no logic. Check your safety settings in Google AI Studio."
            
    except Exception as e:
        return f"Protocol Failure: {str(e)}"

# --- 3. MAIN INTERFACE ---
st.title("🧬 Verilogic Pro")
st.caption("v19.0 | Production URL Fixed")

query = st.text_area("Enter Math or Physics Query:", placeholder="What is the size of the sun?", height=150)

if st.button("Execute Pro Logic"):
    if query:
        with st.spinner("Analyzing via Production Bridge..."):
            result = call_verilogic_engine(query)
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
