import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. UI SETUP ---
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

# --- 2. ENGINE SETUP (THE ULTIMATE FIX) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # THE REPAIR: We use the FULL system path 'models/gemini-1.5-flash'
    # instead of just 'gemini-1.5-flash'. This is the most reliable way 
    # to stop the 404 'v1beta' error.
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 3. APP INTERFACE ---
st.sidebar.title(" Verilogic Pro")
mode = st.sidebar.selectbox("Navigation", ["AI Symbolic Solver", "3D Graphing Engine"])

if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    user_query = st.text_area("Enter Math or Logic:", placeholder="Size of moon", key="main_input")
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Connecting to Stable Engine..."):
                try:
                    # Execute the request
                    response = model.generate_content(user_query)
                    
                    st.markdown("### Engine Output")
                    if response.text:
                        st.write(response.text)
                    else:
                        st.warning("Empty response received.")
                except Exception as e:
                    # FINAL FAILOVER: If '1.5-flash' still fails, try 'gemini-pro'
                    try:
                        st.info("Retrying with Pro Engine...")
                        alt_model = genai.GenerativeModel('models/gemini-pro')
                        response = alt_model.generate_content(user_query)
                        st.write(response.text)
                    except:
                        st.error(f"Bridge Connection Error: {e}")
                        st.info("If you see 404, check AI Studio to ensure your API Key is 'Active'.")
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
st.sidebar.caption("Verilogic Pro v2.9 | Production Build")
