import streamlit as st
import sympy as sp
import datetime, requests
import matplotlib.pyplot as plt
import numpy as np

# --- 1. APPLE ELITE INTERFACE ENGINE ---
st.set_page_config(page_title='Verilogic-125 SRE', layout='centered', initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp {background-color: #FFFFFF; color: #000000;}
    header, .stDeployButton, #MainMenu, [data-testid="stHeader"] { visibility: hidden !important; height: 0px !important; }
    
    /* Center App & Lock Width for Professional Feel */
    .block-container { max-width: 600px !important; padding-top: 2rem !important; }

    /* iPhone Input Bar: Left-Aligned Placeholder, Ultra-Clean */
    .stTextInput input {
        border: none !important; border-bottom: 2px solid #000 !important;
        font-size: 2.8rem !important; text-align: left !important; font-weight: 700 !important;
        background-color: transparent !important; color: #000 !important;
        padding: 10px 0px !important; border-radius: 0px !important;
    }
    ::placeholder { color: #D1D1D6 !important; opacity: 1; }

    /* THE GRID FIX: Force 7-Column Scientific Layout */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
        gap: 4px !important; margin-bottom: -10px !important;
    }
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }

    /* Apple Tactile Keys: Small, Uniform Squares */
    .stButton > button {
        width: 100% !important; aspect-ratio: 1/1 !important;
        border-radius: 10px !important; border: none !important;
        background-color: #F2F2F7 !important; color: #000 !important;
        font-weight: 700 !important; font-size: 0.9rem !important;
        padding: 0px !important; transition: 0.1s;
    }
    .stButton > button:active { background-color: #000 !important; color: #FFF !important; transform: scale(0.92); }
    
    /* Number Pad & Action Button Differentiation */
    div[data-testid="column"]:nth-child(n+5) button { background-color: #E5E5EA !important; }
    button[kind="primary"] { background-color: #000 !important; color: #FFF !important; font-size: 0.8rem !important; }

    /* Branding Fonts */
    .brand-h1 { text-align: center; font-weight: 800; font-size: 2.2rem; margin: 0; color: #000; }
    .brand-sub { text-align: center; font-weight: 700; font-size: 0.8rem; letter-spacing: 2px; color: #8E8E93; margin-top: -5px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL STATE ---
if 'cmd' not in st.session_state: st.session_state.cmd = ""
if 'history' not in st.session_state: st.session_state.history = []

def press(key):
    if key == "AC": st.session_state.cmd = ""
    elif key == "DEL": st.session_state.cmd = st.session_state.cmd[:-1]
    elif key == "EXE": st.session_state.execute = True
    else: st.session_state.cmd += str(key)

# --- 3. BRANDING ---
st.markdown("<div class='brand-h1'>Verilogic-125 SRE</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-sub'>WITH AI ASSIST</div>", unsafe_allow_html=True)

# Live LaTeX Rendering (The "Work" Screen)
if st.session_state.cmd:
    try:
        math_tex = sp.latex(sp.sympify(st.session_state.cmd.replace('×', '*').replace('÷', '/')))
        st.latex(math_tex)
    except: pass

# --- 4. DATA ENTRY BAR ---
entry = st.text_input('', value=st.session_state.cmd, placeholder='0', label_visibility="collapsed", key="v125_entry")
st.session_state.cmd = entry

# --- 5. ELITE 7-COLUMN KEYBOARD (Scientific + Numbers) ---
# Format: [Scientific Functions | Number Pad | Operators]
keys = [
    ['sin', 'cos', 'tan', '7', '8', '9', '÷'],
    ['asin', 'acos', 'atan', '4', '5', '6', '×'],
    ['log', 'ln', 'sqrt', '1', '2', '3', '-'],
    ['(', ')', '^', '0', '.', 'pi', '+'],
    ['diff', 'integ', 'x', 'y', 'DEL', 'AC', 'EXE']
]

for row in keys:
    cols = st.columns(7)
    for i, key in enumerate(row):
        is_exe = "primary" if key == "EXE" else "secondary"
        if cols[i].button(key, type=is_exe, key=f"k_{key}_{keys.index(row)}_{i}"):
            press(key)
            st.rerun()

# --- 6. SETTINGS SIDEBAR (History & Units) ---
with st.sidebar:
    st.title("SYSTEM_CORE")
    t1, t2, t3 = st.tabs(["HISTORY", "UNITS", "LEGAL"])
    with t1:
        for idx, item in enumerate(reversed(st.session_state.history)):
            if st.button(f"{item['v']}", key=f"hist_{idx}", use_container_width=True):
                st.session_state.cmd += str(item['v']); st.rerun()
    with t2:
        val = st.number_input("Value", value=1.0)
        st.info(f"KG: {val*0.453:.2f} | KM: {val*1.609:.2f}")
    with t3:
        st.caption("TX Penal Code § 33.02 COMPLIANT")
        st.caption("LIABILITY WAIVER: EDUCATIONAL USE ONLY")

# --- 7. APEX ENGINE (Graphing & Advanced Math) ---
if st.session_state.get('execute'):
    try:
        p = st.session_state.cmd.replace('×', '*').replace('÷', '/').replace('diff', 'diff').replace('integ', 'integrate')
        if 'x' in p and '(' in p and not '=' in p: # Graphing check
            fig, ax = plt.subplots(figsize=(5, 2.5))
            x_range = np.linspace(-10, 10, 100)
            f_lamb = sp.lambdify(sp.Symbol('x'), sp.sympify(p), 'numpy')
            ax.plot(x_range, f_lamb(x_range), color='black', linewidth=2)
            ax.grid(True, color='#E5E5EA'); ax.set_facecolor('#FFFFFF')
            st.pyplot(fig); res = "Graph Generated"
        else:
            res = sp.solve(sp.sympify(p)) if '=' in p else sp.simplify(p).evalf(6)
        st.success(f"**RESULT:** {res}")
        st.session_state.history.append({"v": res, "t": datetime.datetime.now()})
        st.session_state.execute = False
    except: st.error("LOGIC ERROR")
