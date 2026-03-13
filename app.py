import streamlit as st
import sympy as sp

# 1. APPLE PRO & TEXAS COMPLIANCE CONFIG
st.set_page_config(page_title="Verilogic Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. THE ROBUST SETTINGS & LEGAL SIDEBAR
with st.sidebar:
    st.title("⚙️ System Hub")
    
    st.subheader("Preferences")
    precision = st.slider("Decimal Precision", 0, 10, 4)
    
    st.divider()
    
    st.subheader("⚖️ Legal & Compliance")
    
    with st.expander("Texas Consumer Notice (DTPA)"):
        st.caption("""
        PURSUANT TO THE TEXAS DECEPTIVE TRADE PRACTICES ACT: 
        This software is provided 'as-is.' Verilogic Pro is a mathematical tool 
        and does not constitute professional engineering or legal advice.
        """)

    with st.expander("Medical & Engineering Disclaimer"):
        st.error("STRICT LIABILITY WARNING")
        st.caption("""
        DO NOT use Verilogic Pro for life-critical medical dosing or 
        structural engineering. The user assumes 100% risk.
        """)

    with st.expander("Texas Data Privacy (TDPSA)"):
        st.success("ZERO-TRUST SECURED")
        st.caption("""
        Compliant with the Texas Data Privacy and Security Act. 
        No mathematical data is harvested or transmitted.
        """)

# 3. THE IRONCLAD CSS
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; gap: 8px !important; }
    [data-testid="column"] { width: 25% !important; flex: 1 1 25% !important; min-width: 0 !important; }
    .stButton>button { width: 100% !important; height: 60px !important; border-radius: 12px !important; font-weight: 600 !important; background-color: white !important; border: 1px solid #e5e5ea !important; }
    
    /* Specific Button Colors */
    .ac-btn button { background-color: #a5a5a5 !important; color: black !important; }
    .op-btn button { background-color: #ff9f0a !important; color: white !important; }
    
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
        st.session_state.history.append({"l": sp.latex(expr), "r": f"{res:,.{precision}f}"})
        st.session_state.input = ""
    except: st.toast("Check Syntax")

# 5. NOTEBOOK CANVAS
st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'<div style="border-left: 5px solid #007aff; padding: 15px; margin-bottom: 10px; background:#f9f9fb; border-radius:15px;">{st.latex(item["l"])}<div style="font-size:1.8rem; font-weight:800; color:#007aff;">= {item["r"]}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div style="padding:15px; border-left:5px solid #ff9f0a; font-size:1.5rem; background:#f2f2f7; border-radius:12px;"><b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a;">|</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. DOCKED KEYPAD (Corrected Indentation)
rows = [["AC", "√", "x²", "÷"], ["7", "8", "9", "×"], ["4", "5", "6", "-"], ["1", "2", "3", "+"], ["0", ".", "π", "="]]

for r_idx, row in enumerate(rows):
    cols = st.columns(4)
    for c_idx, label in enumerate(row):
        # Color Logic
        btn_class = ""
        if c_idx == 0 and r_idx == 0: btn_class = "ac-btn"
        elif c_idx == 3: btn_class = "op-btn"
        
        with cols[c_idx]:
            if btn_class: st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
            if st.button(label, key=f"k_{r_idx}_{c_idx}", type="primary" if label == "=" else "secondary"):
                if label == "AC": st.session_state.input = ""
                elif label == "=": solve()
                elif label == "√": st.session_state.input += "sqrt("
                elif label == "x²": st.session_state.input += "**2"
                elif label == "×": st.session_state.input += "*"
                elif label == "÷": st.session_state.input += "/"
                else: st.session_state.input += str(label)
            if btn_class: st.markdown('</div>', unsafe_allow_html=True)
