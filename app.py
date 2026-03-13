import streamlit as st
import sympy as sp

# 1. APPLE PRO CONFIG
st.set_page_config(page_title="Verilogic Pro", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #000000; font-family: -apple-system, sans-serif; }
    [data-testid="stHeader"] { visibility: hidden; }
    
    /* Scrollable Math History (Desmos/Notebook Style) */
    .history-container {
        height: 40vh; overflow-y: auto; padding: 20px;
        border-bottom: 2px solid #f2f2f7; display: flex; flex-direction: column;
    }
    .math-entry {
        border-left: 4px solid #007aff; padding-left: 15px; margin-bottom: 20px;
        font-size: 1.1rem;
    }
    .result-pill { color: #007aff; font-weight: 600; font-size: 1.5rem; margin-top: 5px; }

    /* Keypad Styling (Apple Rounded Rect) */
    .stButton>button {
        width: 100%; border-radius: 12px; height: 55px;
        background-color: #f2f2f7; color: #000; border: none;
        font-weight: 500; font-size: 1.2rem; margin-bottom: 10px;
    }
    /* Button Color Overrides */
    div[data-testid="stVerticalBlock"] > div:last-child .stButton>button { background-color: #007aff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE MANAGER
if "history" not in st.session_state: st.session_state.history = []
if "current_eq" not in st.session_state: st.session_state.current_eq = ""

# 3. MATH ENGINE
def calculate():
    eq = st.session_state.current_eq
    if not eq: return
    try:
        clean_eq = eq.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(clean_eq)
        dec = str(round(float(expr.evalf()), 6))
        exact = str(sp.nsimplify(expr))
        st.session_state.history.append({"q": eq, "r": dec, "e": exact})
        st.session_state.current_eq = ""
    except:
        st.error("Syntax Error")

def add_to_input(val):
    st.session_state.current_eq += str(val)

# 4. THE CANVAS (History)
st.markdown('<div class="history-container">', unsafe_allow_html=True)
for item in st.session_state.history:
    st.markdown(f'''
        <div class="math-entry">
            <div style="opacity: 0.4; font-size: 0.9rem;">{item['q']}</div>
            <div class="result-pill">= {item['r']}</div>
            <div style="font-size: 0.8rem; color: #8e8e93;">Exact: {item['e']}</div>
        </div>
    ''', unsafe_allow_html=True)

# Active Input Line
st.markdown(f'<div class="math-entry" style="border-left-color: #ff9f0a;"><b>{st.session_state.current_eq or "0"}</b><span style="color:#ff9f0a;">|</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. THE KEYPAD (Fixed Index Logic)
# Row 1
r1 = st.columns(4)
if r1[0].button("AC", key="ac"): st.session_state.current_eq = ""
if r1[1].button("√", key="sqrt"): add_to_input("sqrt(")
if r1[2].button("x²", key="sq"): add_to_input("**2")
if r1[3].button("÷", key="div"): add_to_input("/")

# Row 2
r2 = st.columns(4)
if r2[0].button("7", key="7"): add_to_input("7")
if r2[1].button("8", key="8"): add_to_input("8")
if r2[2].button("9", key="9"): add_to_input("9")
if r2[3].button("×", key="mul"): add_to_input("*")

# Row 3
r3 = st.columns(4)
if r3[0].button("4", key="4"): add_to_input("4")
if r3[1].button("5", key="5"): add_to_input("5")
if r3[2].button("6", key="6"): add_to_input("6")
if r3[3].button("-", key="sub"): add_to_input("-")

# Row 4
r4 = st.columns(4)
if r4[0].button("1", key="1"): add_to_input("1")
if r4[1].button("2", key="2"): add_to_input("2")
if r4[2].button("3", key="3"): add_to_input("3")
if r4[3].button("+", key="add"): add_to_input("+")

# Row 5
r5 = st.columns(4)
if r5[0].button("0", key="0"): add_to_input("0")
if r5[1].button(".", key="dot"): add_to_input(".")
if r5[2].button("π", key="pi"): add_to_input("pi")
if r5[3].button("=", key="eq", type="primary"): calculate()
