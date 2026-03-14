import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. APPLE PRO UI ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F5F5F7; }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 12px;
        width: 100%; border: none; padding: 12px; font-weight: 600;
    }
    .stTextArea textarea { 
        border-radius: 14px !important; 
        background-color: #FFFFFF !important; 
        border: 1px solid #d1d1d6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE DIRECT ENGINE ---
try:
    # Get key from secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Using the most universally accepted stable name
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Vault Connection Error: {e}")
    st.stop()

# --- 3. APP INTERFACE ---
st.sidebar.title(" Verilogic Pro")
mode = st.sidebar.selectbox("Navigation", ["AI Symbolic Solver", "3D Graphing Engine"])

if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    
    user_query = st.text_area("Enter Math or Logic:", placeholder="What is the size of the sun?", key="main_input")
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Connecting to Google Brain..."):
                try:
                    # Direct attempt
                    response = model.generate_content(user_query)
                    st.markdown("### Engine Output")
                    st.write(response.text)
                except Exception as e:
                    # This captures the EXACT Google error if it still fails
                    st.error(f"Google Server Error: {e}")
                    st.info("Tip: If you see '404', your API key is likely restricted. Try creating a NEW key in AI Studio.")
        else:
            st.warning("Please enter a query.")

elif mode == "3D Graphing Engine":
    st.title("📈 3D Visualization")
    formula = st.text_input("z = ", "sin(x) * cos(y)")
    try:
        x, y = np.linspace(-5, 5, 50), np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = eval(formula.replace('sin', 'np.sin').replace('cos', 'np.cos').replace('^', '**'))
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Check syntax.")

st.sidebar.markdown("---")
st.sidebar.caption("📡 Status: Online")
