import streamlit as st
import sympy as sp
import re

# 1. Identity & PWA Setup
st.set_page_config(page_title="Verilogic-125 SRE", page_icon="⚡", layout="centered")

# 2. Visual Layer (Fixed Spacing & Colors)
st.markdown("""
<style>
    .stApp {background-color: #0e1117; color: #ffffff;}
    .main-title {text-align: center; color: #4b90ff; font-family: monospace; font-weight: bold; font-size: 1.8rem; margin-top: 20px;}
    .sub-title {text-align: center; color: #00ffcc; font-family: monospace; font-size: 0.8rem; margin-bottom: 30px;}
    .stTextInput>div>div>input {background-color: #1a1c23; color: #00ffcc; border: 2px solid #4b90ff; text-align: center; border-radius: 10px;}
    .stSuccess {background-color: #0e1117; border: 1px solid #4b90ff; color: #4b90ff; text-align: center; border-radius: 10px;}
    .stInfo {background-color: #1a1c23; border-left: 5px solid #00ffcc; color: #ffffff; border-radius: 5px;}
    footer {visibility: hidden;}
</style>
<div class="main-title">VERILOGIC-125 CORE SRE</div>
<div class="sub-title">Scientific Reasoning Engine with MAX AI ASSIST</div>
""", unsafe_allow_html=True)

class VERILOGIC_CORE:
    def __init__(self):
        self.status = "SRE CORE: ONLINE"

    def ai_assist(self, q):
        q = q.lower().strip()
        data = {
            "p=np": "P vs NP: If every easily checked problem is easily solved. Currently Unsolved.",
            "p vs np": "P vs NP: Millennium Logic Gate. If P=NP, cryptography collapses.",
            "schrodinger": "Schrodinger's Equation: Foundation of Quantum Mechanics.",
            "relativity": "General Relativity: Einstein's theory of gravity and spacetime.",
            "thermodynamics": "Second Law: Entropy always increases toward heat death.",
            "quantum": "Quantum Entanglement: Instant link between distant particles."
        }
        for key in data:
            if key in q: return data[key]
        return None

    def math_engine(self, q):
        try:
            if '=' in q:
                l, r = q.split('=')
                return str(sp.solve(sp.Eq(sp.sympify(l.strip()), sp.sympify(r.strip()))))
            return str(sp.simplify(sp.sympify(q)))
        except:
            return None

if 'ai' not in st.session_state:
    st.session_state.ai = VERILOGIC_CORE()

with st.sidebar:
    st.title("⚙️ SYSTEM")
    st.write(f"**Core:** {st.session_state.ai.status}")
    st.write("**Mode:** MAX AI ASSIST")

query = st.text_input("ENTER QUERY (MATH OR THEORY):", placeholder="e.g. P vs NP or 4*x = 20")

if query:
    logic = st.session_state.ai.ai_assist(query)
    math = st.session_state.ai.math_engine(query)
    if logic:
        st.info("🧬 AI ASSIST: " + str(logic))
    if math:
        st.success("🔢 MATH RESULT: " + str(math))
    if not logic and not math:
        st.error("⚠️ UNVERIFIABLE: Use * for multiply (e.g. 4*x).")
