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

# --- 1. SYSTEM ARCHITECTURE & UI ---
st.set_page_config(page_title="Verilogic Pro SRE", layout="centered")

if 'history' not in st.session_state: st.session_state.history = []

# Mobile-Optimized Professional UI
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    .v-header { text-align: center; color: #1C1C1E; font-weight: 900; font-size: 2.2rem; margin-top: -50px; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 700; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 30px; }
    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 15px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 25px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 24px; 
        margin: 15px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #1C1C1E; font-size: 2.1rem; font-weight: 800; margin: 5px 0; letter-spacing: -1px; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE ALMIGHTY ANALYTICAL ENGINE ---
def smart_engine(query):
    q_raw = query.lower().strip()
    
    # PASS 1: GRAPHING (e.g. "plot x^2")
    if "plot" in q_raw:
        try:
            func_str = q_raw.replace("plot", "").strip()
            x_vals = np.linspace(-10, 10, 100)
            y_vals = [float(sp.sympify(func_str).subs('x', val)) for val in x_vals]
            fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#007AFF')))
            fig.update_layout(title=f"f(x) = {func_str}", template="plotly_white", height=350)
            return {"q": query, "a": "Graph Generated", "i": f"Visualization of {func_str} complete.", "t": "GRAPHING", "fig": fig}
        except: pass

    # PASS 2: SCIENCE & CONSTANTS (with Units + Wiki Blurb)
    science_map = {
        "size of the sun": {"val": const.R_sun.to(u.km), "u": "km"},
        "mass of the sun": {"val": const.M_sun, "u": "kg"},
        "speed of light": {"val": const.c.to(u.km/u.s), "u": "km/s"},
        "distance to moon": {"val": 384400, "u": "km"}
    }
    best_match, score, _ = process.extractOne(q_raw, science_map.keys(), scorer=fuzz.WRatio)
    if score > 85:
        data = science_map[best_match]
        val = data['val'].value if hasattr(data['val'], 'value') else data['val']
        try: wiki_info = wikipedia.summary(best_match, sentences=2, auto_suggest=True)
        except: wiki_info = "Data verified via NASA/Astropy standard constants."
        return {"q": query, "a": f"{val:,.2f} {data['u']}", "i": wiki_info, "t": "ASTRO CORE", "lx": sp.latex(data['val'])}

    # PASS 3: SMART MATH (The "2x+9x" & "x^2=16" Fix)
    if any(c.isdigit() or c in "xyz+-*/^()=" for c in q_raw):
        try:
            # Handle implicit multiplication (2x -> 2*x)
            math_ready = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', q_raw)
            x, y, z = sp.symbols('x y z')
            if "=" in math_ready:
                lhs, rhs = math_ready.split("=")
                eq = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
                sol = sp.solve(eq)
                return {"q": query, "a": f"x = {sol}", "i": "Equation solved via symbolic isolation.", "t": "ALGEBRA", "lx": sp.latex(eq)}
            else:
                res = sp.simplify(math_ready)
                return {"q": query, "a": str(res), "i": "Symbolic reduction successful.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # PASS 4: GENERAL KNOWLEDGE (Librarian)
    try:
        wiki = wikipedia.summary(query, sentences=3, auto_suggest=True)
        return {"q": query, "a": "Knowledge Retrieved", "i": wiki, "t": "LIBRARIAN", "lx": None}
    except:
        return {"q": query, "a": "Check Input", "i": "Input unrecognized. Try '2x+9x' or 'Size of the Sun'.", "t": "SYSTEM", "lx": None}

# --- 3. THE VIEWPORT ---
st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ANTICIPATORY RESEARCH ENGINE v13.6</div>', unsafe_allow_html=True)

with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Math, Science, or Facts...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    st.session_state.history.insert(0, smart_engine(u_in))

for item in st.session_state.history:
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:0.9rem; color:#3A3A3C; line-height:1.4;">💡 <b>Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item.get('fig'): st.plotly_chart(item['fig'], use_container_width=True)
    if item.get('lx'): st.latex(item['lx'])

with st.sidebar:
    st.title("SRE Tools")
    if st.button("🗑️ Reset Workspace"):
        st.session_state.history = []
        st.rerun()
