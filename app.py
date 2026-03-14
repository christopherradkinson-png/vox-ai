import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
import sympy
import pandas as pd

# --- 1. APPLE PRO UI (STABLE & LIQUID) ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F5F5F7; }
    
    /* Apple Blue Primary Button */
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 12px;
        width: 100%; border: none; padding: 12px; font-weight: 600;
        transition: 0.2s ease;
    }
    .stButton > button:hover { background-color: #0062CC; transform: scale(0.99); }
    
    /* iPhone Style Input Box - Fixing the "Ghost Text" */
    .stTextArea textarea { 
        border-radius: 14px !important; 
        background-color: #FFFFFF !important; 
        border: 1px solid #d1d1d6 !important;
        color: #1c1c1e !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE MODEL-FLEX ENGINE (RE-SYNCED) ---
@st.cache_resource
def load_engine():
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # We try these in order of modern stability for 2026
        for model_name in ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(model_name)
                # Quick ghost-call to verify it exists
                m.generate_content("ping", generation_config={"max_output_tokens": 1})
                return m
            except:
                continue
        return None
    except Exception as e:
        return f"Error: {e}"

model = load_engine()

# --- 3. APP INTERFACE ---
st.sidebar.title(" Verilogic Pro")
st.sidebar.caption("System v130.0 | Pro Intelligence")

mode = st.sidebar.selectbox("Navigation", ["AI Symbolic Solver", "3D Graphing Engine"])

if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    
    # Empty string for value ensures placeholder dissolves correctly
    user_query = st.text_area("Enter Math or Logic:", placeholder="What is the size of the sun?", key="main_input", value="")
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Brain Syncing..."):
                if isinstance(model, str):
                    st.error(f"Vault Connection Failed: {model}")
                elif model is None:
                    st.error("❌ 404: Google Model Not Found. Please check API Key permissions.")
                else:
                    try:
                        response = model.generate_content(user_query)
                        st.markdown("### Engine Output")
                        st.write(response.text)
                    except Exception as e:
                        if "429" in str(e):
                            st.error("⏳ Quota Exceeded: Please wait 60 seconds for Google to reset.")
                        else:
                            st.error(f"Engine Error: {e}")
        else:
            st.warning("Please enter a query.")

elif mode == "3D Graphing Engine":
    st.title("📈 3D Visualization")
    formula = st.text_input("z = ", "sin(x) * cos(y)")
    try:
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = eval(formula.replace('sin', 'np.sin').replace('cos', 'np.cos').replace('sqrt', 'np.sqrt').replace('^', '**'))
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Math Error: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("📡 Status: Online")
