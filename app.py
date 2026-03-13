import streamlit as st
import sympy as sp
import plotly.graph_objects as go
import numpy as np
from pint import UnitRegistry

# --- 1. PRO UI ARCHITECTURE (IPHONE LOCKED) ---
ureg = UnitRegistry()
# FORCE SIDEBAR OPEN so settings aren't hidden
st.set_page_config(
    page_title='Verilogic-125 SRE', 
    layout='centered', 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: hidden; height: 0px; }
    
    /* FIX: Prevents Execute Button from cutting off the Input Bar */
    .main-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    /* iOS PRO INPUT BAR */
    .stTextInput input {
        border: 2px solid #E5E5EA !important;
        border-radius: 12px !important;
        font-size: 1.4rem !important;
        padding: 15px !important;
        background-color: #F9F9F9 !important;
    }

    /* APPLE BLUE EXECUTE BUTTON */
    div.stButton > button {
        width: 100% !important;
        padding: 16px !important;
        border-radius: 12px !important;
        background-color: #007AFF !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. AI ASSIST ENGINE (FUZZY LOGIC) ---
if 'history' not in st.session_state: st.session_state.history = []

def ai_math_cleaner(text):
    """Simple AI Assist to fix common misspelling in math strings"""
    corrections = {
        "to": "2", "plus": "+", "minus": "-", "times": "*", 
        "divided by": "/", "for": "4", "ate": "8"
    }
    lowered = text.lower()
    for word, replacement in corrections.items():
        lowered = lowered.replace(word, replacement)
    return lowered

def execute_engine(raw_query):
    if not raw_query: return
    
    # AI Assist Step
    clean_query = ai_math_cleaner(raw_query)
    
    try:
        # A. Units
        if any(u in clean_query for u in ['ft', 'm', 'kg', 'lb', 'in', 's']):
            res = ureg(clean_query)
            st.session_state.history.append({"q": raw_query, "a": f"{res.magnitude:.4f} {res.units}", "steps": ["Unit Conversion Logic Applied"]})
        
        # B. Symbolic Math
        else:
            final_math = clean_query.replace('^', '**')
            expr = sp.sympify(final_math)
            steps = [f"AI Interpreted: {clean_query}", f"Latex: {sp.latex(expr)}"]
            st.session_state.history.append({"q": raw_query, "a": expr.evalf(5), "steps": steps})
            
    except Exception as e:
        st.error(f"Engine Error: {e}")

# --- 3. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:800;'>Verilogic-125 SRE <span style='color:#007AFF;'>with AI Assist</span></h2>", unsafe_allow_html=True)

# THE INPUT ZONE
query = st.text_input("Data Entry Bar", placeholder="Enter math (e.g., 'to plus two')", key="input_widget")

if st.button("EXECUTE"):
    execute_engine(query)
    # st.rerun() is often better for mobile state updates
    st.rerun()

st.divider()

# THE RESULTS ZONE (Newest on top)
for entry in reversed(st.session_state.history):
    with st.container():
        st.markdown(f"**Query:** `{entry['q']}`")
        st.markdown(f"### Result: {entry['a']}")
        with st.expander("Show Your Work"):
            for s in entry['steps']:
                st.write(f"• {s}")
        st.divider()

# --- 4. ROBUST SETTINGS (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Verilogic Pro v5.2.1")
    st.divider()
    
    st.subheader("System Controls")
    if st.button("🗑️ CLEAR ALL DATA"):
        st.session_state.history = []
        st.rerun()
    
    st.divider()
    st.caption("TASAA 2026 Compliance Node")
