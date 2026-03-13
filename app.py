import streamlit as st
import sympy as sp
import numpy as np
import time, hashlib

# 1. SAFARI GPU HEARTBEAT CONFIG
st.set_page_config(page_title="Verilogic Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. THE IRONCLAD DESIGN SYSTEM (Safari-Safe Version)
st.markdown("""
    <style>
    /* Kill White Screen Bug: Force hardware acceleration only after load */
    html, body { 
        background: #fbfbfd !important; 
        height: 100%; 
        margin: 0; 
        padding: 0;
        -webkit-overflow-scrolling: touch;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #fbfbfd !important;
        opacity: 1 !important;
        transition: opacity 0.5s ease-in;
    }

    /* GRID LOCK: Hard-coded 4 columns */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
    }
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
    }

    /* GLASS BUTTONS: Simplified for Safari Stability */
    .stButton>button {
        width: 100% !important; 
        height: 60px !important;
        border-radius: 16px !important; 
        background: #ffffff !important; 
        border: 1px solid #e5e5ea !important;
        font-weight: 600 !important; 
        font-size: 1.2rem !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    .stButton>button:active { background: #f2f2f7 !important; transform: scale(0.95); }

    /* Canvas Area */
    .canvas { height: 40vh; overflow-y: auto; padding: 15px; border-bottom: 2px solid #f2f2f7; }
    .entry { border-left: 4px solid #007aff; padding-left: 12px; margin-bottom: 15px; }
    
    footer, header, #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. STATE & LOGIC
if "history" not in st.session_state: st.session_state.history = []
if "input" not in st.session_state: st.session_state.input = ""

def solve():
    if not st.session_state.input: return
    try:
        q = st.session_state.input.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(q)
        res = float(expr.evalf())
        st.session_state.history.append({
            "q": st.session_state.input,
            "latex": sp.latex(expr),
            "res": f"{res:,.4f}"
        })
        st.session_state.input = ""
    except: st.toast("Check Math Syntax")

# 4. NOTEBOOK CANVAS
st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'''
        <div class="entry">
            <small style="opacity:0.3;">{item['q']}</small>
            {st.latex(item['latex'])}
            <div style="font-size:1.8rem; font-weight:800; color:#007aff;">= {item['res']}</div>
        </div>
    ''', unsafe_allow_html=True)

# Active Cursor Area
st.markdown(f'<div style="padding:10px; border-left:4px solid #ff9f0a; font-size:1.5rem; background:white; border-radius:10px;"><b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a;">|</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. DOCKED KEYPAD (4-Column Hard Locked)
rows = [
    ["AC", "√", "x²", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "π", "="]
]

for r_idx, row in enumerate(rows):
    cols = st.columns(4)
    for c_idx, label in enumerate(row):
        if cols[c_idx].button(label, key=f"v181_{r_idx}_{c_idx}"):
            if label == "AC": st.session_state.input = ""
            elif label == "=": solve()
            elif label == "√": st.session_state.input += "sqrt("
            elif label == "x²": st.session_state.input += "**2"
            else: st.session_state.input += str(label)
