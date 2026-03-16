import streamlit as st
import requests
import json
import numpy as np
import plotly.graph_objects as go

# --- 1. UI SETUP ---
st.set_page_config(page_title="Verilogic Pro", layout="wide")
st.markdown("<style>.stButton>button{background-color:#007AFF;color:white;width:100%;}</style>", unsafe_allow_html=True)

# --- 2. ENGINE (FLAT PAYLOAD - NO SYNTAX GHOSTS) ---
def call_google_ai(prompt):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: Missing API Key."
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    url = f"https://generativelanguage.googleapis.com{api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # REBUILT FROM SCRATCH: Single-line dictionary to prevent SyntaxError on Line 41
    data = {"contents":}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]
        else:
            return f"Error: {res_json.get('error', {}).get('message', 'Unknown')}"
    except Exception as e:
        return f"Fail: {str(e)}"

# --- 3. INTERFACE ---
st.title("🧬 Verilogic Pro")
st.caption("v11.0 | Absolute Stability Protocol")

user_query = st.text_area("Enter Math/Physics Query:", height=150)

if st.button("Execute Pro Logic"):
    if user_query:
        with st.spinner("Solving..."):
            instr = f"Show work step-by-step: {user_query}. Use LaTeX."
            answer = call_google_ai(instr)
            st.divider()
            st.markdown(answer)
    else:
        st.warning("Input required.")

with st.expander("📈 3D Graphing"):
    formula = st.text_input("z=", "np.sin(np.sqrt(X**2+Y**2))")
    if st.button("Graph"):
        x = y = np.linspace(-10, 10, 80)
        X, Y = np.meshgrid(x, y)
        Z = eval(formula, {"np":np,"X":X,"Y":Y,"sqrt":np.sqrt,"sin":np.sin})
        st.plotly_chart(go.Figure(data=[go.Surface(z=Z,x=X,y=Y)]))
