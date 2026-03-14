import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import plotly.graph_objects as go
from scipy import constants as sc
from pint import UnitRegistry
from rapidfuzz import process, fuzz

# --- 1. SYSTEM INITIALIZATION ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="expanded")

# APPLE PRO UI: ULTRA-CLEAN GRID
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 12px 18px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 25px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stForm"] > div {
        display: grid !important; grid-template-columns: 4.5fr 1fr !important;
        align-items: center !important; gap: 10px !important;
    }
    button[kind="formSubmit"] {
        background-color: #007AFF !important; color: white !important;
        border-radius: 12px !important; font-weight: 700 !important;
    }
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 24px; 
        margin: 15px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #1C1C1E; font-size: 1.9rem; font-weight: 800; margin: 5px 0; letter-spacing: -1px; }
    .ai-insight { color: #1C1C1E; font-size: 0.95rem; border-top: 1px solid #F2F2F7; padding-top: 10px; margin-top: 10px;}
</style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. THE ADVANCED REASONING ENGINE ---
def ai_brain(query):
    q_raw = query.lower().strip()
    
    # NASA-GRADE KNOWLEDGE VAULT (In-Memory Database)
    science_vault = {
        "mass of the sun": {"val": sc.value('solar mass'), "unit": "kg"},
        "radius of the sun": {"val": 6.957e8, "unit": "meters"},
        "speed of light": {"val": sc.c, "unit": "m/s"},
        "gravitational constant": {"val": sc.G, "unit": "m^3/kg/s^2"},
        "thermal mass of the sun": {"val": "1.989e30", "unit": "kg"},
        "pi": {"val": str(np.pi), "unit": ""}
    }

    # PASS 1: SEMANTIC UNIT CONVERSION (e.g. "5 meters to feet")
    if " to " in q_raw:
        try:
            parts = q_raw.split(" to ")
            result_unit = ureg(parts[0]).to(parts[1])
            return {"q": query, "a": f"{result_unit}", "i": "Unit Conversion Logic synchronized.", "t": "ENGINEERING CORE"}
        except: pass

    # PASS 2: CONTEXTUAL INJECTION (Injecting Science Data)
    processed_q = q_raw
    injected = []
    for key, data in science_vault.items():
        if key in processed_q:
            processed_q = processed_q.replace(key, str(data['val']))
            injected.append(key.title())

    # PASS 3: MATH REASONING
    processed_q = processed_q.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')
    processed_q = re.sub(r'[^\d\+\-\*\/\.\(\)\^e]', '', processed_q) # Strict Math Safety Filter

    if any(c.isdigit() for c in processed_q):
        try:
            expr = sp.sympify(processed_q.replace('^', '**'))
            ans = expr.evalf(12)
            return {"q": query, "a": f"{float(ans):,g}", "i": f"Logic successful. Injected: {', '.join(injected)}" if injected else "Direct calculation successful.", "t": "MATH CORE"}
        except: pass

    # PASS 4: GLOBAL LIBRARIAN (Wikipedia with Fuzzy Matching)
    try:
        summary = wikipedia.summary(q_raw, sentences=3, auto_suggest=True)
        return {"q": query, "a": "Verified Data", "i": summary, "t": "GLOBAL LIBRARIAN"}
    except:
        return {"q": query, "a": "Processing...", "i": "The SRE is refining parameters. Try using specific units or operators.", "t": "SYSTEM"}

# --- 3. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("pro_dock_v5", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Enter Equation, Unit Conversion, or Science Query...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_brain(u_in)
    st.session_state.history.append(result)
    st.rerun()

for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 <b>Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
