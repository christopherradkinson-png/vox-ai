import streamlit as st
import sympy as sp
import datetime, requests
import matplotlib.pyplot as plt
import numpy as np

# --- 1. APPLE PRO PRECISION INTERFACE ---
st.set_page_config(page_title='Verilogic-125 SRE', layout='centered')

st.markdown("""
<style>
    /* Pure Apple Monochrome Theme */
    .stApp {background-color: #FFFFFF; color: #000000;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    #MainMenu {visibility: visible; color: #000 !important;}

    /* Force San Francisco System Font */
    * {font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;}

    /* Main Branding */
    .brand-h1 {text-align: center; font-weight: 800; font-size: 2.2rem; margin-bottom: 0px; color: #000;}
    .brand-sub {text-align: center; font-weight: 700; font-size: 0.8rem; letter-spacing: 2px; color: #8E8E93; margin-top: 0px;}

    /* Input Bar: iPhone Style */
    .stTextInput input {
        border: none !important; border-bottom: 2px solid #000 !important;
        font-size: 2.5rem !important; text-align: right !important; font-weight: 700 !important;
        background-color: transparent !important; color: #000 !important;
        padding-bottom: 10px !important;
    }

    /* THE KEYPAD FIX: CSS GRID FOR PERFECT SQUARES */
    .keypad-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 8px;
        margin-top: 20px;
        max-width: 450px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Individual Key Styling */
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important; /* Forces Square Shape */
        border-radius: 12px !important;
        border: none !important;
        background-color: #F2F2F7 !important;
        color: #000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: 0.1s;
    }
    .stButton > button:active { background-color: #000 !important; color: #FFF !important; }

    /* Scientific Operators (Darker) */
    div[data-testid="column"]:nth-child(n+4) button {
        background-color: #E5E5EA !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL STATE & LOGIC ---
if 'cmd' not in st.session_state: st.session_state.cmd = ""
if 'history' not in st.session_state: st.session_state.history = []

def press(key):
    if key == "AC": st.session_state.cmd = ""
    elif key == "DEL": st.session_state.cmd = st.session_state.cmd[:-1]
    elif key == "=": st.session_state.execute = True
    else: st.session_state.cmd += str(key)

# --- 3. BRANDING ---
st.markdown("<h1 class='brand-h1'>Verilogic-125 SRE</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-sub'>WITH AI ASSIST</p>", unsafe_allow_html=True)

# Live LaTeX Result rendering (Show Your Work)
if st.session_state.cmd:
    try:
        math_tex = sp.latex(sp.sympify(st.session_state.cmd.replace('×', '*').replace('÷', '/')))
        st.latex(math_tex)
    except: pass

# --- 4. INPUT BAR ---
entry = st.text_input('', value=st.session_state.cmd, placeholder='0', label_visibility="collapsed")
st.session_state.cmd = entry

# --- 5. THE SQUARE KEYPAD GRID ---
# Standard Scientific Layout: Numbers center, symbols wrapped
keys = [
    ['sin', 'cos', 'tan', 'sqrt', '÷'],
    ['(', ')', '^', 'log', '×'],
    ['7', '8', '9', '-', 'AC'],
    ['4', '5', '6', '+', 'DEL'],
    ['1', '2', '3', 'x', 'y'],
    ['0', '.', 'pi', 'e', '=']
]

for row in keys:
    cols = st.columns(5)
    for i, key in enumerate(row):
        if cols[i].button(key, use_container_width=True):
            press(key)
            st.rerun()

# --- 6. RESTORED SIDEBAR (History, Settings, Legal) ---
with st.sidebar:
    st.markdown("### **SYSTEM_CORE**")
    t1, t2, t3 = st.tabs(["HISTORY", "UNITS", "LEGAL"])
    
    with t1:
        for idx, item in enumerate(reversed(st.session_state.history)):
            if st.button(f"{item['v']}", key=f"h_{idx}", use_container_width=True):
                st.session_state.cmd += str(item['v']); st.rerun()
    
    with t2:
        st.write("**Quick Converters**")
        cat = st.selectbox("Category", ["Length (mi-km)", "Weight (lb-kg)"])
        val = st.number_input("Input", value=1.0)
        if "Length" in cat: st.info(f"{val*1.609:.2f} km")
        else: st.info(f"{val*0.453:.2f} kg")

    with t3:
        st.caption("TX Penal Code § 33.02 COMPLIANT")
        st.caption("LIABILITY WAIVER: EDUCATIONAL USE ONLY")

# --- 7. APEX ENGINE (Graphing & Math) ---
if st.session_state.get('execute') or "=" in st.session_state.cmd:
    try:
        clean = st.session_state.cmd.replace('×', '*').replace('÷', '/').replace('=', '')
        if 'x' in clean and not '=' in st.session_state.cmd:
            # Automatic Graphing for functions of x
            fig, ax = plt.subplots(figsize=(5, 3))
            x_range = np.linspace(-10, 10, 100)
            f_lamb = sp.lambdify(sp.Symbol('x'), sp.sympify(clean), 'numpy')
            ax.plot(x_range, f_lamb(x_range), color='black', linewidth=2)
            ax.grid(True, color='#E5E5EA'); ax.set_facecolor('#FFFFFF')
            st.pyplot(fig)
            res = "Graph Plotted"
        else:
            # Symbolic Solver
            res = sp.solve(sp.sympify(clean)) if 'x' in clean else sp.simplify(clean).evalf(6)
        
        st.success(f"**RESULT:** {res}")
        st.session_state.history.append({"v": res, "t": datetime.datetime.now()})
        st.session_state.execute = False
    except: st.error("LOGIC ERROR: Check Sequence")
