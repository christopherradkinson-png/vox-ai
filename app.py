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

# --- 2. THE ENGINE (PRODUCTION V1 PROTOCOL) ---
def call_verilogic_engine(user_input):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: GOOGLE_API_KEY missing from Streamlit Secrets."
    
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    
    # UPGRADED TO V1 PRODUCTION STABLE
    url = "https://generativelanguage.googleapis.com"
    
    # System instructions for 'Show Your Work'
    full_prompt = f"System: You are Verilogic Pro. Provide a step-by-step 'Show Your Work' derivation for: {user_input}. Use LaTeX for all mathematical notation."
    
    # Payload Construction (Verified Structure)
    payload = {
        "contents":
        }]
    }

    try:
        response = requests.post(url, params={"key": api_key}, json=payload)
        
        # Check if the connection itself worked
        if response.status_code != 200:
            return f"Bridge Error {response.status_code}: {response.text}"
            
        response_data = response.json()
        
        # RESPONSE GUARD: Safely navigating the Google API JSON tree
        if 'candidates' in response_data:
            # Getting the text from the first candidate
            text_output = response_data['candidates'][0]['content']['parts'][0]
            return text_output
        else:
            return "The engine connected but didn't return a result. Check your API quota."
            
    except Exception as e:
        return f"System Connection Failed: {str(e)}"

# --- 3. MAIN INTERFACE ---
st.title("🧬 Verilogic Pro")
st.caption("v16.0 | Production V1 Stable")

query = st.text_area("Enter Math or Physics Query:", placeholder="What is the size of the sun?", height=150)

if st.button("Execute Pro Logic"):
    if query:
        with st.spinner("Calculating via Production Bridge..."):
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
            Z = eval(formula, {"np": np, "X": X, "Y": Y, "sqrt": np.sqrt, "sin": np.sin, "cos": np.cos, "exp": np.exp})
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Formula Error: {e}")
