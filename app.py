import streamlit as st
import sympy as sp
import datetime, requests
import matplotlib.pyplot as plt
import numpy as np

# --- 1. APPLE PRO DESIGN SYSTEM ---
st.set_page_config(page_title='Verilogic-125', layout='wide', initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp {background-color: #FFFFFF; color: #000000;}
    * {font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;}
    
    /* MOBILE GRID LOCK: Keeps 5 columns horizontal */
    [data-testid="column"] { flex: 1 1 0% !important; min-width: 0px !important; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; }

    /* Apple-Style Data Entry Bar */
    .stTextInput input {
        border: none !important; border-bottom: 2px solid #000 !important;
        font-size: 2.2rem !important; text-align: center !important; font-weight: 800 !important;
        background-color: transparent !important; color: #000 !important; padding: 10px 0px !important;
        border-radius: 0px !important;
    }
    
    /* Pro Tactile Buttons */
    div.stButton > button {
        background-color: #FFFFFF !important; color: #000 !important;
        border: 2px solid #000 !important; border-radius: 12px !important;
        height: 55px !important; font-weight: 800 !important; font-size: 1rem !important;
    }
    div.stButton > button:active { background-color: #000 !important; color: #FFF !important; transform: scale(0.96); }
    
    /* Operator Differentiation (Dark Keys) */
    div[data-testid="column"]:nth-child(5) button { background-color: #000 !important; color: #FFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL STATE ---
if 'cmd' not in st.session_state: st.session_state.cmd = ""
if 'history' not in st.session_state: st.session_state.history = []

def press(key):
    if key == "AC": st.session_state.cmd = ""
    elif key == "DEL": st.session_state.cmd = st.session_state.cmd[:-1]
    elif key == "=": st.session_state.execute = True
    else: st.session_state.cmd += str(key)

# --- 3. BRANDING & WORK PREVIEW ---
st.markdown("<h1 style='text-align: center; margin-bottom:0;'>Verilogic-125</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size:0.8rem; letter-spacing:3px; opacity:0.7;'>VOX AI INTEGRATED SYSTEM</h3>", unsafe_allow_html=True)

# Live "Show Your Work" LaTeX Rendering
if st.session_state.cmd:
    try:
        math_tex = sp.latex(sp.sympify(st.session_state.cmd.replace('×', '*').replace('÷', '/')))
        st.latex(math_tex)
    except: pass

# --- 4. MAIN ENTRY BAR ---
entry = st.text_input('', value=st.session_state.cmd, placeholder='ENTER SEQUENCE', label_visibility="collapsed")
st.session_state.cmd = entry

# --- 5. SCIENTIFIC KEYPAD (5-Column Matrix) ---
keys = [
    ['sin', 'cos', 'tan', 'sqrt', '÷'],
    ['(', ')', '^', 'log', '×'],
    ['7', '8', '9', 'pi', '-'],
    ['4', '5', '6', 'e', '+'],
    ['1', '2', '3', 'DEL', 'AC'],
    ['0', '.', 'x', 'y', '=']
]

for r_idx, row in enumerate(keys):
    cols = st.columns(5)
    for c_idx, key in enumerate(row):
        if cols[c_idx].button(key, use_container_width=True, key=f"btn_{r_idx}_{c_idx}"):
            press(key)
            st.rerun()

# --- 6. ROBUST SIDEBAR (History, Units, Currency, Legal) ---
with st.sidebar:
    st.title("SYSTEM_CORE")
    t1, t2, t3, t4 = st.tabs(["HISTORY", "UNITS", "CURRENCY", "LEGAL"])
    
    with t1: # Calculation Tape
        for item in reversed(st.session_state.history):
            if st.button(f"{item['v']}", key=f"h_{item['t']}", use_container_width=True):
                st.session_state.cmd += str(item['v'])
                st.rerun()
    
    with t2: # Multi-Category Unit Converter
        st.subheader("CONVERSION_NODE")
        cat = st.selectbox("Category", ["Weight", "Volume", "Length"])
        val = st.number_input("Value", value=1.0)
        
        if cat == "Weight":
            st.write(f"{val} lb = {val * 0.45359:.3f} kg")
        elif cat == "Volume":
            st.write(f"{val} gal = {val * 3.78541:.3f} L")
        elif cat == "Length":
            st.write(f"{val} mi = {val * 1.60934:.3f} km")

    with t3: # Real-time Currency
        base = st.selectbox("Base", ["USD", "EUR", "GBP"])
        target = st.selectbox("Target", ["EUR", "USD", "JPY"])
        if st.button("Get Live Rate"):
            try:
                r = requests.get(f"https://api.exchangerate-api.com{base}").json()
                st.info(f"1 {base} = {r['rates'][target]} {target}")
            except: st.error("Offline")

    with t4: # Original Legal Protocols
        st.markdown("**LEGAL_PROTOCOL_V2**")
        st.write("LIABILITY WAIVER: EDUCATIONAL USE ONLY.")
        st.write("TX Penal Code § 33.02 Compliant.")
        st.write("TX Bus. & Com. Code § 521 Compliant.")

# --- 7. APEX CALC & GRAPH ENGINE ---
if st.session_state.get('execute') or "=" in st.session_state.cmd:
    try:
        clean = st.session_state.cmd.replace('×', '*').replace('÷', '/').replace('=', '')
        if 'x' in clean and not '=' in st.session_state.cmd:
            # High-Performance Graphing
            fig, ax = plt.subplots(figsize=(6, 3))
            x = np.linspace(-10, 10, 400)
            f = sp.lambdify(sp.Symbol('x'), sp.sympify(clean), 'numpy')
            ax.plot(x, f(x), color='black', linewidth=2)
            ax.grid(True, color='#E5E5EA'); ax.set_facecolor('#FFFFFF')
            st.pyplot(fig)
            res = "Plotted"
        else:
            res = sp.solve(sp.sympify(clean)) if 'x' in clean else sp.simplify(clean).evalf(6)
        
        st.success(f"RESULT: {res}")
        st.session_state.history.append({"v": res, "t": datetime.datetime.now().timestamp()})
        st.session_state.execute = False
    except: st.error("LOGIC ERROR")
