import streamlit as st
import requests
import numpy as np
import plotly.graph_objects as go

# -----------------------------
# 1. PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Verilogic Pro",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------
# 2. UI STYLE
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
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 3. AI ENGINE
# -----------------------------
def call_verilogic_engine(user_query):

    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ GOOGLE_API_KEY missing from Streamlit Secrets."

    api_key = st.secrets["GOOGLE_API_KEY"].strip()

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
You are Verilogic Pro — an advanced AI scientific calculator.

Solve the following problem step-by-step.
Use LaTeX formatting for equations.

Problem:
{user_query}
"""
                    }
                ]
            }
        ]
    }

    try:

        response = requests.post(
            url,
            params={"key": api_key},
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            return f"⚠️ API Error {response.status_code}: {response.text}"

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Connection Failure: {str(e)}"

# -----------------------------
# 4. MAIN APP
# -----------------------------
st.title("🧬 Verilogic Pro")
st.caption("Advanced AI Scientific & Mathematical Engine")

user_input = st.text_area(
    "Enter Math or Physics Query:",
    placeholder="Example: What is the Schwarzschild radius of Earth?",
    height=150
)

if st.button("Execute Pro Logic"):

    if user_input.strip() == "":
        st.warning("Please enter a query.")

    else:
        with st.spinner("Analyzing via Verilogic AI Engine..."):

            result = call_verilogic_engine(user_input)

        st.divider()
        st.markdown(result)

# -----------------------------
# 5. 3D GRAPH ENGINE
# -----------------------------
with st.expander("📈 3D Graphing Engine"):

    formula = st.text_input(
        "Function (z = f(x,y))",
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

            fig = go.Figure(
                data=[go.Surface(z=Z, x=X, y=Y)]
            )

            fig.update_layout(
                margin=dict(l=0, r=0, t=40, b=0)
            )

            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:

            st.error(f"Formula Error: {e}")
