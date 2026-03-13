import streamlit as st
import sympy as sp
import plotly.graph_objects as go
import numpy as np
from pint import UnitRegistry

# --- 1. THE MILLION-DOLLAR APPLE UI ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="collapsed")

# PERSISTENT CSS FOR GLASSMORPHISM & FLOATING DOCK
st.markdown("""
<style>
    /* Apple Core Aesthetic */
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: hidden; } 
    
    /* GLASS FEED CARDS */
    .sre-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 30px;
        padding: 28px;
        margin-bottom: 20px;
        border: 1px solid #F2F2F7;
        box-shadow: 0 12px 40px rgba(0,0,0,0.04);
    }

    .q-label { color: #8E8E93; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.2px; }
    .a-label { color: #000000; font-size: 2.6rem; font-weight: 800; margin: 10px 0; letter-spacing: -1.5px; }
    .work-label { color: #007AFF; font-size: 0.9rem; font-weight: 400; opacity: 0.8; }

    /* THE FLOATING DOCK (FIXED TO BOTTOM) */
    div[data-testid="stForm"] {
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 92% !important;
        max-width: 550px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(40px) !important;
        -webkit-backdrop-filter: blur(40px) !important;
        border-radius: 100px !important;
        border: 1px solid #D1D1D6 !important;
        padding: 8px 20px !important;
        box-shadow: 0 25px 60px rgba(0,0,0,0.12) !important;
        z-index: 10000 !important;
    }

    /* Input & Button Styling */
    input { border: none !important; background: transparent !important; font-size: 1.3rem !important; }
    button[kind="formSubmit"] {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 12px 35px !important;
        border: none !important;
        font-weight: 700 !important;
    }
    
    /* Spacer so content doesn't hide behind the dock */
    .main .block-container { padding-bottom: 180px; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE ADVANCED SRE INTELLIGENCE ENGINE ---
if 'history' not in st.session_state: st.session_state.history = []

SCIENCE_DB = {
    "sun mass": "1.989 × 10³⁰ kg",
    "sun thermal mass": "Approx 5 × 10³³ J/K",
    "thermal mass of the sun": "Approx 5 × 10³³ J/K",
    "speed of light": "299,792,458 m/s",
    "gravity": "9.80665 m/s²"
}

def analyze_sre(raw_text):
    query = raw_text.lower().strip()
    if not query: return None
    
    try:
        # 1. AI SCIENCE LOOKUP
        for key in SCIENCE_DB:
            if key in query:
                return {"q": raw_text, "a": SCIENCE_DB[key], "w": "AI-Assist Science Data", "t": "sci"}

        # 2. UNIT CONVERSION (e.g., 100m to ft)
        if " to " in query:
            res = ureg(query)
            return {"q": raw_text, "a": f"{res.magnitude:g} {res.units}", "w": "Dimensional Analysis", "t": "unit"}

        # 3. ADVANCED GRAPHING
        if 'x' in query and '=' not in query:
            return {"q": raw_text, "a": "Graphing...", "w": "Plotly Engine", "t": "graph"}

        # 4. HARDENED MATH (With Implicit Mult 2x -> 2*x)
        clean_q = query.replace('^', '**').replace('x', '*x')
        expr = sp.sympify(clean_q)
        ans = expr.evalf(8)
        return {"q": raw_text, "a": f"{ans:g}", "w": f"Exact: {sp.latex(expr)}", "t": "math"}
    
    except:
        return {"q": raw_text, "a": "Check Entry", "w": "Syntax Error", "t": "err"}

# --- 3. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:800; margin-top:-50px;'>Verilogic Pro</h2>", unsafe_allow_html=True)

# Display the History Feed
for entry in st.session_state.history:
    st.markdown(f'<div class="sre-card"><div class="q-label">{entry["q"]}</div><div class="a-label">= {entry["a"]}</div>', unsafe_allow_html=True)
    
    if entry['t'] == "graph":
        x = np.linspace(-10, 10, 400)
        f_sym = sp.sympify(entry['q'].replace('^', '**'))
        f_num = sp.lambdify(sp.Symbol('x'), f_sym, "numpy")
        fig = go.Figure(data=go.Scatter(x=x, y=f_num(x), line=dict(color='#007AFF', width=4)))
        fig.update_layout(height=280, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(240,240,245,0.4)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(f'<div class="work-label">{entry["w"]}</div></div>', unsafe_allow_html=True)

# --- 4. THE FLOATING INPUT DOCK ---
with st.form("sre_input_dock", clear_on_submit=True):
    cols = st.columns([0.8, 0.2])
    with cols[0]:
        user_val = st.text_input("SRE Input", placeholder="Math, Units, or Science...", label_visibility="collapsed")
    with cols[1]:
        submitted = st.form_submit_button("EXE")

if submitted and user_val:
    pkg = analyze_sre(user_val)
    if pkg:
        st.session_state.history.append(pkg)
        st.rerun()

# Sidebar for clearing data
with st.sidebar:
    if st.button("🗑️ Reset Worksheet"):
        st.session_state.history = []
        st.rerun()
