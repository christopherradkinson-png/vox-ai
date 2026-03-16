import streamlit as st
import requests
import json
import numpy as np
import plotly.graph_objects as go

# --- 1. PRO UI SETUP (APPLE MINIMALIST) ---
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
    .stTextArea textarea { border-radius: 12px !important; }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 10px;
        border: none; padding: 10px 24px; font-weight: 600; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DIRECT ENGINE (BYPASSING BUGGY LIBRARIES) ---
def call_google_ai(prompt):
    """Calls Google AI directly via REST to bypass the 404 v1beta library bug."""
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: Missing API Key in Secrets."
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    # FORCE PRODUCTION V1 URL
    url = f"https://generativelanguage.googleapis.com{api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"System Error {response.status_code}: {response_data.get('error', {}).get('message', 'Unknown Error')}"
    except Exception as e:
        return f"Direct Connection Failed: {e}"

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🧬 Verilogic Pro")
    st.caption("v9.0 | Direct Protocol Stable")
    mode = st.radio("Navigation", ["AI Symbolic Solver", "3D Graphing Engine"])
    st.markdown("---")
    if st.button("Re-Sync System"):
        st.rerun()

# --- 4. MAIN INTERFACE ---
if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    user_query = st.text_area("Enter Query:", placeholder="e.g. Solve for x: 2x + 5 = 15", height=150)
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("Executing via Direct Production Bridge..."):
                # Integrated 'Show Your Work' Instruction
                enhanced_prompt = f"System: You are Verilogic Pro. Show your work step-by-step for: {user_query}. Use LaTeX."
                answer = call_google_ai(enhanced_prompt)
                
                st.divider()
                st.markdown("## Engine Output")
                st.markdown(answer)
        else:
            st.warning("Please enter a query.")

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
