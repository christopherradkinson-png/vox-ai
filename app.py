import streamlit as st
import sympy as sp

st.set_page_config(page_title="Verilogic-125", layout="centered")

# 1. THE "FORCED GRID" CSS (This kills the vertical stack)
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    
    /* FORCE 4 COLUMNS: This is the magic fix for your screenshot */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: 0px !important;
    }

    /* Apple Button Styling */
    .stButton > button {
        width: 100% !important;
        height: 70px !important;
        border-radius: 12px !important;
        font-size: 24px !important;
        background-color: #333333 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Orange Side Operators */
    div[data-testid="column"]:last-child .stButton > button {
        background-color: #FF9F0A !important;
    }

    /* Screen Display */
    .calc-screen {
        text-align: right; font-size: 70px; padding: 40px 10px;
        color: white; font-family: -apple-system, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIC ENGINE
if 'val' not in st.session_state: st.session_state.val = ""

def press(k):
    if k == "AC": st.session_state.val = ""
    elif k == "=":
        try:
            res = sp.sympify(st.session_state.val.replace('×', '*').replace('÷', '/')).evalf()
            st.session_state.val = str(round(res, 6))
        except: st.session_state.val = "Error"
    else: st.session_state.val += str(k)

# 3. INTERFACE
st.markdown(f'<div class="calc-screen">{st.session_state.val or "0"}</div>', unsafe_allow_html=True)

# 4. THE ROBUST KEYBOARD GRID
# We manually define each row to ensure the CSS above can lock them in place
rows = [
    ["AC", "(", ")", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "π", "="]
]

for row in rows:
    cols = st.columns(4)
    for i, label in enumerate(row):
        if cols[i].button(label, key=f"btn_{label}"):
            press(label)
            st.rerun()
