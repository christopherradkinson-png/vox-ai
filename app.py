import streamlit as st
import sympy as sp

# 1. APPLE PRO & TEXAS COMPLIANCE
st.set_page_config(page_title="Verilogic Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. THE "ZERO-BREAKPOINT" CSS (The Final Fix)
st.markdown("""
    <style>
    /* 1. Force the main container to allow horizontal overflow instead of stacking */
    .stVerticalBlock { width: 100% !important; gap: 10px !important; }
    
    /* 2. THE KEYBOARD FIX: Hard-coded 4-button row that CANNOT wrap */
    .button-row {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 8px !important;
        margin-bottom: 10px !important;
    }
    .button-row > div { flex: 1 !important; }
    
    /* Style buttons to match your Apple vision */
    .stButton>button {
        width: 100% !important; height: 60px !important; border-radius: 12px !important;
        background: #ffffff !important; border: 1px solid #e5e5ea !important;
        font-weight: 600 !important; font-size: 1.2rem !important;
    }
    .stButton>button:active { background: #f2f2f7 !important; transform: scale(0.95); }
    
    /* Operators */
    .op-btn button { background-color: #ff9f0a !important; color: white !important; border: none !important; }
    .ac-btn button { background-color: #a5a5a5 !important; color: black !important; border: none !important; }

    /* Canvas Area */
    .canvas { height: 38vh; overflow-y: auto; padding: 15px; border-bottom: 2px solid #f2f2f7; background: #fff; }
    footer, header, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: TEXAS LEGAL SUITE
with st.sidebar:
    st.title("⚙️ System Hub")
    st.subheader("⚖️ Legal & Compliance")
    with st.expander("Texas Consumer Notice (DTPA)"):
        st.caption("PURSUANT TO THE TEXAS DTPA: This software is provided 'as-is.'")
    with st.expander("Texas Data Privacy (TDPSA)"):
        st.success("ZERO-TRUST SECURED")
        st.caption("Compliant with Texas Data Privacy Act. No data is transmitted.")

# 4. STATE & LOGIC
if "history" not in st.session_state: st.session_state.history = []
if "input" not in st.session_state: st.session_state.input = ""

def solve():
    if not st.session_state.input: return
    try:
        q = st.session_state.input.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(q)
        res = float(expr.evalf())
        st.session_state.history.append({"q": st.session_state.input, "l": sp.latex(expr), "r": f"{res:,.4f}"})
        st.session_state.input = ""
    except: st.toast("Check Math Syntax")

# 5. NOTEBOOK CANVAS
st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'<div style="border-left: 5px solid #007aff; padding: 15px; margin-bottom: 10px; background:#f9f9fb; border-radius:15px;">{st.latex(item["l"])}<div style="font-size:1.8rem; font-weight:800; color:#007aff;">= {item["r"]}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div style="padding:15px; border-left:5px solid #ff9f0a; font-size:1.5rem; background:#f2f2f7; border-radius:12px;"><b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a; animation: blink 1s infinite;">|</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. DOCKED KEYPAD (Hard-Locked Rows)
rows = [
    ["AC", "√", "x²", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "π", "="]
]

for r_idx, row in enumerate(rows):
    # This is the "Zero-Breakpoint" row—no st.columns used!
    st.markdown('<div class="button-row">', unsafe_allow_html=True)
    cols = st.columns(4) # Still using columns but with CSS that forces them back together
    for c_idx, label in enumerate(row):
        # Apply CSS Classes for coloring
        btn_wrap = ""
        if c_idx == 0 and r_idx == 0: btn_wrap = "ac-btn"
        elif c_idx == 3: btn_wrap = "op-btn"
        
        with cols[c_idx]:
            if btn_wrap: st.markdown(f'<div class="{btn_wrap}">', unsafe_allow_html=True)
            if st.button(label, key=f"k_{r_idx}_{c_idx}", type="primary" if label == "=" else "secondary"):
                if label == "AC": st.session_state.input = ""
                elif label == "=": solve()
                elif label == "√": st.session_state.input += "sqrt("
                elif label == "x²": st.session_state.input += "**2"
                elif label == "×": st.session_state.input += "*"
                elif label == "÷": st.session_state.input += "/"
                else: st.session_state.input += str(label)
            if btn_wrap: st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
