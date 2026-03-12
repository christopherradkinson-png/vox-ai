import sys, warnings, datetime, re
import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings('ignore')
st.set_page_config(page_title='Verilogic-125', layout='wide')

# --- Triple-Layer Centering & High-Contrast CSS ---
st.markdown("""
<style>
    .stApp {background-color: #FFFFFF; color: #000000;}
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
    }
    h1 {text-align: center; color: #000000 !important; font-weight: 800; font-size: 2.2rem !important;}
    h3 {text-align: center; color: #000000 !important; font-weight: 800; font-size: 0.95rem !important; text-transform: uppercase;}
    
    /* UNIVERSAL CENTERING PATCH */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        display: flex !important;
        justify-content: center !important;
    }
    div.stButton {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    .stButton>button {
        width: 90% !important; 
        max-width: 400px !important; 
        height: 60px !important;
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        border: 2px solid #000000 !important; 
        border-radius: 12px !important;
        font-weight: 800; font-size: 1.1rem !important;
    }
    
    .stTextInput input {
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #000000 !important; border-radius: 10px !important;
        text-align: center; font-size: 1.2rem !important;
    }
    ::placeholder {color: #000000 !important; opacity: 1 !important; font-weight: 700;}
    [data-testid="stSidebar"] {background-color: #FFFFFF !important; border-right: 2px solid #000000 !important;}
    [data-testid="stSidebar"] * {color: #000000 !important; font-weight: 700 !important; text-decoration: none !important;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1>Verilogic-125</h1>', unsafe_allow_html=True)
st.markdown('<h3>VOX AI INTEGRATED SYSTEM</h3>', unsafe_allow_html=True)

query = st.text_input('', placeholder='ENTER SEQUENCE (e.g. 2+2)', label_visibility='collapsed')
calc = st.button('CALCULATE SEQUENCE')

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
                ax.plot(x_v, f_l(x_v), color="#000000", linewidth=3)
                ax.set_facecolor("#FFFFFF"); fig.patch.set_facecolor("#FFFFFF")
                ax.grid(True, color='#E5E5EA')
                st.pyplot(fig)
            st.success(f"RESULT_OUTPUT: {res}")
        except Exception as e:
            status.update(label="Logic Error", state="error")
            st.error(f"Sequence unreadable: {e}")

# --- Sidebar & Legal Shield ---
st.sidebar.title('SYSTEM_CORE')
st.sidebar.caption(f"AUTH_NODE: {datetime.datetime.now().strftime('%H:%M')} CST")

with st.sidebar.expander("LEGAL_PROTOCOL_V2", expanded=True):
    st.write("**LIABILITY WAIVER:** EDUCATIONAL PURPOSES ONLY.")
    st.write("Creator assumes **NO RESPONSIBILITY** for errors or damages.")
    st.write("**USE AT YOUR OWN RISK.**")
    st.markdown("---")
    st.write("TX Bus. & Com. Code Sec 521 & Penal Code 33.02 Compliant.")

st.sidebar.markdown("---")
st.sidebar.subheader("VERSION_INTEL")
st.sidebar.code('OS: SRE_PROD\nVER: 1.35.3-ULTIMATE')

# --- Hard Reset Logic ---
if st.sidebar.button('HARD RE-SYNC'):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.query_params.clear() # Forces a URL refresh
    st.rerun()
