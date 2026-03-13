import streamlit as st
import sympy as sp
import hashlib
import time

# 1. APPLE PRO CONFIG
st.set_page_config(page_title="Verilogic Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. THE "GOD-MODE" CSS (Forces the exact grid in your photo)
st.markdown("""
    <style>
    /* 1. Force the 4-column grid horizontally on ALL devices */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
    }
    [data-testid="column"] {
        flex: 1 1 0% !important;
        width: 25% !important;
        min-width: 0 !important;
    }

    /* 2. Style buttons to match your photo exactly */
    .stButton>button {
        width: 100% !important;
        height: 65px !important;
        border-radius: 15px !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        border: none !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: transform 0.1s !important;
    }
    .stButton>button:active { transform: scale(0.95); }

    /* Orange Operators */
    div[data-testid="column"]:last-child .stButton>button {
        background-color: #ff9f0a !important;
        color: white !important;
    }
    /* Blue Equals */
    button[kind="primary"] {
        background-color: #007aff !important;
        color: white !important;
    }
    /* AC Gray */
    div[data-testid="stHorizontalBlock"] div:first-child .stButton>button {
        background-color: #a5a5a5 !important;
        color: black !important;
    }

    /* Notebook Display Area */
    .canvas { height: 35vh; overflow-y: auto; background: white; padding: 20px; border-radius: 20px; margin-bottom: 20px; }
    
    footer, header, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. STATE WATCHDOG
if "history" not in st.session_state: st.session_state.history = []
if "input" not in st.session_state: st.session_state.input = ""

def solve():
    if not st.session_state.input: return
    try:
        q = st.session_state.input.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(q)
        res = float(expr.evalf())
        sig = hashlib.sha256(f"{q}{res}".encode()).hexdigest()[:8].upper()
        st.session_state.history.append({"q": st.session_state.input, "l": sp.latex(expr), "r": f"{res:,.4f}", "s": sig})
        st.session_state.input = ""
    except: st.toast("Check Math Syntax")

# 4. NOTEBOOK CANVAS
st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'''
        <div style="border-left: 5px solid #007aff; padding: 15px; margin-bottom: 10px; background:#f9f9fb; border-radius:0 15px 15px 0;">
            <small style="opacity:0.3;">SIG: {item['s']}</small><br>
            {st.latex(item['l'])}
            <div style="font-size:1.8rem; font-weight:800; color:#007aff;">= {item['r']}</div>
        </div>
    ''', unsafe_allow_html=True)

# Active Cursor Line
st.markdown(f'''
    <div style="padding:20px; border-left:5px solid #ff9f0a; font-size:1.8rem; background:#f2f2f7; border-radius:15px;">
        <b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a; animation: blink 1s infinite;">|</span>
    </div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. DOCKED KEYPAD (Matched to your Photo)
# Using a manual layout to ensure the grid is rock-solid
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
        # We handle each button press natively in Python to prevent "None" errors
        if cols[c_idx].button(label, key=f"btn_{r_idx}_{c_idx}", type="primary" if label == "=" else "secondary"):
            if label == "AC": st.session_state.input = ""
            elif label == "=": solve()
            elif label == "√": st.session_state.input += "sqrt("
            elif label == "x²": st.session_state.input += "**2"
            elif label == "×": st.session_state.input += "*"
            elif label == "÷": st.session_state.input += "/"
            else: st.session_state.input += str(label)
