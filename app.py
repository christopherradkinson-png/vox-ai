import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import pandas as pd
import plotly.graph_objects as go
from astropy import constants as const
from astropy import units as u
from rapidfuzz import process, fuzz
from PIL import Image
from fpdf import FPDF
import base64

# --- 1. SYSTEM INITIALIZATION ---
st.set_page_config(page_title="Verilogic Pro SRE", layout="wide")

if 'history' not in st.session_state: st.session_state.history = []
if 'registry' not in st.session_state: st.session_state.registry = {}

# Professional UI Styling
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    .sre-card {
        background: #F2F2F7; border-radius: 15px; padding: 20px; 
        margin: 10px 0; border: 1px solid #D1D1D6;
    }
    .meta { color: #007AFF; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
    .ans { color: #1C1C1E; font-size: 1.8rem; font-weight: 800; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# --- 2. LOGIC MODULES ---

def nl_translator(text):
    t = text.lower().strip()
    if "derivative" in t or "diff" in t:
        expr = re.search(r"(?:of|is)\s+([a-z0-9\^ \*\+\-\/]+)", t)
        if expr: return f"diff {expr.group(1).strip()}"
    if "solve" in t or "find x" in t:
        eq = re.search(r"(?:for|is)\s+([a-z0-9\^ \*\+\-\/\=\s]+)", t)
        if eq: return f"steps {eq.group(1).strip()}"
    return t

def solve_steps(expr_str):
    steps = []
    try:
        if "=" in expr_str:
            lhs, rhs = expr_str.split("=")
            eq = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
        else:
            eq = sp.Eq(sp.sympify(expr_str), 0)
        steps.append({"m": "Initial Equation", "lx": sp.latex(eq)})
        simplified = sp.simplify(eq.lhs - eq.rhs)
        steps.append({"m": "Isolate Terms", "lx": f"{sp.latex(simplified)} = 0"})
        sol = sp.solve(simplified)
        steps.append({"m": "Final Solution", "lx": f"x = {sp.latex(sol)}"})
        return steps
    except: return [{"m": "Error", "lx": "Verify syntax"}]

def ai_brain(query):
    q = nl_translator(query)
    # Calculus
    if any(x in q for x in ["diff", "int", "derivative", "integral"]):
        try:
            x_sym = sp.symbols('x')
            expr = sp.sympify(q.replace("diff", "").replace("derivative", "").strip())
            res = sp.diff(expr, x_sym)
            return {"q": query, "a": "Derivative Result", "i": "Calculus engine processed.", "t": "CALC", "lx": sp.latex(res)}
        except: pass
    # Steps
    if "steps" in q:
        return {"q": query, "a": "Step-by-Step", "i": "Logic breakdown.", "t": "STEPS", "steps": solve_steps(q.replace("steps", ""))}
    # Knowledge
    try:
        sum_wiki = wikipedia.summary(q, sentences=2)
        return {"q": query, "a": "Fact Retrieval", "i": sum_wiki, "t": "WIKI", "lx": None}
    except:
        return {"q": query, "a": "Output", "i": "Process finished.", "t": "CORE", "lx": None}

# --- 3. VIEWPORT ---

with st.sidebar:
    st.title("Verilogic Pro v12")
    st.caption("SRE Stable Build")
    mode = st.radio("Operating Mode", ["Calculator", "Simulation Lab"])

if mode == "Calculator":
    st.header("Workspace")
    with st.form("input_form", clear_on_submit=True):
        u_in = st.text_input("Enter command or sentence:")
        exec_btn = st.form_submit_button("EXE")
    if exec_btn and u_in:
        st.session_state.history.insert(0, ai_brain(u_in))
    for item in st.session_state.history:
        with st.container():
            st.markdown(f'<div class="sre-card"><div class="meta">{item["t"]}</div><div class="ans">{item["a"]}</div><p>{item["i"]}</p></div>', unsafe_allow_html=True)
            if "steps" in item:
                for s in item["steps"]:
                    st.caption(s["m"])
                    st.latex(s["lx"])
            elif item.get("lx"):
                st.latex(item["lx"])
else:
    st.header("Simulation Lab")
    v0 = st.slider("Velocity (m/s)", 1, 100, 30)
    ang = st.slider("Angle", 0, 90, 45)
    t_f = (2 * v0 * np.sin(np.radians(ang))) / 9.81
    t = np.linspace(0, t_f, 100)
    x = v0 * np.cos(np.radians(ang)) * t
    y = v0 * np.sin(np.radians(ang)) * t - 0.5 * 9.81 * t**2
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', line=dict(color='#007AFF', width=3)))
    st.plotly_chart(fig, use_container_width=True)
    st.download_button("Export CSV", pd.DataFrame({"X": x, "Y": y}).to_csv(), "results.csv")
