import streamlit as st
import sympy as sp

# 1. APPLE PRO & TEXAS COMPLIANCE
st.set_page_config(page_title="Verilogic Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. THE "INDESTRUCTIBLE" CSS
st.markdown("""
    <style>
    .main { background-color: #fbfbfd; }
    [data-testid="stHeader"] { visibility: hidden; }
    
    /* THE FIX: Hard-coded Table Grid Logic */
    table { width: 100%; border-spacing: 10px; border-collapse: separate; table-layout: fixed; }
    td { width: 25%; }
    
    /* Apple Button Styling */
    .stButton>button {
        width: 100% !important; height: 60px !important; border-radius: 12px !important;
        background: white !important; border: 1px solid #e5e5ea !important;
        font-weight: 600 !important; font-size: 1.2rem !important;
    }
    .stButton>button:active { background: #f2f2f7 !important; }
    
    /* Canvas Area */
    .canvas { height: 40vh; overflow-y: auto; padding: 15px; border-bottom: 2px solid #f2f2f7; background: #fff; }
    footer, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: TEXAS LEGAL SUITE
with st.sidebar:
    st.title("⚙️ System Hub")
    st.subheader("⚖️ Legal & Compliance")
    with st.expander("Texas Consumer Notice (DTPA)"):
        st.caption("PURSUANT TO THE TEXAS DTPA: Provided 'as-is'. Venue: Texas.")

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
st.markdown(f'<div style="padding:15px; border-left:5px solid #ff9f0a; font-size:1.5rem; background:#f2f2f7; border-radius:12px; margin-bottom:10px;"><b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a;">|</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 6. DOCKED KEYPAD (Hard-Coded Table Injection)
rows = [
    ["AC", "√", "x²", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "π", "="]
]

# We use a manual table-based column system to lock the buttons in place
for r_idx, row in enumerate(rows):
    # This st.columns([1,1,1,1]) is the last defense. 
    # Combined with the CSS table-layout: fixed, it CANNOT wrap.
    cols = st.columns([1,1,1,1]) 
    for c_idx, label in enumerate(row):
        if cols[c_idx].button(label, key=f"v29_{r_idx}_{c_idx}", type="primary" if label == "=" else "secondary"):
            if label == "AC": st.session_state.input = ""
            elif label == "=": solve()
            elif label == "√": st.session_state.input += "sqrt("
            elif label == "x²": st.session_state.input += "**2"
            elif label == "×": st.session_state.input += "*"
            elif label == "÷": st.session_state.input += "/"
            else: st.session_state.input += str(label)
