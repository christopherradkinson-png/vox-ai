import streamlit as st
import sympy as sp
import datetime, requests
import matplotlib.pyplot as plt
import numpy as np

# --- 1. APPLE "LIQUID GLASS" DESIGN ENGINE ---
st.set_page_config(page_title='Verilogic-125 SRE', layout='centered', initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Global Liquid Backdrop */
    .stApp {
        background: linear-gradient(180deg, #F2F2F7 0%, #FFFFFF 100%);
        color: #000000;
    }
    header, [data-testid="stHeader"] { visibility: hidden !important; height: 0px !important; }
    
    /* Center & Lock Content Width */
    .block-container { max-width: 420px !important; padding: 2rem 1rem !important; margin: auto !important; }

    /* Glassmorphic Branding */
    .brand-h1 { text-align: center; font-weight: 800; font-size: 2.4rem; color: #000; letter-spacing: -1px; margin-bottom: 0; }
    .brand-sub { text-align: center; font-weight: 700; font-size: 0.75rem; letter-spacing: 3px; color: #8E8E93; text-transform: uppercase; margin-top: -5px; margin-bottom: 30px; }

    /* iPhone Input Bar: Translucent Glass */
    .stTextInput input {
        border: none !important;
        border-bottom: 1.5px solid rgba(0,0,0,0.1) !important;
        font-size: 2.6rem !important;
        text-align: left !important;
        font-weight: 700 !important;
        background-color: transparent !important;
        color: #000 !important;
        padding: 15px 0px !important;
        border-radius: 0px !important;
    }

    /* Tactile Grid: Forced 5-Column Logic */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;
        gap: 10px !important; margin-bottom: 10px !important;
    }
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }

    /* Apple "Taptic" Buttons: Scale & Depth */
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1/1 !important;
        border-radius: 18px !important; /* Softer Apple Corners */
        border: 1px solid rgba(0,0,0,0.05) !important;
        background: #FFFFFF !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.04) !important;
        color: #000 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:active {
        transform: scale(0.9) !important;
        background: #E5E5EA !important;
    }

    /* High-Contrast Operators */
    div[data-testid="column"]:nth-child(5) button {
        background: #000000 !important;
        color: #FFFFFF !important;
    }

    /* Glass Sidebar Settings */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0,0,0,0.05);
    }
    .setting-island {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0px 2px 8px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL STATE ---
if 'cmd' not in st.session_state: st.session_state.cmd = ""
if 'history' not in st.session_state: st.session_state.history = []

def press(key):
    if key == "AC": st.session_state.cmd = ""
    elif key == "DEL": st.session_state.cmd = st.session_state.cmd[:-1]
    elif key == "EXE": st.session_state.execute = True
    else: st.session_state.cmd += str(key)

# --- 3. UI: BRANDING & NATURAL PREVIEW ---
st.markdown("<div class='brand-h1'>Verilogic-125</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-sub'>SRE WITH AI ASSIST</div>", unsafe_allow_html=True)

# Ghost Display: Real-time Math Rendering
if st.session_state.cmd:
    try:
        math_tex = sp.latex(sp.sympify(st.session_state.cmd.replace('×', '*').replace('÷', '/')))
        st.latex(math_tex)
    except:
        st.markdown(f"<p style='text-align:center; color:#8E8E93;'>{st.session_state.cmd}</p>", unsafe_allow_html=True)

# Entry Bar
entry = st.text_input('', value=st.session_state.cmd, placeholder='0', label_visibility="collapsed", key="v125_pro")
st.session_state.cmd = entry

# --- 4. THE APEX KEYPAD ---
keys = [
    ['sin', 'cos', 'tan', 'sqrt', '^'],
    ['log', 'ln', '(', ')', '÷'],
    ['7', '8', '9', 'pi', '×'],
    ['4', '5', '6', 'e', '-'],
    ['1', '2', '3', 'DEL', '+'],
    ['0', '.', 'x', 'AC', 'EXE']
]

for row in keys:
    cols = st.columns(5)
    for i, key in enumerate(row):
        if cols[i].button(key, key=f"k_{key}_{keys.index(row)}_{i}"):
            press(key)
            st.rerun()

# --- 5. ROBUST SETTINGS (Apple Inset Style) ---
with st.sidebar:
    st.markdown("<h2 style='margin-top:0;'>Settings</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='setting-island'>", unsafe_allow_html=True)
    st.markdown("**DIAGNOSTICS**")
    val = st.number_input("Unit Converter (mi/lb)", 1.0)
    st.caption(f"Metric: {val*1.609:.2f}km | {val*0.453:.2f}kg")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='setting-island'>", unsafe_allow_html=True)
    st.markdown("**CALCULATION TAPE**")
    for item in reversed(st.session_state.history[-5:]):
        st.caption(f"Result: {item}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='setting-island'>", unsafe_allow_html=True)
    st.markdown("**LEGAL_SHIELD**")
    st.caption("TX Penal Code § 33.02 Compliant")
    st.caption("Liability Waiver Active")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. APEX MATH & GRAPHING ---
if st.session_state.get('execute'):
    try:
        p = st.session_state.cmd.replace('×', '*').replace('÷', '/')
        if 'x' in p and '(' in p and '=' not in p:
            fig, ax = plt.subplots(figsize=(4, 2.5))
            x_r = np.linspace(-10, 10, 200); f = sp.lambdify(sp.Symbol('x'), sp.sympify(p), 'numpy')
            ax.plot(x_r, f(x_r), color='black', linewidth=2.5); ax.grid(True, color='#E5E5EA')
            st.pyplot(fig)
            res = "Graph Plotted"
        else:
            res = sp.solve(sp.sympify(p)) if '=' in p else sp.simplify(p).evalf(6)
        
        st.success(f"**RESULT:** {res}")
        st.session_state.history.append(str(res))
        st.session_state.execute = False
    except: st.error("LOGIC ERROR")
