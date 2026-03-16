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

# --- 2. THE ENGINE (REST PROTOCOL V1) ---
def call_verilogic_engine(user_input):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: GOOGLE_API_KEY missing from Streamlit Secrets."
    
    # Use clean variables to prevent URL mangling
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    url = "https://generativelanguage.googleapis.com"
    
    # We use 'params' so the library handles the '?' and 'key=' safely
    params = {"key": api_key}
    
    # Build the prompt with the "Show Your Work" instruction
    full_prompt = f"System: You are Verilogic Pro. Provide a step-by-step 'Show Your Work' derivation for: {user_input}. Use LaTeX for all math."
    
    # Constructing the JSON payload using standard Python dictionaries
    # This prevents the 'unmatched bracket' syntax errors
    payload = {
        "contents":
            }
        ]
    }

    try:
        response = requests.post(url, params=params, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            # Safely navigate the candidates list
            return response_data['candidates'][0]['content']['parts'][0]
        else:
            error_msg = response_data.get('error', {}).get('message', 'Unknown API error.')
            return f"API Error {response.status_code}: {error_msg}"
    except Exception as e:
        return f"System Connection Failed: {str(e)}"

# --- 3. MAIN INTERFACE ---
st.title("🧬 Verilogic Pro")
st.caption("v14.0 | Protocol Finalized")

query = st.text_area("Enter Math or Physics Query:", placeholder="e.g. What is the size of the sun?", height=150)

if st.button("Execute Pro Logic"):
    if query:
        with st.spinner("Processing Logic..."):
            result = call_verilogic_engine(query)
            st.divider()
            st.markdown(result)
    else:
        st.warning("Please enter a query.")

# --- 4. 3D GRAPHING ENGINE ---
with st.expander("📈 3D Graphing Engine"):
    formula = st.text_input("Function (z=)", "np.sin(np.sqrt(X**2 + Y**2))")
    if st.button("Generate Graph"):
        try:
            x, y = np.linspace(-10, 10, 80), np.linspace(-10, 10, 80)
            X, Y = np.meshgrid(x, y)
            # Safe eval for basic math
            Z = eval(formula, {"np": np, "X": X, "Y": Y, "sqrt": np.sqrt, "sin": np.sin, "cos": np.cos, "exp": np.exp})
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Formula Error: {e}")
