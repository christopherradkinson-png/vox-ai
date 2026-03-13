import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from pint import UnitRegistry
import time

# --- 1. SRE ULTIMATE SYSTEM UI ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro', layout='centered', initial_sidebar_state="collapsed")

# HARD-CODED CSS OVERRIDE (TESTED ON IOS SAFARI)
st.markdown("""
<style>
    /* 1. Global Reset */
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: hidden !important; height: 0px !important; } 
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stDeployButton { display:none !important; }

    /* 2. Glassmorphism Worksheet Cards */
    .sre-card {
        background: #F2F2F7;
        border-radius: 24px;
        padding: 24px;
        margin: 15px 0px;
        border: 1px solid #E5E5EA;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .meta { color: #8E8E93; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .ans { color: #000000; font-size: 2.2rem; font-weight: 700; margin: 5px 0; letter-spacing: -1.5px; }
    .work { color: #007AFF; font-size: 0.85rem; font-family: 'SF Mono', monospace; opacity: 0.8; }

    /* 3. THE FLOATING DOCK (MOBILE-LOCK SYSTEM) */
    div[data-testid="stForm"] {
        position: fixed !important;
        bottom: 40px !important;
        left: 5% !important;
        right: 5% !important;
        background: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-radius: 100px !important;
        border: 1px solid #D1D1D6 !important;
        padding: 5px 15px !important;
        z-index: 999999 !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.1) !important;
    }
    
    /* Force horizontal layout for mobile dock */
    div[data-testid="stForm"] > div {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 10px !important;
    }

    /* Clean Input Styling */
    .stTextInput input {
        border: none !important;
        background: transparent !important;
        font-size: 1.2rem !important;
        color: #000 !important;
    }
    
    /* BLUE EXE BUTTON */
    button[kind="formSubmit"] {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 10px 25px !important;
        border: none !important;
        font-weight: 700 !important;
    }

    /* Padding for the worksheet feed */
    .main .block-container { padding-bottom: 220px !important; padding-top: 20px !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE ADVANCED COGNITION ENGINE ---
if 'history' not in st.session_state: st.session_state.history = []

SCIENCE_DB = {
    "sun mass": "1.989 × 10³⁰ kg",
    "thermal mass of the sun": "Approx 5 × 10³³ J/K",
    "speed of light": "299,792,458 m/s",
    "gravity": "9.80665 m/s²"
}

def analyze_engine(raw):
    q = raw.lower().strip()
    if not q: return None
    start = time.time()
    try:
        # 1. Science Core Lookup
        for key in SCIENCE_DB:
            if key in q:
                return {"q": raw, "a": SCIENCE_DB[key], "w": "Science Logic Core", "t": "SCI", "ms": round((time.time()-start)*1000, 1)}

        # 2. Advanced Units (e.g., 100mph to kph)
        if " to " in q:
            res = ureg(q)
            return {"q": raw, "a": f"{res.magnitude:g} {res.units}", "w": "Unit Conversion Engine", "t": "UNIT", "ms": round((time.time()-start)*1000, 1)}

        # 3. Plotting Logic
        if 'x' in q and '=' not in q:
            return {"q": raw, "a": "Plot Rendered", "w": "Plotly Visuals", "t": "PLOT", "ms": round((time.time()-start)*1000, 1)}

        # 4. Symbolic Math (Implicit Mult 2x -> 2*x)
        clean = q.replace('^', '**')
        # Hardened implicit multiplication
        import re
        clean = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', clean)
        
        expr = sp.sympify(clean)
        ans = expr.evalf(8)
        return {"q": raw, "a": f"{ans:g}", "w": f"Exact: {sp.latex(expr)}", "t": "MATH", "ms": round((time.time()-start)*1000, 1)}

    except:
        return {"q": raw, "a": "Check Entry", "w": "Syntax Check Required", "t": "ERR", "ms": 0}

# --- 3. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900; letter-spacing:-2px; margin-top:-40px;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

# THE FEED
for item in st.session_state.history:
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | {item['ms']}ms</div>
        <div class="ans">= {item['a']}</div>
        <div class="work">{item['w']}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    if item['t'] == "PLOT":
        x_vals = np.linspace(-10, 10, 400)
        f_sym = sp.sympify(item['q'].replace('^', '**'))
        f_num = sp.lambdify(sp.Symbol('x'), f_sym, "numpy")
        fig = go.Figure(data=go.Scatter(x=x_vals, y=f_num(x_vals), line=dict(color='#007AFF', width=5)))
        fig.update_layout(height=280, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.03)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 4. THE FLOATING INPUT DOCK ---
# 'clear_on_submit' is the key to preventing the infinite loop bug
with st.form("pro_dock_final", clear_on_submit=True):
    col1, col2 = st.columns([0.75, 0.25])
    with col1:
        user_in = st.text_input("SRE Input", placeholder="5x + 10...", label_visibility="collapsed")
    with col2:
        exe_btn = st.form_submit_button("EXE")

if exe_btn and user_in:
    result_pkg = analyze_engine(user_in)
    if result_pkg:
        st.session_state.history.append(result_pkg)
        st.rerun()

# Sidebar Utility
with st.sidebar:
    if st.button("🗑️ Reset Worksheet"):
        st.session_state.history = []
        st.rerun()
