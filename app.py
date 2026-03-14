import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import pandas as pd
from astropy import constants as const
from astropy import units as u
from rapidfuzz import process, fuzz
from fpdf import FPDF

# --- 1. SYSTEM CONFIG & UI ---
st.set_page_config(page_title="Verilogic Pro SRE", layout="centered")

if 'history' not in st.session_state: st.session_state.history = []
if 'registry' not in st.session_state: st.session_state.registry = {}
if 'unit_pref' not in st.session_state: st.session_state.unit_pref = "Metric"

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

# --- 2. THE ALMIGHTY RESEARCH ENGINE ---
def clean_wiki(text):
    """Removes raw LaTeX and math formatting from Wiki results"""
    text = re.sub(r'\{[^{}]*\}', '', text)
    text = re.sub(r'\\displaystyle', '', text)
    text = re.sub(r'\\[a-z]+', '', text)
    return text.strip()

def smart_engine(query):
    q_raw = query.lower().strip()
    
    # PASS 1: SCIENCE CONSTANTS
    science_map = {
        "size of the sun": {"val": const.R_sun, "u_m": u.km, "u_i": u.imperial.mile},
        "mass of the sun": {"val": const.M_sun, "u_m": u.kg, "u_i": u.lb},
        "speed of light": {"val": const.c, "u_m": u.km/u.s, "u_i": u.imperial.mile/u.s}
    }
    best_match, score, _ = process.extractOne(q_raw, science_map.keys(), scorer=fuzz.WRatio)
    if score > 85:
        data = science_map[best_match]
        unit = data['u_m'] if st.session_state.unit_pref == "Metric" else data['u_i']
        converted = data['val'].to(unit)
        st.session_state.registry[best_match.replace(" ", "_")] = f"{converted.value:,.2f} {unit}"
        try: wiki_info = clean_wiki(wikipedia.summary(best_match, sentences=2, auto_suggest=True))
        except: wiki_info = "Data verified via NASA/Astropy standard constants."
        return {"q": query, "a": f"{converted.value:,.0f} {unit}", "i": wiki_info, "t": "ASTRO CORE", "lx": sp.latex(converted)}

    # PASS 2: SMART MATH (2x+9x Fix)
    if any(c.isdigit() or c in "xyz+-*/^()=" for c in q_raw):
        try:
            math_ready = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', q_raw)
            x, y, z = sp.symbols('x y z')
            if "=" in math_ready:
                lhs, rhs = math_ready.split("=")
                eq = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
                sol = sp.solve(eq)
                return {"q": query, "a": f"x = {sol}", "i": "Equation solved via symbolic isolation.", "t": "ALGEBRA", "lx": sp.latex(eq)}
            else:
                res = sp.simplify(math_ready)
                return {"q": query, "a": str(res), "i": "Symbolic reduction complete.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # PASS 3: LIBRARIAN
    try:
        wiki = clean_wiki(wikipedia.summary(query, sentences=3, auto_suggest=True))
        return {"q": query, "a": "Knowledge Retrieved", "i": wiki, "t": "LIBRARIAN", "lx": None}
    except:
        return {"q": query, "a": "Refining...", "i": "Try '2x+9x' or 'Size of the Sun'.", "t": "SYSTEM", "lx": None}

# --- 3. SETTINGS & SIDEBAR ---
with st.sidebar:
    st.title("SRE Settings")
    st.session_state.unit_pref = st.radio("System Units", ["Metric", "Imperial"])
    
    st.write("---")
    st.subheader("📊 Variable Registry")
    if st.session_state.registry:
        for k, v in st.session_state.registry.items():
            st.code(f"{k}: {v}")
    else: st.caption("No constants captured.")
    
    st.write("---")
    if st.button("🗑️ Reset Workspace"):
        st.session_state.history = []
        st.session_state.registry = {}
        st.rerun()

# --- 4. VIEWPORT ---
st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ADVANCED RESEARCH ENVIRONMENT v15.0</div>', unsafe_allow_html=True)

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
        <div style="font-size:0.9rem; color:#3A3A3C; line-height:1.5;">💡 <b>Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item.get('lx'): st.latex(item['lx'])
