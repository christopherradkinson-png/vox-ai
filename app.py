import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
import requests
import json

# --- 1. APPLE PRO UI SETUP ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F5F5F7; }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 12px;
        width: 100%; border: none; padding: 12px; font-weight: 600;
    }
    .stTextArea textarea { border-radius: 14px !important; border: 1px solid #d1d1d6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE DIRECT BRIDGE ENGINE ---
# We use a direct POST request to bypass the 'v1beta' library bug
def call_google_ai(prompt, api_key):
    # This URL is the "Stable v1" production endpoint
    url = f"https://generativelanguage.googleapis.com{api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# --- 3. APP INTERFACE ---
st.sidebar.title(" Verilogic Pro")
mode = st.sidebar.selectbox("Navigation", ["AI Symbolic Solver", "3D Graphing Engine"])

st.sidebar.markdown("---")
st.sidebar.caption("📡 Status: Online")
st.sidebar.caption("🤖 Engine: Gemini 1.5 Flash (Direct Bridge)")

if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    
    user_query = st.text_area("Enter Math or Logic:", placeholder="What is the size of the moon?", key="main_input")
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Crossing the Bridge to Google Brain..."):
                try:
                    # Get the key and call our custom bridge function
                    api_key = st.secrets["GOOGLE_API_KEY"]
                    result = call_google_ai(user_query, api_key)
                    
                    st.markdown("### Engine Output")
                    st.write(result)
                except Exception as e:
                    st.error(f"Bridge Connection Error: {e}")
                    st.info("Check your API key in Streamlit Secrets.")
        else:
            st.warning("Please enter a query.")

elif mode == "3D Graphing Engine":
    st.title("📈 3D Visualization")
    formula = st.text_input("z = ", "np.sin(np.sqrt(X**2 + Y**2))")
    try:
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = eval(formula, {"np": np, "X": X, "Y": Y})
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Syntax Error: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("Verilogic Pro v2.8 | Direct Bridge Build")
