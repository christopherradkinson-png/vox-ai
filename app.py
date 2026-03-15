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
    }
    .stTextArea textarea { border-radius: 14px !important; border: 1px solid #d1d1d6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE HARD-WIRED ENGINE ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # We use 'rest' transport to avoid the gRPC/v1beta mismatch error seen in your screenshot
    genai.configure(api_key=api_key, transport='rest')
    
    # Force the path to the stable production model
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
except Exception as e:
    st.error(f"Vault Connection Error: {e}")
    st.stop()

# --- 3. APP INTERFACE ---
st.sidebar.title(" Verilogic Pro")
mode = st.sidebar.selectbox("Navigation", ["AI Symbolic Solver", "3D Graphing Engine"])

st.sidebar.markdown("---")
st.sidebar.caption("📡 Status: Online")
st.sidebar.caption("🤖 Engine: Gemini 1.5 Flash (Stable)")

if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    
    user_query = st.text_area("Enter Math or Logic:", placeholder="What is the size of the sun?", key="main_input")
    
    if st.button("Execute Pro Logic"):
        if user_query:
            with st.spinner("🧠 Connecting to Production Engine..."):
                try:
                    # Execute the request
                    response = model.generate_content(user_query)
                    
                    st.markdown("### Engine Output")
                    if response.text:
                        st.write(response.text)
                    else:
                        st.warning("No text returned. The query may have been flagged by safety filters.")
                except Exception as e:
                    # Final diagnostic catch
                    st.error(f"Critical Connection Error: {e}")
                    st.info("Ensure your API key is active in Google AI Studio.")
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
st.sidebar.caption("Verilogic Pro v2.7.1 | Clean Build")
