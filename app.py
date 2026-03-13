import streamlit as st
import sympy as sp
import plotly.graph_objects as go
import numpy as np
from pint import UnitRegistry

# --- 1. PRO-TIER UI (Liquid Glass + Variable Tray) ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro', layout='centered', initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #F2F2F7; color: #000000; font-family: -apple-system, sans-serif; }
    
    /* Variable Memory Tray */
    .variable-tray {
        background: #E5E5EA; border-radius: 12px; padding: 10px; margin-bottom: 20px;
        display: flex; gap: 10px; overflow-x: auto;
    }
    .var-token { background: #007AFF; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; }

    /* Interactive Worksheet Cards */
    .worksheet-card {
        background: #FFFFFF; border-radius: 18px; padding: 20px; 
        margin-bottom: 12px; border: 1px solid #E5E5EA;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    
    /* Input Bar - Always Focused */
    div[data-testid="stVerticalBlock"] > div:last-child {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: rgba(255,255,255,0.9); backdrop-filter: blur(20px);
        padding: 15px 20px 40px 20px; border-top: 1px solid #D1D1D6; z-index: 100;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. ADVANCED SRE ENGINE ---
if 'history' not in st.session_state: st.session_state.history = []
if 'vars' not in st.session_state: st.session_state.vars = {}

def calculate(raw):
    raw = raw.lower().strip()
    if not raw: return
    try:
        # 1. Variable Assignment (e.g., x=10)
        if '=' in raw and '==' not in raw:
            var_name, var_val = raw.split('=')
            st.session_state.vars[var_name.strip()] = var_val.strip()
            st.toast(f"Variable {var_name.strip()} saved", icon="💾")
            
        # 2. Conversion Engine
        elif ' to ' in raw:
            res = ureg(raw)
            st.session_state.history.append({"q": raw, "a": f"{res.magnitude:.4f} {res.units}", "t": "math"})
            
        # 3. Enhanced Math (with Variable Injection)
        else:
            processed = raw.replace('^', '**')
            for var, val in st.session_state.vars.items():
                processed = processed.replace(var, f"({val})")
            
            if 'x' in processed and '(' not in processed:
                st.session_state.history.append({"q": raw, "a": "Plotting...", "t": "graph"})
            else:
                expr = sp.sympify(processed)
                st.session_state.history.append({"q": raw, "a": str(expr.evalf(6)), "t": "math", "exact": str(expr)})
    except Exception as e:
        st.toast(f"Error: {str(e)}", icon="❌")

# --- 3. THE VIEWPORT ---
st.markdown("<h3 style='text-align:center; font-weight:700;'>Verilogic Pro</h3>", unsafe_allow_html=True)

# Display Variable Tray
if st.session_state.vars:
    st.markdown('<div class="variable-tray">', unsafe_allow_html=True)
    for v, val in st.session_state.vars.items():
        st.markdown(f'<span class="var-token">{v}: {val}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main Feed
for item in st.session_state.history:
    with st.container():
        st.markdown(f'<div class="worksheet-card"><small style="color:#8E8E93;">{item["q"]}</small>', unsafe_allow_html=True)
        if item['t'] == "math":
            st.markdown(f'<div style="font-size:1.6rem; font-weight:600;">= {item["a"]}</div>', unsafe_allow_html=True)
            with st.expander("Exact Value & Steps"):
                st.code(item.get('exact', 'N/A'))
        elif item['t'] == "graph":
            x = np.linspace(-10, 10, 400)
            f = sp.lambdify(sp.Symbol('x'), sp.sympify(item['q'].replace('^', '**')), "numpy")
            fig = go.Figure(data=go.Scatter(x=x, y=f(x), line=dict(color='#007AFF', width=3)))
            fig.update_layout(height=240, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='white', plot_bgcolor='#F9F9FB')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

# Footer Input
prompt = st.text_input("Enter Math, Variable, or Conversion", key="cmd_pro", placeholder="e.g., 50mph to kph", label_visibility="collapsed")
if prompt:
    calculate(prompt)
    st.rerun()
