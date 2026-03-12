import streamlit as st
import sympy as sp
import datetime
import matplotlib.pyplot as plt
import numpy as np

# --- 1. APPLE PRO DESIGN SYSTEM ---
st.set_page_config(page_title='Verilogic-125', layout='wide', initial_sidebar_state="collapsed")

# Custom CSS for Pure Monochrome Apple Aesthetic
st.markdown("""
<style>
    .stApp {background-color: #FFFFFF;}
    * {font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;}
    
    /* Main Input - iOS Style */
    .stTextInput input {
        border: none !important; border-bottom: 2px solid #000 !important;
        font-size: 2.8rem !important; text-align: center !important; font-weight: 800 !important;
        background-color: transparent !important; color: #000 !important; padding: 15px 0px !important;
    }
    
    /* Keypad - Tactile Grid */
    div.stButton > button {
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #000000 !important; border-radius: 12px !important;
        height: 62px !important; font-weight: 800 !important; font-size: 1.15rem !important;
        transition: 0.1s ease;
    }
    div.stButton > button:active { background-color: #000 !important; color: #FFF !important; transform: scale(0.96); }
    
    /* Operator Differentiation */
    div[data-testid="column"]:nth-child(5) button { background-color: #000 !important; color: #FFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. ELITE SESSION STATE ---
if 'cmd' not in st.session_state: st.session_state.cmd = ""
if 'history' not in st.session_state: st.session_state.history = []

def press(key):
    if key == "AC": st.session_state.cmd = ""
    elif key == "DEL": st.session_state.cmd = st.session_state.cmd[:-1]
    elif key == "=": st.session_state.solve_now = True
    else: st.session_state.cmd += str(key)

# --- 3. ROBUST SIDEBAR (History & Constants) ---
with st.sidebar:
    st.markdown("<h2 style='color:black;'>SYSTEM_CORE</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["HISTORY", "CONSTANTS"])
    
    with tab1:
        if not st.session_state.history: st.write("Tape is empty.")
        for idx, item in enumerate(reversed(st.session_state.history)):
            if st.button(f"{item['val']}", key=f"h_{idx}", use_container_width=True):
                st.session_state.cmd += str(item['val'])
                st.rerun()
            st.caption(f"Time: {item['time']}")

    with tab2:
        st.subheader("PHYSICS_LIB")
        c_lib = {"Light (c)": "299792458", "Planck (h)": "6.626e-34", "Gravity (g)": "9.806", "pi": "pi", "e": "e"}
        for name, val in c_lib.items():
            if st.button(name, use_container_width=True):
                st.session_state.cmd += val
                st.rerun()

# --- 4. SHOW YOUR WORK (LaTeX View) ---
st.markdown("<h1 style='text-align: center; color:black; margin-bottom:0;'>Verilogic-125</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight:800; font-size:0.7rem; letter-spacing:4px; opacity:0.6;'>APEX SCIENTIFIC SYSTEM</p>", unsafe_allow_html=True)

if st.session_state.cmd:
    try:
        clean_tex = st.session_state.cmd.replace('×', '*').replace('÷', '/')
        st.latex(sp.latex(sp.sympify(clean_tex)))
    except:
        st.markdown(f"<p style='text-align:center; color:#8E8E93;'>{st.session_state.cmd}</p>", unsafe_allow_html=True)

# --- 5. HYBRID INPUT (Native Keyboard + Keypad) ---
entry = st.text_input('', value=st.session_state.cmd, placeholder='0', label_visibility="collapsed", key="v125_apex")
if entry != st.session_state.cmd:
    st.session_state.cmd = entry

# --- 6. ADVANCED SCIENTIFIC KEYPAD ---
keys = [
    ['sin', 'cos', 'tan', 'sqrt', '÷'],
    ['(', ')', '^', 'log', '×'],
    ['7', '8', '9', 'pi', '-'],
    ['4', '5', '6', 'e', '+'],
    ['1', '2', '3', 'DEL', 'AC'],
    ['0', '.', 'x', 'y', '=']
]

for r_idx, row in enumerate(keys):
    cols = st.columns(5)
    for c_idx, key in enumerate(row):
        if cols[c_idx].button(key, use_container_width=True, key=f"k_{r_idx}_{c_idx}"):
            press(key)
            st.rerun()

# --- 7. CALCULATION ENGINE ---
if st.session_state.get('solve_now') or "=" in st.session_state.cmd:
    try:
        proc = st.session_state.cmd.replace('×', '*').replace('÷', '/').replace('=', '')
        if any(v in proc for v in ['x', 'y']):
            res = sp.solve(sp.sympify(proc))
        else:
            res = sp.simplify(proc).evalf(6)
        
        st.success(f"**RESULT:** {res}")
        st.session_state.history.append({"val": res, "time": datetime.datetime.now().strftime("%H:%M:%S")})
        st.session_state.solve_now = False
    except:
        st.error("SYNTAX_ERROR: Verify Sequence")
