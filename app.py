import streamlit as st
import sympy as sp
import plotly.graph_objects as go
import numpy as np
from pint import UnitRegistry

# --- 1. THE "VERILOGIC" PRO UI (MOBILE-OPTIMIZED) ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro', layout='centered', initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* APPLE SYSTEM UI */
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: hidden; }
    
    /* GLASS FEED CARDS */
    .sre-card {
        background: #F9F9F9;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 16px;
        border: 1px solid #E5E5EA;
    }
    .q-text { color: #8E8E93; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; }
    .a-text { color: #000000; font-size: 2.2rem; font-weight: 700; margin-top: 8px; letter-spacing: -1px; }

    /* FLOATING INPUT DOCK FIX (FOR IPHONE) */
    div[data-testid="stForm"] {
        position: fixed !important;
        bottom: 20px !important;
        left: 5% !important;
        right: 5% !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-radius: 50px !important;
        border: 1px solid #D1D1D6 !important;
        padding: 10px 20px !important;
        z-index: 10000 !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1) !important;
    }
    
    /* Clean up the form display */
    div[data-testid="stForm"] > div:first-child { border: none !important; }
    
    /* EXE BUTTON - PRO BLUE */
    button[kind="formSubmit"] {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 40px !important;
        padding: 10px 25px !important;
        border: none !important;
        font-weight: 600 !important;
        float: right;
    }

    /* Padding for the feed so it doesn't get cut off by the dock */
    .main .block-container { padding-bottom: 120px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SRE INTELLIGENCE ENGINE ---
if 'history' not in st.session_state: st.session_state.history = []

SCIENCE_DB = {
    "sun mass": "1.989e30 kg",
    "thermal mass of the sun": "Approx 5e33 J/K",
    "speed of light": "299,792,458 m/s"
}

def analyze_sre(raw):
    q = raw.lower().strip()
    if not q: return None
    try:
        # Science Lookup
        for key in SCIENCE_DB:
            if key in q: return {"q": raw, "a": SCIENCE_DB[key], "t": "sci"}
        # Units
        if " to " in q:
            res = ureg(q)
            return {"q": raw, "a": f"{res.magnitude:g} {res.units}", "t": "unit"}
        # Math
        clean = q.replace('^', '**').replace('x', '*x')
        expr = sp.sympify(clean)
        return {"q": raw, "a": f"{expr.evalf(6):g}", "t": "math"}
    except: return {"q": raw, "a": "Check Syntax", "t": "err"}

# --- 3. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:800; margin-top:-40px;'>Verilogic Pro</h2>", unsafe_allow_html=True)

for entry in st.session_state.history:
    st.markdown(f'<div class="sre-card"><div class="q-text">{entry["q"]}</div><div class="a-text">= {entry["a"]}</div></div>', unsafe_allow_html=True)

# --- 4. THE INPUT DOCK ---
with st.form("dock", clear_on_submit=True):
    # This layout forces the input and button to sit side-by-side on mobile
    c1, c2 = st.columns([0.7, 0.3])
    with c1:
        user_val = st.text_input("Input", placeholder="Enter query...", label_visibility="collapsed")
    with c2:
        exe = st.form_submit_button("EXE")

if exe and user_val:
    result = analyze_sre(user_val)
    if result:
        st.session_state.history.append(result)
        st.rerun()

# Sidebar for reset
with st.sidebar:
    if st.button("Reset App"):
        st.session_state.history = []
        st.rerun()
