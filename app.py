import streamlit as st
import sympy as sp
import plotly.graph_objects as go
import numpy as np
from pint import UnitRegistry

# --- 1. APPLE X DESMOS GRID-LOCK UI ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic SRE', layout='centered', initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: hidden; height: 0px; }
    
    /* THE FIX: Force 5 columns to stay horizontal on iPhone */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* Locks layout */
        gap: 6px !important;
        margin-bottom: 8px !important;
    }
    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* APPLE SQUIRCLE BUTTONS */
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1.1 / 1 !important;
        border-radius: 12px !important;
        border: 1px solid #E5E5EA !important;
        background-color: #FDFDFD !important;
        color: #000000 !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        box-shadow: 0px 1px 2px rgba(0,0,0,0.05);
    }
    .stButton > button:active { transform: scale(0.95); background-color: #E5E5EA !important; }
    button:has(div:contains("EXE")) { background-color: #007AFF !important; color: white !important; border: none !important; }

    /* DESMOS WORKSHEET FEED */
    .worksheet-row {
        background: #FFFFFF; padding: 18px; border-bottom: 1px solid #F2F2F7;
    }
    
    /* iOS INPUT BAR */
    .stTextInput input {
        border: none !important; border-top: 1px solid #F2F2F7 !important;
        color: #000000 !important; font-size: 2.2rem !important;
        text-align: right !important; background-color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE SRE ENGINE ---
if 'history' not in st.session_state: st.session_state.history = []
if 'cmd' not in st.session_state: st.session_state.cmd = ""

def calculate():
    raw = st.session_state.cmd
    try:
        # Unit Logic
        if any(u in raw for u in ['ft', 'm', 'kg', 'lb', 'in']):
            res = ureg(raw)
            st.session_state.history.append({"type": "math", "q": raw, "a": f"{res.magnitude:.4f} {res.units}"})
        # Graphing Logic
        elif 'x' in raw and '=' not in raw:
            st.session_state.history.append({"type": "graph", "q": raw})
        # Standard Math
        else:
            expr = sp.sympify(raw.replace('^', '**').replace('x', '*x'))
            st.session_state.history.append({"type": "math", "q": raw, "a": expr.evalf(5), "step": f"Parsed: {sp.latex(expr)}"})
        st.session_state.cmd = ""
    except: st.toast("Check Syntax", icon="⚠️")

# --- 3. THE VIEWPORT ---
st.markdown("<h4 style='text-align:center; font-weight:600; margin-top:-40px;'>Verilogic SRE</h4>", unsafe_allow_html=True)

for entry in st.session_state.history[-3:]:
    with st.container():
        if entry['type'] == "math":
            st.markdown(f'<div class="worksheet-row"><small style="color:#8E8E93;">{entry["q"]}</small><br><b>= {entry["a"]}</b></div>', unsafe_allow_html=True)
        elif entry['type'] == "graph":
            x = np.linspace(-10, 10, 400)
            f = sp.lambdify(sp.Symbol('x'), sp.sympify(entry['q'].replace('^', '**')), "numpy")
            fig = go.Figure(data=go.Scatter(x=x, y=f(x), line=dict(color='#007AFF', width=3)))
            fig.update_layout(height=240, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='white', plot_bgcolor='#F9F9FB')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.text_input('', value=st.session_state.cmd, placeholder="0", key="main_in", label_visibility="collapsed")

# --- 4. KEYBOARD (GRID LOCKED) ---
keys = [['sin', 'cos', 'tan', 'x', '/'], ['7', '8', '9', '(', '*'], ['4', '5', '6', ')', '-'], ['1', '2', '3', '^', '+'], ['AC', '0', '.', 'DEL', 'EXE']]
for row in keys:
    cols = st.columns(5)
    for i, key in enumerate(row):
        if cols[i].button(key, key=f"btn_{key}_{keys.index(row)}"):
            if key == "AC": st.session_state.cmd = ""
            elif key == "DEL": st.session_state.cmd = st.session_state.cmd[:-1]
            elif key == "EXE": calculate()
            else: st.session_state.cmd += str(key)
            st.rerun()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    st.caption("TASAA Compliance 2026")
    if st.button("Clear Worksheet"): st.session_state.history = []; st.rerun()
