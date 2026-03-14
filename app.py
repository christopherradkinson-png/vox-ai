import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. APPLE PRO UI (STABLE & LIGHTWEIGHT) ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F5F5F7; }
    
    /* Apple Blue Primary Button */
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 12px;
        width: 100%; border: none; padding: 12px; font-weight: 600;
    }
    
    /* iPhone Style Input Box */
    .stTextArea textarea { 
        border-radius: 12px !important; 
        background-color: #FFFFFF !important; 
        border: 1px solid #d1d1d6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE STABLE ENGINE ---
# Locking to 'gemini-1.5-flash' - it has the highest free quota
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("🔑 API Key Issue in Secrets.")
    st.stop()

# --- 3. APP INTERFACE ---
st.sidebar.title(" Verilogic Pro")
mode = st.sidebar.selectbox("Navigation", ["AI Solver", "3D Graphing"])

if mode == "AI Solver":
    st.title("∫ AI Symbolic Solver")
    
    # We removed the 'value' to ensure the placeholder works correctly
    user_query = st.text_area("Enter Math or Logic:", placeholder="Type your query here...", key="main_input")
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Brain Syncing..."):
                try:
                    response = model.generate_content(user_query)
                    st.markdown("### Engine Output")
                    st.write(response.text)
                except Exception as e:
                    if "429" in str(e):
                        st.error("⏳ Quota Full: Google is cooling down. Please wait 60 seconds and try again.")
                    else:
                        st.error(f"Engine Error: {e}")
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
        st.error("Syntax Error (e.g. use x**2)")
