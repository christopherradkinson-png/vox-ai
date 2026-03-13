import streamlit as st
import sympy as sp
import numpy as np
import scipy.constants as const
import pandas as pd
import matplotlib.pyplot as plt
import io, base64, time

# 1. ADVANCED ENGINEERING CONFIG
st.set_page_config(page_title="Verilogic Pro Eng", layout="centered", initial_sidebar_state="collapsed")

# 2. IRONCLAD CSS (Kills Vertical Line Error & Forces Apple Glass)
st.markdown("""
    <style>
    /* Force 4-Column Grid on Mobile - The Final Fix */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
        width: 100% !important;
        align-items: center !important;
    }
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: 0 !important;
    }

    /* Apple Liquid Glass Styling */
    .main { background-color: #fbfbfd; }
    .stButton>button {
        width: 100% !important; border-radius: 16px !important; height: 62px !important;
        background: #ffffff !important; border: 1px solid rgba(0,0,0,0.05) !important;
        font-weight: 600 !important; font-size: 1.2rem !important;
        transition: transform 0.1s ease !important;
    }
    .stButton>button:active { transform: scale(0.92); background: #f2f2f7 !important; }
    
    /* Notebook Display */
    .canvas { height: 35vh; overflow-y: auto; padding: 20px; border-bottom: 2px solid #f2f2f7; background: #fff; }
    .entry { border-left: 5px solid #007aff; padding-left: 15px; margin-bottom: 20px; }
    
    footer, header, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. ADVANCED SCIENCE ENGINE
if "history" not in st.session_state: st.session_state.history = []
if "input" not in st.session_state: st.session_state.input = ""

def solve_eng():
    if not st.session_state.input: return
    try:
        # Replace scientific symbols with machine math
        q = st.session_state.input.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(q)
        res_dec = float(expr.evalf())
        res_exact = str(sp.nsimplify(expr))
        
        st.session_state.history.append({
            "latex": sp.latex(expr),
            "dec": f"{res_dec:,.4f}",
            "exact": res_exact,
            "raw": st.session_state.input
        })
        st.session_state.input = ""
    except: st.toast("Check Scientific Syntax")

# 4. NOTEBOOK CANVAS (Textbook Math Rendering)
st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'''
        <div class="entry">
            <small style="opacity:0.3; font-size:0.7rem;">{item['raw']}</small>
            {st.latex(item['latex'])}
            <div style="font-size:1.8rem; font-weight:800; color:#007aff;">= {item['dec']}</div>
            <div style="font-size:0.7rem; opacity:0.6;">Exact: {item['exact']}</div>
        </div>
    ''', unsafe_allow_html=True)

# Active Input Line
st.markdown(f'''
    <div style="padding:15px; border-left:5px solid #ff9f0a; font-size:1.5rem; background:#fff; border-radius:12px;">
        <b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a;">|</span>
    </div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. DOCKED SCIENTIFIC KEYPAD
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
        if cols[c_idx].button(label, key=f"vpro_{r_idx}_{c_idx}"):
            if label == "AC": st.session_state.input = ""
            elif label == "=": solve_eng()
            elif label == "√": st.session_state.input += "sqrt("
            elif label == "x²": st.session_state.input += "**2"
            else: st.session_state.input += str(label)

st.markdown('<div style="text-align:center; font-size:0.6rem; opacity:0.2; letter-spacing:2px; margin-top:20px;">VERILOGIC SCIENTIFIC STATION v21.0</div>', unsafe_allow_html=True)
