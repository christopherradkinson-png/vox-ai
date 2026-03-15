import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import numpy as np
import sympy as sp

# --- 1. APPLE PRO UI SETUP ---
st.set_page_config(page_title="Verilogic Pro", page_icon="🧬", layout="wide")

# Custom CSS for the "Apple" aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F5F5F7; }
    .stButton > button {
        background-color: #007AFF; color: white; border-radius: 12px;
        width: 100%; border: none; padding: 12px; font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { background-color: #0062CC; border: none; color: white; }
    .stTextArea textarea { border-radius: 14px !important; border: 1px solid #d1d1d6 !important; }
    .stTextInput input { border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE INITIALIZATION ---
try:
    # Use the key from your secrets.toml or Streamlit Cloud Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Using gemini-1.5-flash for speed and reliability
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("🚨 Vault Connection Error")
    st.info("Check your Secrets. Ensure GOOGLE_API_KEY is pasted correctly.")
    st.stop()

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title(" Verilogic Pro")
st.sidebar.markdown("---")
mode = st.sidebar.radio("Navigation", ["AI Symbolic Solver", "3D Graphing Engine"])
st.sidebar.markdown("---")
st.sidebar.caption("📡 System Status: Online")
st.sidebar.caption("🤖 Model: Gemini 1.5 Flash")

# --- 4. MODE: AI SYMBOLIC SOLVER ---
if mode == "AI Symbolic Solver":
    st.title("∫ AI Symbolic Solver")
    st.markdown("##### Solve complex logic, calculus, or general queries using Google's Neural Engine.")
    
    user_query = st.text_area("Input Command:", placeholder="Example: Solve for x: x^2 + 5x + 6 = 0", key="main_input", height=150)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        execute = st.button("Execute Pro Logic")

    if execute:
        if user_query:
            with st.spinner("🧠 Analyzing Logic..."):
                try:
                    # System instruction to ensure clean math formatting
                    prompt = f"Provide a detailed, step-by-step solution. Use LaTeX for math formulas: {user_query}"
                    response = model.generate_content(prompt)
                    
                    st.markdown("### Engine Output")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Google Server Error: {e}")
                    st.info("Tip: If you see a 404, check if the API key was created in a 'New Project' as discussed.")
        else:
            st.warning("Please enter a query to proceed.")

# --- 5. MODE: 3D GRAPHING ENGINE ---
elif mode == "3D Graphing Engine":
    st.title("📈 3D Visualization")
    st.markdown("##### Render mathematical surfaces in real-time.")
    
    formula = st.text_input("Define Surface (z = )", "np.sin(np.sqrt(X**2 + Y**2))")
    
    try:
        # Generate grid
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)
        
        # Evaluate formula safely
        # Note: We use np prefix in the default to guide the user
        Z = eval(formula)
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        
        fig.update_layout(
            title='Surface Plot',
            autosize=True,
            margin=dict(l=0, r=0, b=0, t=40),
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Syntax Error: {e}")
        st.info("Hint: Use 'np.' before math functions. Example: np.sin(X) * np.cos(Y)")

# --- 6. FOOTER ---
st.markdown("---")
st.caption("Verilogic Pro v2.0 | Built with Streamlit & Google AI Studio")
