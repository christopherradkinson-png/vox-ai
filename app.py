import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
import sympy

# --- 1. PRO APPLE UI (REPAIRED & STABLE) ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 12px;
        width: 100%; border: none; padding: 12px; font-weight: 600;
    }
    .stTextArea textarea { border-radius: 12px !important; background-color: #F2F2F7 !important; }
    /* Fix for the "Ghost" placeholder text */
    .stTextArea textarea::placeholder { color: #8E8E93 !important; opacity: 1; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SELF-HEALING ENGINE ---
@st.cache_resource
def initialize_engine():
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # DYNAMIC REPAIR: We ask Google for the list of working models
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # We prioritize 'flash' for speed, then 'pro'
        for model_path in available_models:
            if 'gemini-1.5-flash' in model_path: return genai.GenerativeModel(model_path)
            if 'gemini-pro' in model_path: return genai.GenerativeModel(model_path)
        
        # Fallback to the first one available if others fail
        return genai.GenerativeModel(available_models[0])
    except Exception as e:
        st.error(f"🔑 Vault Connection Failed: {e}")
        return None

model = initialize_engine()

# --- 3. APP INTERFACE ---
st.sidebar.title(" Verilogic Pro")
mode = st.sidebar.selectbox("Navigation", ["AI Symbolic Solver", "3D Graphing"])

if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    
    # Using a unique key to fix the placeholder/input freeze
    user_query = st.text_area("Enter Math or Logic:", placeholder="What is the size of the sun?", key="main_input")
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Brain Syncing..."):
                try:
                    response = model.generate_content(user_query)
                    st.markdown("### Engine Output")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Engine Error: {e}")
                    st.info("Try clicking the button again in 5 seconds.")
        else:
            st.warning("Please enter a query.")

elif mode == "3D Graphing":
    st.title("📈 3D Visualization")
    formula = st.text_input("z = ", "sin(x) * cos(y)")
    try:
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = eval(formula.replace('sin', 'np.sin').replace('cos', 'np.cos').replace('^', '**'))
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Syntax Error (e.g. use x**2 for x²)")
