import streamlit as st
import numpy as np
import plotly.graph_objects as go
import google.generativeai as genai

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Verilogic Pro",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------
# CONFIGURE GEMINI
# -----------------------------
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("GOOGLE_API_KEY missing from Streamlit secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# FIX: Using 'gemini-1.5-flash' with the explicit 'models/' prefix 
# or 'gemini-flash-latest' forces the SDK to bypass the deprecated v1beta path.
MODEL_ID = "gemini-1.5-flash" 
model = genai.GenerativeModel(MODEL_ID)

# -----------------------------
# UI STYLE
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #F5F5F7;
}

.stTextArea textarea {
    border-radius: 12px !important;
    border: 1px solid #d1d1d6 !important;
}

.stButton > button {
    background-color: #007AFF;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# AI ENGINE
# -----------------------------
def call_verilogic_engine(query):
    try:
        prompt = f"""
You are Verilogic Pro, an advanced scientific calculator.
Solve the following problem step-by-step.

Problem:
{query}
"""
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # Improved error reporting to catch exactly what the API says
        return f"AI Error: {str(e)}"

# -----------------------------
# MAIN INTERFACE
# -----------------------------
st.title("🧬 Verilogic Pro")
st.caption("Advanced AI Scientific & Mathematical Engine")

query = st.text_area(
    "Enter Math or Physics Query:",
    placeholder="Example: What is the diameter of the Sun?",
    height=150
)

if st.button("Execute Pro Logic"):
    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        with st.spinner("Running AI engine..."):
            result = call_verilogic_engine(query)
        st.divider()
        st.markdown(result)

# -----------------------------
# 3D GRAPHING ENGINE
# -----------------------------
with st.expander("📈 3D Graphing Engine"):
    formula = st.text_input(
        "Function z = f(x,y)",
        "np.sin(np.sqrt(X**2 + Y**2))"
    )

    if st.button("Generate Graph"):
        try:
            x = np.linspace(-10, 10, 80)
            y = np.linspace(-10, 10, 80)
            X, Y = np.meshgrid(x, y)

            safe_env = {
                "np": np,
                "X": X,
                "Y": Y,
                "sin": np.sin,
                "cos": np.cos,
                "sqrt": np.sqrt,
                "exp": np.exp
            }

            Z = eval(formula, {"__builtins__": {}}, safe_env)
            fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Graph error: {e}")
