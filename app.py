import streamlit as st
import sympy as sp

# 1. APPLE PRO & TEXAS COMPLIANCE CONFIG
st.set_page_config(page_title="Verilogic Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. THE ROBUST SETTINGS & LEGAL SIDEBAR
with st.sidebar:
    st.title("⚙️ System Hub")
    
    # --- USER SETTINGS ---
    st.subheader("Preferences")
    precision = st.slider("Decimal Precision", 0, 10, 4)
    theme = st.radio("Interface Style", ["Apple Light", "Titanium Dark", "System Sync"])
    
    st.divider()
    
    # --- TEXAS LEGAL JARGON (#51, #84) ---
    st.subheader("⚖️ Legal & Compliance")
    
    with st.expander("Texas Consumer Notice (DTPA)"):
        st.caption("""
        PURSUANT TO THE TEXAS DECEPTIVE TRADE PRACTICES-CONSUMER PROTECTION ACT: 
        This software is provided 'as-is.' Verilogic Pro is a mathematical tool 
        and does not constitute professional engineering, financial, or legal advice. 
        Venue for any disputes is established in the State of Texas.
        """)

    with st.expander("Medical & Engineering Disclaimer"):
        st.error("STRICT LIABILITY WARNING")
        st.caption("""
        Calculations provided by this engine are for educational and informational 
        purposes only. DO NOT use Verilogic Pro for life-critical medical dosing, 
        structural engineering, or aerospace navigation. The user assumes 100% 
        risk for the application of results.
        """)

    with st.expander("Texas Data Privacy (TDPSA)"):
        st.success("ZERO-TRUST SECURED")
        st.caption("""
        Compliant with the Texas Data Privacy and Security Act (TDPSA). 
        No personal biometric or mathematical data is harvested, sold, 
        or transmitted to third-party servers. All 'Librarian' data stays on 
        this device.
        """)

    with st.expander("Intellectual Property"):
        st.caption("© 2026 Verilogic-125 SRE. All Rights Reserved. Proprietary Logic Engine.")

# 3. THE IRONCLAD CSS (Layout Fix)
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { width: 25% !important; flex: 1 1 25% !important; min-width: 0 !important; }
    .stButton>button { width: 100% !important; height: 60px !important; border-radius: 12px !important; font-weight: 600 !important; background-color: white !important; border: 1px solid #e5e5ea !important; }
    .op-col button { background-color: #ff9f0a !important; color: white !important; border: none !important; }
    .ac-col button { background-color: #a5a5a5 !important; color: black !important; border: none !important; }
    .canvas { height: 35vh; overflow-y: auto; background: white; padding: 20px; border-bottom: 2px solid #f2f2f7; }
    footer, header, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 4. STATE & LOGIC
if "history" not in st.session_state: st.session_state.history = []
if "input" not in st.session_state: st.session_state.input = ""

def solve():
    if not st.session_state.input: return
    try:
        q = st.session_state.input.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(q)
        res = float(expr.evalf())
        st.session_state.history.append({"q": st.session_state.input, "l": sp.latex(expr), "r": f"{res:,.{precision}f}"})
        st.session_state.input = ""
    except: st.toast("Check Syntax")

# 5. NOTEBOOK CANVAS
st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'<div style="border-left: 5px solid #007aff; padding: 15px; margin-bottom: 10px; background:#f9f9fb; border-radius:15px;">{st.latex(item["l"])}<div style="font-size:1.8rem; font-weight:800; color:#007aff;">= {item["r"]}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div style="padding:15px; border-left:5px solid #ff9f0a; font-size:1.5rem; background:#f2f2f7; border-radius:12px;"><b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a;">|</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. DOCKED KEYPAD (Forced 4-Column Grid)
rows = [["AC", "√", "x²", "÷"], ["7", "8", "9", "×"], ["4", "5", "6", "-"], ["1", "2", "3", "+"], ["0", ".", "π", "="]]
for r_idx, row in enumerate(rows):
    cols = st.columns(4)
    for c_idx, label in enumerate(row):
        if c_idx == 0 and r_idx == 0: with cols[c_idx]: st.markdown('<div class="ac-col">', unsafe_allow_html=True)
        elif c_idx == 3: with cols[c_idx]: st.markdown('<div class="op-col">', unsafe_allow_html=True)
        
        if cols[c_idx].button(label, key=f"key_{r_idx}_{c_idx}", type="primary" if label == "=" else "secondary"):
            if label == "AC": st.session_state.input = ""
            elif label == "=": solve()
            elif label == "√": st.session_state.input += "sqrt("
            elif label == "x²": st.session_state.input += "**2"
            elif label == "×": st.session_state.input += "*"
            elif label == "÷": st.session_state.input += "/"
            else: st.session_state.input += str(label)
