import streamlit as st
import sympy as sp
import datetime, requests
import matplotlib.pyplot as plt
import numpy as np

# --- 1. APPLE COMPACT GRID SYSTEM ---
st.set_page_config(page_title='Verilogic-125 SRE', layout='centered')

st.markdown("""
<style>
    .stApp {background-color: #FFFFFF; color: #000000;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    #MainMenu {visibility: visible;}

    /* Force San Francisco Font */
    * {font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;}

    /* Branding */
    .brand-h1 {text-align: center; font-weight: 800; font-size: 1.8rem; margin-bottom: 0px; color: #000;}
    .brand-sub {text-align: center; font-weight: 700; font-size: 0.7rem; letter-spacing: 2px; color: #8E8E93; margin-top: 0px; margin-bottom: 20px;}

    /* Force Horizontal Grid on All Devices */
    [data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        gap: 8px !important;
        max-width: 400px !important;
        margin: auto !important;
    }

    /* Compact Display Bar */
    .stTextInput input {
        border: none !important; border-bottom: 2px solid #000 !important;
        font-size: 2.2rem !important; text-align: right !important; font-weight: 700 !important;
        background-color: transparent !important; color: #000 !important;
        padding-bottom: 5px !important;
    }

    /* Button Styling: Small & Uniform */
    .stButton > button {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        max-width: 65px !important;
        max-height: 60px !important;
        border-radius: 14px !important;
        border: none !important;
        background-color: #F2F2F7 !important;
        color: #000 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0px !important;
    }
    .stButton > button:active { background-color: #000 !important; color: #FFF !important; }

    /* Darker Function Keys */
    div[data-testid="column"]:nth-child(n+4) button { background-color: #E5E5EA !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL STATE ---
if 'cmd' not in st.session_state: st.session_state.cmd = ""
if 'history' not in st.session_state: st.session_state.history = []

def press(key):
    if key == "AC": st.session_state.cmd = ""
    elif key == "DEL": st.session_state.cmd = st.session_state.cmd[:-1]
    elif key == "=": st.session_state.execute = True
    else: st.session_state.cmd += str(key)

# --- 3. BRANDING ---
st.markdown("<h1 class='brand-h1'>Verilogic-125 SRE</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-sub'>WITH AI ASSIST</p>", unsafe_allow_html=True)

# Live Math Visualization
if st.session_state.cmd:
    try:
        math_tex = sp.latex(sp.sympify(st.session_state.cmd.replace('×', '*').replace('÷', '/')))
        st.latex(math_tex)
    except: pass

# --- 4. DATA ENTRY ---
entry = st.text_input('', value=st.session_state.cmd, placeholder='0', label_visibility="collapsed", key="v125_main")
st.session_state.cmd = entry

# --- 5. THE 5-COLUMN KEYBOARD GRID ---
keys = [
    ['sin', 'cos', 'tan', 'sqrt', '÷'],
    ['(', ')', '^', 'log', '×'],
    ['7', '8', '9', '-', 'AC'],
    ['4', '5', '6', '+', 'DEL'],
    ['1', '2', '3', 'x', 'y'],
    ['0', '.', 'pi', 'e', '=']
]

for row_idx, row in enumerate(keys):
    cols = st.columns(5)
    for col_idx, key in enumerate(row):
        if cols[col_idx].button(key, use_container_width=True, key=f"k_{row_idx}_{col_idx}"):
            press(key)
            st.rerun()

# --- 6. SIDEBAR SETTINGS ---
with st.sidebar:
    st.markdown("### **SYSTEM_CORE**")
    t1, t2, t3 = st.tabs(["HISTORY", "UNITS", "LEGAL"])
    with t1:
        for idx, item in enumerate(reversed(st.session_state.history)):
            if st.button(f"{item['v']}", key=f"h_{idx}", use_container_width=True):
                st.session_state.cmd += str(item['v']); st.rerun()
    with t2:
        val = st.number_input("Input Converter", value=1.0)
        st.info(f"KG: {val*0.453:.2f} | KM: {val*1.609:.2f}")
    with t3:
        st.caption("TX Penal Code § 33.02 COMPLIANT")
        st.caption("LIABILITY WAIVER: EDUCATIONAL USE ONLY")

# --- 7. APEX MATH ENGINE ---
if st.session_state.get('execute') or "=" in st.session_state.cmd:
    try:
        clean = st.session_state.cmd.replace('×', '*').replace('÷', '/').replace('=', '')
        if 'x' in clean and not '=' in st.session_state.cmd:
            fig, ax = plt.subplots(figsize=(4, 2))
            x_r = np.linspace(-10, 10, 100); f_l = sp.lambdify(sp.Symbol('x'), sp.sympify(clean), 'numpy')
            ax.plot(x_r, f_l(x_r), color='black'); ax.grid(True); ax.set_facecolor('#FFFFFF')
            st.pyplot(fig); res = "Graph Plotted"
        else:
            res = sp.solve(sp.sympify(clean)) if 'x' in clean else sp.simplify(clean).evalf(6)
        st.success(f"**RESULT:** {res}")
        st.session_state.history.append({"v": res, "t": datetime.datetime.now()})
        st.session_state.execute = False
    except: st.error("LOGIC ERROR")
