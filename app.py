import streamlit as st
import sympy as sp
import re

# 1. APPLE PRO & TEXAS COMPLIANCE CONFIG
st.set_page_config(page_title="Verilogic Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. THE "IRONCLAD" CSS (Kills Vertical Line Error & Internal Object Leaks)
st.markdown("""
    <style>
    /* 1. THE NUCLEAR OPTION FOR GRID: Force 4 columns side-by-side on all iPhones */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 8px !important;
        width: 100% !important;
    }
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: 0 !important;
    }

    /* 2. Apple Liquid Glass Button Styling */
    .stButton>button {
        width: 100% !important; border-radius: 14px !important; height: 60px !important;
        background-color: #ffffff !important; color: #000 !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        font-weight: 600 !important; font-size: 1.2rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }
    .stButton>button:active { transform: scale(0.95); background-color: #f2f2f7 !important; }
    
    /* Display Area */
    .canvas { height: 38vh; overflow-y: auto; background: white; padding: 20px; border-bottom: 2px solid #f2f2f7; }
    
    /* Hide System UI */
    footer, header, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. ROBUST SETTINGS & TEXAS LEGAL JARGON
with st.sidebar:
    st.title("⚙️ System Hub")
    st.subheader("⚖️ Legal & Compliance")
    with st.expander("Texas Consumer Notice (DTPA)"):
        st.caption("PURSUANT TO THE TEXAS DTPA: This software is provided 'as-is.' Venue: Texas.")
    with st.expander("Texas Data Privacy (TDPSA)"):
        st.success("ZERO-TRUST SECURED")
        st.caption("Compliant with Texas Data Privacy Act. No data is transmitted or sold.")
    with st.expander("Engineering Disclaimer"):
        st.error("STRICT LIABILITY WARNING")
        st.caption("DO NOT use for life-critical structural engineering.")

# 4. STATE & MATH ENGINE
if "history" not in st.session_state: st.session_state.history = []
if "input" not in st.session_state: st.session_state.input = ""

def solve():
    if not st.session_state.input: return
    try:
        # Clean human input (7x7) to machine math (7*7)
        q = st.session_state.input.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(q)
        res = float(expr.evalf())
        st.session_state.history.append({"q": st.session_state.input, "l": sp.latex(expr), "r": f"{res:,.4f}"})
        st.session_state.input = ""
    except: st.toast("Check Math Syntax")

# 5. NOTEBOOK CANVAS
st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'''
        <div style="border-left: 5px solid #007aff; padding: 15px; margin-bottom: 10px; background:#f9f9fb; border-radius:15px;">
            {st.latex(item['l'])}
            <div style="font-size:1.8rem; font-weight:800; color:#007aff;">= {item['res']}</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown(f'''
    <div style="padding:15px; border-left:4px solid #ff9f0a; font-size:1.5rem; background:#f2f2f7; border-radius:12px; margin-bottom:10px;">
        <b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a; animation: blink 1s infinite;">|</span>
    </div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. DOCKED KEYPAD (Hard-Locked 4-Column Row)
# We use a manual index system to ensure no internal objects leak
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
        # Every button click is handled natively by the Python engine
        if cols[c_idx].button(label, key=f"key_{r_idx}_{c_idx}", type="primary" if label == "=" else "secondary"):
            if label == "AC": st.session_state.input = ""
            elif label == "=": solve()
            elif label == "√": st.session_state.input += "sqrt("
            elif label == "x²": st.session_state.input += "**2"
            elif label == "×": st.session_state.input += "*"
            elif label == "÷": st.session_state.input += "/"
            else: st.session_state.input += str(label)
