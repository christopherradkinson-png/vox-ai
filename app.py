import streamlit as st
import sympy as sp
import plotly.graph_objects as go
import numpy as np
from pint import UnitRegistry

# --- 1. PRO APPLE COMMAND UI ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic SRE Pro', layout='centered', initial_sidebar_state="collapsed")

# iOS Design: Pure White, System Blue, High Contrast
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: hidden; height: 0px; }
    
    /* iOS NATIVE INPUT BAR */
    .stTextInput input {
        border: 2px solid #007AFF !important;
        border-radius: 14px !important;
        font-size: 1.6rem !important;
        padding: 18px !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* APPLE BLUE EXECUTE BUTTON */
    .stButton > button {
        width: 100% !important;
        padding: 15px !important;
        border-radius: 14px !important;
        background-color: #007AFF !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,122,255,0.3);
    }
    .stButton > button:active { transform: scale(0.96); opacity: 0.8; }

    /* WORKSHEET CARDS (DESMOS STYLE) */
    .worksheet-card {
        background: #F2F2F7;
        padding: 20px;
        border-radius: 18px;
        margin-bottom: 15px;
        border: 1px solid #D1D1D6;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE SRE ENGINE ---
if 'history' not in st.session_state: st.session_state.history = []

def process_input(raw):
    if not raw: return
    try:
        # A. UNIT ENGINE (e.g. "5ft + 2in")
        if any(u in raw.lower() for u in ['ft', 'm', 'kg', 'lb', 'in', 's', 'psi']):
            res = ureg(raw)
            st.session_state.history.append({"type": "unit", "q": raw, "a": f"{res.magnitude:.4f} {res.units}"})
        
        # B. GRAPHING ENGINE (e.g. "x^2 + 5")
        elif 'x' in raw.lower() and '=' not in raw:
            st.session_state.history.append({"type": "graph", "q": raw})
            
        # C. SYMBOLIC MATH ENGINE (e.g. "sin(pi/2)")
        else:
            clean = raw.replace('^', '**').replace('x', '*x')
            expr = sp.sympify(clean)
            st.session_state.history.append({
                "type": "math", 
                "q": raw, 
                "a": expr.evalf(5), 
                "step": f"Calculated as: {sp.latex(expr)}"
            })
    except Exception as e:
        st.toast(f"Error: {str(e)}", icon="⚠️")

# --- 3. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:800; letter-spacing:-1px;'>Verilogic SRE Pro</h2>", unsafe_allow_html=True)

# History Feed (The Worksheet)
for entry in st.session_state.history[::-1]: # Newest on top
    with st.container():
        if entry['type'] in ["math", "unit"]:
            st.markdown(f'''<div class="worksheet-card">
                <small style="color:#8E8E93; font-weight:500;">{entry['q']}</small><br>
                <b style="font-size:1.8rem; color:#000000;">= {entry['a']}</b>
            </div>''', unsafe_allow_html=True)
            if 'step' in entry:
                with st.expander("Show Your Work"):
                    st.latex(entry['step'])
                    
        elif entry['type'] == "graph":
            st.markdown(f"**Interactive Graph:** `{entry['q']}`")
            x_vals = np.linspace(-10, 10, 400)
            f_num = sp.lambdify(sp.Symbol('x'), sp.sympify(entry['q'].replace('^', '**')), "numpy")
            fig = go.Figure(data=go.Scatter(x=x_vals, y=f_num(x_vals), line=dict(color='#007AFF', width=4)))
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='white', plot_bgcolor='#F9F9FB')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 4. COMMAND ENTRY ---
# Tapping this triggers the native iOS keyboard immediately
user_query = st.text_input("Enter math, units, or equations:", placeholder="e.g. 5ft + 2in or sin(pi/2)", key="input_bar")

if st.button("EXECUTE"):
    process_input(user_query)
    st.rerun()

# --- 5. ROBUST SETTINGS SIDEBAR ---
with st.sidebar:
    st.header("⚙️ System Settings")
    st.divider()
    
    # Feature Toggles
    show_steps = st.toggle("Auto-Expand Steps", value=False)
    high_precision = st.toggle("High Precision (10 Decimals)", value=False)
    
    st.divider()
    
    # Unit Defaults
    st.subheader("Default Units")
    pref_system = st.selectbox("System", ["Metric (m, kg)", "Imperial (ft, lb)"])
    
    st.divider()
    
    # History Management
    if st.button("🗑️ CLEAR WORKSHEET", use_container_width=True):
        st.session_state.history = []
        st.rerun()
        
    st.caption("TASAA Compliance 2026")
    st.caption("Authorized SRE Node v5.1.0")
