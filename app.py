import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 1. APPLE OPTIMIZED UI (CSS)
st.set_page_config(page_title="QuantumCalc Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="column"] { padding: 1px !important; flex: 1 1 0% !important; min-width: 0px !important; }
    [data-testid="stVerticalBlock"] > div { gap: 4px !important; }
    
    .calc-display {
        background: #1c1c1e; border-radius: 20px; color: white; 
        text-align: right; font-size: 60px; padding: 40px 20px; 
        font-family: -apple-system, sans-serif; font-weight: 200;
    }
    
    .stButton > button {
        width: 100% !important; border-radius: 12px !important;
        height: 70px !important; border: none !important;
        font-size: 24px !important; transition: 0.1s;
    }
    .stButton > button:active { transform: scale(0.95); opacity: 0.7; }
    
    /* Apple Colors */
    div.stButton > button[key*="num"] { background-color: #333333; color: white; }
    div.stButton > button[key*="op"] { background-color: #FF9F0A; color: white; }
    div.stButton > button[key*="func"] { background-color: #A5A5A5; color: black; }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE (The Brain)
if 'input' not in st.session_state: st.session_state.input = ""
if 'history' not in st.session_state: st.session_state.history = []

# 3. LIBRARIAN FUNCTIONS
def solve_math(query):
    try:
        # AI Logic for Human Input
        q_clean = query.replace('×', '*').replace('÷', '/').replace('−', '-')
        expr = sp.sympify(q_clean)
        return str(round(expr.evalf(), 6))
    except:
        return "Error"

# 4. TOP HEADER
t1, t2 = st.columns([0.8, 0.2])
with t1: st.markdown("<h2 style='font-weight:300;'>QuantumCalc</h2>", unsafe_allow_html=True)
with t2: 
    if st.button("🎙️", key="btn_voice"): st.toast("Voice Mode Active")

# 5. DISPLAY
st.markdown(f'<div class="calc-display">{st.session_state.input or "0"}</div>', unsafe_allow_html=True)

# 6. KEYBOARD GRID
def press(label):
    if label == "AC": st.session_state.input = ""
    elif label == "=":
        ans = solve_math(st.session_state.input)
        st.session_state.history.append(f"{st.session_state.input} = {ans}")
        st.session_state.input = ans
    else:
        st.session_state.input += str(label)

layout = [
    [("AC", "func"), ("(", "func"), (")", "func"), ("÷", "op")],
    [("7", "num"), ("8", "num"), ("9", "num"), ("×", "op")],
    [("4", "num"), ("5", "num"), ("6", "num"), ("−", "op")],
    [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
    [("0", "num"), (".", "num"), ("π", "num"), ("=", "op")]
]

for row in layout:
    cols = st.columns(4)
    for i, (label, kind) in enumerate(row):
        if cols[i].button(label, key=f"k_{kind}_{label}"):
            press(label)
            st.rerun()

# 7. WORK SHOWCASE (Lower Section)
if st.session_state.history:
    with st.expander("Show Your Work / History"):
        for item in reversed(st.session_state.history):
            st.write(item)
