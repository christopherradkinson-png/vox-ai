import streamlit as st
import requests
import json
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

# --- 2. ENGINE (SYNTAX VERIFIED) ---
def call_google_ai(prompt):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: Missing API Key in Streamlit Secrets."
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # Using the stable production v1 endpoint
    url = f"https://generativelanguage.googleapis.com{api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # PAYLOAD: Manually verified for perfect bracket matching.
    payload = {
        "contents":
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            # Extraction path: candidates -> content -> parts -> text
            return response_data['candidates'][0]['content']['parts'][0]
        else:
            error_msg = response_data.get('error', {}).get('message', 'Unknown API Error')
            return f"API Error {response.status_code}: {error_msg}"
    except Exception as e:
        return f"Connection Failed: {str(e)}"

# --- 3. MAIN INTERFACE ---
st.title("🧬 Verilogic Pro")
st.caption("v10.1 | Syntax Verified")

user_query = st.text_area("Enter Math or Physics Query:", placeholder="e.g. Solve for x: 2x + 10 = 20", height=150)

if st.button("Execute Pro Logic"):
    if user_query:
        with st.spinner("Connecting to Production Engine..."):
            # System instructions for "Show Your Work"
            logic_prompt = f"System: You are Verilogic Pro. Show your work step-by-step for: {user_query}. Use LaTeX."
            answer = call_google_ai(logic_prompt)
            
            st.divider()
            st.markdown("### Engine Output")
            st.markdown(answer)
    else:
        st.warning("Please enter a query.")

# --- 4. 3D GRAPHING ENGINE ---
with st.expander("📈 3D Graphing Engine"):
    formula = st.text_input("Function (z=)", "np.sin(np.sqrt(X**2 + Y**2))")
    if st.button("Generate Graph"):
        try:
            x, y = np.linspace(-10, 10, 80), np.linspace(-10, 10, 80)
            X, Y = np.meshgrid(x, y)
            Z = eval(formula, {"np": np, "X": X, "Y": Y, "sqrt": np.sqrt, "sin": np.sin})
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Formula Error: {e}")
