import sys, warnings, datetime, re
import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings('ignore')
st.set_page_config(page_title='Verilogic-125', layout='wide')

# --- Apple High-Contrast Contrast Patch ---
st.markdown("""
<style>
    .stApp {background-color: #FFFFFF; color: #000000;}
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Arial, sans-serif !important;
    }
    h1 {
        text-align: center; color: #000000 !important; font-weight: 800; 
        letter-spacing: -0.8px; font-size: 2.2rem !important; margin-bottom: 2px;
    }
    /* Sub-header: Darkened to Deep Graphite */
    h3 {
        text-align: center; color: #1C1C1E !important; font-weight: 700; 
        font-size: 0.9rem !important; text-transform: uppercase; letter-spacing: 1px;
        opacity: 1 !important;
    }
    .stTextInput input {
        background-color: #F2F2F7 !important; color: #000000 !important;
        border: 1px solid #8E8E93 !important; border-radius: 10px !important;
        text-align: center; font-size: 1.1rem !important; padding: 12px !important;
    }
    /* Placeholder: Darkened for Visibility */
    ::placeholder {
        color: #1C1C1E !important; opacity: 0.9 !important; font-weight: 500;
    }
    div.stButton {
        display: flex; justify-content: center; align-items: center; width: 100%;
    }
    .stButton>button {
        width: 90% !important; max-width: 380px; background-color: #000000 !important; 
        color: #FFFFFF !important; border: none !important; border-radius: 12px !important; 
        font-weight: 700; font-size: 1.1rem !important; height: 52px; transition: 0.3s;
    }
    [data-testid="stSidebar"] {
        background-color: #F2F2F7 !important; border-right: 1px solid #C6C6C8 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1>Verilogic-125</h1>', unsafe_allow_html=True)
st.markdown('<h3>VOX AI INTEGRATED SYSTEM</h3>', unsafe_allow_html=True)

query = st.text_input('', placeholder='ENTER SEQUENCE (e.g. 2+2)', label_visibility='collapsed')
calc = st.button('Calculate')

if calc and query:
    with st.status("Analyzing...", expanded=True) as status:
        clean = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", query.replace(" ", "").lower())
        w_map = {"plus":"+", "minus":"-", "times":"*", "divided":"/", "dividedby":"/"}
        for w, s in w_map.items(): clean = clean.replace(w, s)
        if "=" in clean: clean = clean.replace("=", "-(")+")"
        try:
            expr = sp.sympify(clean)
            status.write(f"NODE_01: Identified Logic: {expr}")
            res = sp.solve(expr) if any(v in clean for v in 'xyz') else sp.simplify(expr)
            status.update(label="Analysis Complete", state="complete")
            if "x" in clean:
                fig, ax = plt.subplots(figsize=(6,3))
                x_v = np.linspace(-10, 10, 100)
                f_l = sp.lambdify(sp.symbols("x"), expr, "numpy")
                ax.plot(x_v, f_l(x_v), color="#000000", linewidth=2.5)
                ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
                ax.grid(True, color='#F2F2F7')
                st.pyplot(fig)
            st.success(f"Result: {res}")
        except Exception as e:
            status.update(label="Logic Error", state="error")
            st.error("Sequence unreadable. Check syntax.")

st.sidebar.title('System')
st.sidebar.caption(f"Secure Node: {datetime.datetime.now().strftime('%H:%M')} CST")
with st.sidebar.expander("Legal & Privacy"):
    st.write("TX Bus. & Com. Code Sec 521 Compliant.")
st.sidebar.code('OS: SRE_PROD\nVER: 1.34.5-STABLE')

if st.sidebar.button('Hard Re-Sync'):
    st.cache_data.clear(); st.rerun()
