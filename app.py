import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np

# --- 1. APPLE PRO UI SETUP ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F5F5F7; }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 12px;
        width: 100%; border: none; padding: 12px; font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { background-color: #0062CC; color: white; }
    .stTextArea textarea { border-radius: 14px !important; border: 1px solid #d1d1d6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE DIRECT ENGINE (STABLE REPAIR) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # REPAIR: We explicitly tell the library to use the stable 'v1' API
    # instead of 'v1beta' which was causing your 404 error.
    genai.configure(api_key=api_key, transport='rest') 
    
    model_name = 'gemini-1.5-flash'
    model = genai.GenerativeModel(model_name)
    
except Exception as e:
    st.error(f"Vault Connection Error: {e}")
    st.stop()

# --- 3. APP INTERFACE ---
st.sidebar.title(" Verilogic Pro")
mode = st.sidebar.selectbox("Navigation", ["AI Symbolic Solver", "3D Graphing Engine"])

st.sidebar.markdown("---")
st.sidebar.caption("📡 Status: Online")
st.sidebar.caption(f"🤖 Engine: {model_name} (Stable)")

if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    
    user_query = st.text_area("Enter Math or Logic:", placeholder="Example: What is the size of the sun?", key="main_input")
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Connecting to Google Neural Engine..."):
                try:
                    # Execute the request
                    response = model.generate_content(user_query)
                    st.markdown("### Engine Output")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Google Server Error: {e}")
                    st.info("If this persists, go to AI Studio and ensure you clicked 'Create API key in NEW project'.")
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
        st.info("Tip: Use 'np.' for functions (e.g., np.cos(X))")

st.sidebar.markdown("---")
st.sidebar.caption("Verilogic Pro v2.3 | March 2026")
