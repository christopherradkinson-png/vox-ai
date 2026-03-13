import streamlit as st
import sympy as sp
import io, base64

# 1. APPLE PRO CONFIG (White Background, Black Text)
st.set_page_config(page_title="Verilogic Pro", layout="centered")

st.markdown("""
    <style>
    /* White Canvas / Apple Typography */
    .main { background-color: #ffffff; color: #000000; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    [data-testid="stHeader"] { visibility: hidden; }
    
    /* Scrollable Math History (Desmos Style) */
    .history-container {
        height: 45vh; overflow-y: auto; padding: 20px;
        border-bottom: 1px solid #e5e5e7; display: flex; flex-direction: column-reverse;
    }
    .math-entry {
        border-left: 4px solid #007aff; padding-left: 15px; margin-bottom: 15px;
        font-size: 1.2rem; line-height: 1.6;
    }
    .result-pill { color: #007aff; font-weight: 600; font-size: 1.4rem; }

    /* Keypad Styling (Apple Dark) */
    .stButton>button {
        width: 100%; border-radius: 12px; height: 50px;
        background-color: #f2f2f7; color: #000; border: none;
        font-weight: 500; font-size: 1.1rem;
    }
    .op-btn button { background-color: #ff9f0a !important; color: white !important; font-size: 1.4rem !important; }
    .num-btn button { background-color: #e5e5ea !important; }
    .eq-btn button { background-color: #007aff !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGER
if "history" not in st.session_state: st.session_state.history = []
if "current_eq" not in st.session_state: st.session_state.current_eq = ""

# 3. MATH ENGINE (Multi-Result Engineering)
def calculate():
    eq = st.session_state.current_eq
    if not eq: return
    try:
        clean_eq = eq.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(clean_eq)
        # Get Decimal and Exact Radical/Fraction
        dec = str(round(float(expr.evalf()), 4))
        exact = str(sp.nsimplify(expr))
        
        # Save to history list
        st.session_state.history.append({"q": eq, "r": dec, "e": exact})
        st.session_state.current_eq = ""
    except:
        st.toast("Syntax Error")

def press(val):
    st.session_state.current_eq += str(val)

# 4. THE DESMOS-STYLE CANVAS (Top 50%)
st.markdown('<div class="history-container">', unsafe_allow_html=True)
# Current Active Line
st.markdown(f'<div class="math-entry"><b>{st.session_state.current_eq}</b><span style="opacity:0.3; animation: blink 1s infinite;">|</span></div>', unsafe_allow_html=True)

# Previous Calculations
for item in reversed(st.session_state.history):
    st.markdown(f'''
        <div class="math-entry">
            <div style="font-size: 0.9rem; opacity: 0.5;">{item['q']}</div>
            <div class="result-pill">= {item['r']}</div>
            <div style="font-size: 0.8rem; color: #8e8e93;">Exact: {item['e']}</div>
        </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. THE APPLE-STYLE KEYBOARD (Bottom 50%)
st.write("") # Spacer
# Row 1: System
r1 = st.columns(4)
if r1.button("AC"): st.session_state.current_eq = ""
if r1.button("√"): press("sqrt(")
if r1.button("x²"): press("**2")
if r1.button("÷"): press("÷")

# Row 2-4: Numbers & Basic Operators
nums = [
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"]
]
for row in nums:
    cols = st.columns(4)
    for i, val in enumerate(row):
        if cols[i].button(val): press(val)

# Row 5: Scientific & Result
r5 = st.columns(4)
if r5.button("0"): press("0")
if r5.button("."): press(".")
if r5.button("π"): press("pi")
if r5.button("=", type="primary"): calculate()

# Advanced Scientific (Expander to keep UI clean like Desmos)
with st.expander("Advanced Functions (sin, cos, log)"):
    adv = st.columns(4)
    if adv.button("sin"): press("sin(")
    if adv.button("cos"): press("cos(")
    if adv.button("log"): press("log10(")
    if adv.button("ln"): press("log(")
