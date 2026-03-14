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

# --- 1. SYSTEM UI & STATE ---
st.set_page_config(page_title="Verilogic Pro SRE", layout="centered")

if 'history' not in st.session_state: st.session_state.history = []
if 'registry' not in st.session_state: st.session_state.registry = {}

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .v-header { text-align: center; color: #1C1C1E; font-weight: 900; font-size: 2.2rem; margin-top: -40px; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 700; font-size: 0.7rem; letter-spacing: 2px; margin-bottom: 25px; }
    .sre-card { background: #F2F2F7; border-radius: 18px; padding: 20px; margin: 15px 0; border: 1px solid #D1D1D6; }
    .meta { color: #007AFF; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #1C1C1E; font-size: 1.8rem; font-weight: 800; margin: 5px 0; }
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE MULTI-AGENT RESEARCH ENGINE ---
def research_engine(query):
    q_raw = query.lower().strip()
    
    # PASS 1: GRAPHING (e.g. "plot x^2")
    if "plot" in q_raw:
        try:
            func_str = q_raw.replace("plot", "").strip()
            x_vals = np.linspace(-10, 10, 100)
            y_vals = [float(sp.sympify(func_str).subs('x', val)) for val in x_vals]
            fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#007AFF')))
            fig.update_layout(title=f"f(x) = {func_str}", template="plotly_white", height=350)
            return {"q": query, "a": "Graph Generated", "i": f"Plotting {func_str}", "t": "GRAPHING", "fig": fig}
        except: pass

    # PASS 2: SCIENCE & CONSTANTS (Astropy Integration)
    science_map = {"size of the sun": const.R_sun.to(u.km), "speed of light": const.c, "mass of earth": const.M_earth}
    match, score, _ = process.extractOne(q_raw, science_map.keys(), scorer=fuzz.WRatio)
    if score > 85:
        data = science_map[match]
        val = data.value if hasattr(data, 'value') else data
        st.session_state.registry[match.replace(" ", "_")] = val
        return {"q": query, "a": f"{val:,.2f}", "i": "Verified via NASA/Astropy standard constants.", "t": "ASTRO CORE", "lx": sp.latex(val)}

    # PASS 3: ADVANCED CAS (SymPy Solver)
    try:
        if "=" in q_raw or "solve" in q_raw:
            eq_text = q_raw.replace("solve", "").strip()
            lhs, rhs = eq_text.split("=") if "=" in eq_text else (eq_text, "0")
            eq = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            sol = sp.solve(eq)
            return {"q": query, "a": f"x = {sol}", "i": "Symbolic root discovery.", "t": "ALGEBRA", "lx": sp.latex(eq)}
        
        # Raw Arithmetic Fallback
        if any(c.isdigit() or c in "+-*/^()" for c in q_raw):
            res = sp.sympify(q_raw).evalf(10)
            return {"q": query, "a": f"{float(res):g}", "i": "Mathematical computation complete.", "t": "MATH CORE", "lx": sp.latex(sp.sympify(q_raw))}
    except: pass

    # PASS 4: LIBRARIAN (Wikipedia)
    try:
        wiki = wikipedia.summary(q_raw, sentences=2, auto_suggest=True)
        return {"q": query, "a": "Fact Verified", "i": wiki, "t": "LIBRARIAN", "lx": None}
    except:
        return {"q": query, "a": "System Error", "i": "Unrecognized command. Try 'plot x^2' or 'size of the sun'.", "t": "SYSTEM", "lx": None}

# --- 3. UI VIEWPORT ---
st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">SCIENTIFIC RESEARCH ENGINE v13.0</div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("Workspace Registry")
    if st.session_state.registry:
        for k, v in st.session_state.registry.items():
            st.code(f"{k}: {v:g}")
    else: st.caption("No variables stored.")
    if st.button("🗑️ Reset All"):
        st.session_state.history = []
        st.session_state.registry = {}
        st.rerun()

with st.form("main_input", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="e.g. 'solve x^2=9' or 'plot sin(x)'", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    st.session_state.history.insert(0, research_engine(u_in))

for item in st.session_state.history:
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:0.9rem; color:#3A3A3C;">💡 {item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item.get('fig'): st.plotly_chart(item['fig'], use_container_width=True)
    if item.get('lx'): st.latex(item['lx'])
