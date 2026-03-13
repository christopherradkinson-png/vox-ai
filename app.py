import streamlit as st
import sympy as sp
from pint import UnitRegistry

# --- 1. APPLE NATIVE HYBRID UI ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic SRE', layout='centered', initial_sidebar_state="collapsed")

# iOS Design: Pure White, System Blue, High Contrast
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    header { visibility: hidden; height: 0px; }
    
    /* TOOLBAR GRID: 4 Columns wide (Safe for iPhone) */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
    }
    div[data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }

    /* APPLE SQUIRCLE BUTTONS */
    .stButton > button {
        width: 100% !important;
        padding: 12px 0px !important;
        border-radius: 12px !important;
        background-color: #F2F2F7 !important;
        color: #007AFF !important;
        border: 1px solid #D1D1D6 !important;
        font-weight: 600 !important;
    }
    
    /* BLUE EXE ACTION */
    button:has(div:contains("EXE")) { 
        background-color: #007AFF !important; 
        color: white !important; 
        border: none !important;
    }

    /* iOS NATIVE INPUT BAR */
    .stTextInput input {
        border: 2px solid #E5E5EA !important;
        border-radius: 14px !important;
        font-size: 1.8rem !important;
        padding: 15px !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. ENGINE ---
if 'history' not in st.session_state: st.session_state.history = []
if 'cmd' not in st.session_state: st.session_state.cmd = ""

def run_calculation():
    raw = st.session_state.cmd
    try:
        if any(u in raw for u in ['ft', 'm', 'kg', 'lb']):
            res = ureg(raw)
            st.session_state.history.append({"q": raw, "a": f"{res.magnitude:.4f} {res.units}"})
        else:
            expr = sp.sympify(raw.replace('^', '**').replace('x', '*x'))
            st.session_state.history.append({"q": raw, "a": expr.evalf(5)})
        st.session_state.cmd = ""
    except: st.toast("Syntax Error", icon="⚠️")

# --- 3. THE VIEWPORT ---
st.markdown("<h3 style='text-align:center; font-weight:700;'>Verilogic SRE</h3>", unsafe_allow_html=True)

# Desmos-style Worksheet
for entry in st.session_state.history[-3:]:
    st.markdown(f'''<div style="padding:15px; border-bottom:1px solid #F2F2F7;">
        <small style="color:#8E8E93;">{entry['q']}</small><br>
        <b style="font-size:1.4rem;">= {entry['a']}</b>
    </div>''', unsafe_allow_html=True)

# --- 4. HYBRID DATA ENTRY ---
# Tapping this triggers the native iPhone keyboard
entry = st.text_input("Tap to enter math/units", value=st.session_state.cmd, key="main_in")
st.session_state.cmd = entry

st.caption("Tip: Use the toolbar below for symbols or tap EXE to solve.")

# --- 5. SCIENTIFIC TOOLBAR (Fixed 4-Column Layout) ---
toolbar = [
    ['sin', 'cos', 'tan', 'sqrt'],
    ['(', ')', '^', '/'],
    ['ft', 'm', 'kg', 'lb'],
    ['AC', 'DEL', 'pi', 'EXE']
]

for row in toolbar:
    cols = st.columns(4) # 4 columns is much more stable than 5 on small iPhones
    for i, key in enumerate(row):
        if cols[i].button(key, key=f"tool_{key}_{toolbar.index(row)}"):
            if key == "AC": st.session_state.cmd = ""
            elif key == "DEL": st.session_state.cmd = st.session_state.cmd[:-1]
            elif key == "EXE": run_calculation()
            else: st.session_state.cmd += str(key)
            st.rerun()

with st.sidebar:
    st.title("Settings")
    st.caption("TASAA 2026 Compliant")
    if st.button("Clear Worksheet"):
        st.session_state.history = []
        st.rerun()
