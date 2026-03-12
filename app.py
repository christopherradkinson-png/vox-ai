import streamlit as st
import sympy as sp

# 1. FORCED MOBILE CONFIG
st.set_page_config(page_title="Verilogic-125 Pro", layout="centered")

# 2. THE "NO-STACK" CSS ENGINE
# This is the final fix for the vertical stacking seen in your screenshot.
st.markdown("""
    <style>
    /* Force OLED Black background */
    .stApp { background-color: #000 !important; color: white !important; }
    
    /* THE ULTIMATE FIX: This forces 4 buttons per line, NO MATTER WHAT */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        gap: 8px !important;
        margin-bottom: 8px !important;
    }
    
    /* Ensures each button column takes exactly 25% of the width */
    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* Apple-Style Button Aesthetics */
    .stButton > button {
        width: 100% !important;
        height: 75px !important;
        border-radius: 16px !important;
        font-size: 24px !important;
        font-weight: 500 !important;
        background-color: #333333 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Apple Orange for the rightmost operators */
    div[data-testid="column"]:last-child .stButton > button {
        background-color: #FF9F0A !important;
    }

    /* iOS 18 Style Large Display */
    .calc-display {
        text-align: right;
        font-size: 75px;
        padding: 50px 15px 10px 15px;
        color: white;
        font-family: -apple-system, sans-serif;
        font-weight: 200;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CALCULATOR LOGIC (Session State)
if 'val' not in st.session_state: st.session_state.val = ""

def press(k):
    if k == "AC": st.session_state.val = ""
    elif k == "=":
        try:
            # AI Librarian Logic: Replaces visual chars with math code
            clean = st.session_state.val.replace('×', '*').replace('÷', '/')
            res = sp.sympify(clean).evalf()
            st.session_state.val = str(round(res, 6))
        except: st.session_state.val = "Error"
    else: st.session_state.val += str(k)

# 4. DISPLAY AREA
st.markdown(f'<div class="calc-display">{st.session_state.val or "0"}</div>', unsafe_allow_html=True)

# 5. THE HARD-CODED 4-COLUMN KEYBOARD
# By repeating st.columns(4) for every row, we ensure the CSS above locks them in.
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
        # Using on_click is more stable for mobile than checking if button():
        cols[i].button(label, key=f"btn_{label}", on_click=press, args=(label,))
