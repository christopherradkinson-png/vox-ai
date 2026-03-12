import streamlit as st
import sympy as sp

st.set_page_config(page_title="Verilogic-125", layout="centered")

# 1. FIXED CSS GRID (The "Anti-Collapse" Engine)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    
    /* Forces a 4-column grid on ALL mobile screens */
    .iphone-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        padding: 10px;
    }
    
    /* Apple Button Styling */
    .stButton > button {
        width: 100% !important;
        height: 75px !important;
        border-radius: 18px !important;
        font-size: 24px !important;
        font-weight: 500 !important;
        background-color: #333333 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Special Colors for Operators & Clear */
    .stButton > button[key*="op_"] { background-color: #FF9F0A !important; }
    .stButton > button[key*="cl_"] { background-color: #A5A5A5 !important; color: black !important; }
    
    /* The Screen Display */
    .calc-screen {
        text-align: right;
        font-size: 80px;
        padding: 40px 20px;
        font-family: -apple-system, sans-serif;
        font-weight: 200;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. APP LOGIC
if 'input' not in st.session_state: st.session_state.input = ""

def press(k):
    if k == "AC": st.session_state.input = ""
    elif k == "=":
        try:
            res = sp.sympify(st.session_state.input.replace('×', '*').replace('÷', '/')).evalf()
            st.session_state.input = str(round(res, 6))
        except: st.session_state.input = "Error"
    else: st.session_state.input += str(k)

# 3. THE INTERFACE
st.markdown(f'<div class="calc-screen">{st.session_state.input or "0"}</div>', unsafe_allow_html=True)

# 4. THE 4-COLUMN MANUAL GRID (No Stacking Possible)
# We use individual containers to ensure they don't collapse
grid_labels = [
    ("AC", "cl_"), ("(", "num"), (")", "num"), ("÷", "op_"),
    ("7", "num"), ("8", "num"), ("9", "num"), ("×", "op_"),
    ("4", "num"), ("5", "num"), ("6", "num"), ("-", "op_"),
    ("1", "num"), ("2", "num"), ("3", "num"), ("+", "op_"),
    ("0", "num"), (".", "num"), ("π", "num"), ("=", "op_")
]

# Manual loop with 4-column break to prevent stacking
for i in range(0, len(grid_labels), 4):
    cols = st.columns(4)
    for j in range(4):
        label, style = grid_labels[i+j]
        if cols[j].button(label, key=f"btn_{style}_{label}"):
            press(label)
            st.rerun()
