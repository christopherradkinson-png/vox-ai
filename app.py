import streamlit as st
import sympy as sp
import datetime, requests
import matplotlib.pyplot as plt
import numpy as np

# --- 1. APPLE PRO DESIGN SYSTEM & GRID FIX ---
st.set_page_config(page_title='Verilogic-125', layout='wide')

st.markdown("""
<style>
    .stApp {background-color: #FFFFFF; color: #000000;}
    /* Remove top decoration and arrows */
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    
    * {font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;}
    
    /* Center the app and limit width to prevent "Super Wide" buttons */
    .block-container {
        max-width: 500px !important;
        padding-top: 2rem !important;
        margin: auto !important;
    }

    /* Force Horizontal Grid on Mobile */
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; gap: 5px !important;}

    /* Apple Input Bar */
    .stTextInput input {
        border: none !important; border-bottom: 2px solid #000 !important;
        font-size: 2rem !important; text-align: right !important; font-weight: 800 !important;
        background-color: transparent !important; color: #000 !important;
    }
    
    /* Tactile Round-Rect Buttons */
    div.stButton > button {
        background-color: #F2F2F7 !important; color: #000 !important;
        border: none !important; border-radius: 10px !important;
        height: 50px !important; font-weight: 700 !important; font-size: 1.1rem !important;
    }
    div.stButton > button:active { background-color: #000 !important; color: #FFF !important; }
    
    /* Dark Operators */
    div[data-testid="column"]:nth-child(4) button, 
    div[data-testid="column"]:nth-child(5) button { 
        background-color: #000000 !important; color: #FFFFFF !important; 
    }
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
st.markdown("<h1 style='text-align: center; margin-bottom:0;'>Verilogic-125</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:0.7rem; letter-spacing:2px; font-weight:800;'>VOX AI INTEGRATED</p>", unsafe_allow_html=True)

# Live LaTeX Work Preview
if st.session_state.cmd:
    try:
        math_tex = sp.latex(sp.sympify(st.session_state.cmd.replace('×', '*').replace('÷', '/')))
        st.latex(math_tex)
    except: pass

# --- 4. MAIN ENTRY BAR ---
entry = st.text_input('', value=st.session_state.cmd, placeholder='0', label_visibility="collapsed")
st.session_state.cmd = entry

# --- 5. LOGICAL SCIENTIFIC LAYOUT (nCalc/Casio Style) ---
# Grid: 5 columns. Numbers on left, Operators on right.
keys = [
    ['sin', 'cos', 'tan', 'sqrt', '÷'],
    ['(', ')', '^', 'log', '×'],
    ['7', '8', '9', 'DEL', 'AC'],
    ['4', '5', '6', '+', '-'],
    ['1', '2', '3', 'x', 'y'],
    ['0', '.', 'pi', 'e', '=']
]

for r_idx, row in enumerate(keys):
    cols = st.columns(5)
    for c_idx, key in enumerate(row):
        if cols[c_idx].button(key, use_container_width=True, key=f"btn_{r_idx}_{c_idx}"):
            press(key)
            st.rerun()

# --- 6. SIDEBAR (History, Units, Currency, Legal) ---
with st.sidebar:
    st.title("SYSTEM_CORE")
    t1, t2, t3, t4 = st.tabs(["HISTORY", "UNITS", "FX", "LEGAL"])
    with t1:
        for item in reversed(st.session_state.history):
            if st.button(f"{item['v']}", key=f"h_{item['t']}", use_container_width=True):
                st.session_state.cmd += str(item['v']); st.rerun()
    with t2:
        cat = st.selectbox("Type", ["Weight", "Volume", "Length"])
        val = st.number_input("Value", value=1.0)
        if cat == "Weight": st.write(f"{val} lb = {val * 0.453:.3f} kg")
        if cat == "Volume": st.write(f"{val} gal = {val * 3.785:.3f} L")
        if cat == "Length": st.write(f"{val} mi = {val * 1.609:.3f} km")
    with t3:
        if st.button("USD to EUR Rate"):
            try:
                r = requests.get("https://api.exchangerate-api.com").json()
                st.info(f"1 USD = {r['rates']['EUR']} EUR")
            except: st.error("Offline")
    with t4:
        st.caption("TX Penal Code § 33.02 Compliant.")
        st.caption("LIABILITY WAIVER: EDUCATIONAL USE ONLY.")

# --- 7. APEX CALC & GRAPH ENGINE ---
if st.session_state.get('execute') or "=" in st.session_state.cmd:
    try:
        clean = st.session_state.cmd.replace('×', '*').replace('÷', '/').replace('=', '')
        if 'x' in clean and not '=' in st.session_state.cmd:
            fig, ax = plt.subplots(figsize=(5, 3))
            x = np.linspace(-10, 10, 100); f = sp.lambdify(sp.Symbol('x'), sp.sympify(clean), 'numpy')
            ax.plot(x, f(x), color='black'); ax.grid(True); ax.set_facecolor('#FFFFFF')
            st.pyplot(fig)
            res = "Graph Plotted"
        else:
            res = sp.solve(sp.sympify(clean)) if 'x' in clean else sp.simplify(clean).evalf(6)
        st.success(f"RESULT: {res}")
        st.session_state.history.append({"v": res, "t": datetime.datetime.now().timestamp()})
        st.session_state.execute = False
    except: st.error("LOGIC ERROR")
