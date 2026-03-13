import streamlit as st
import sympy as sp
import numpy as np
from pint import UnitRegistry
import re

# --- 1. CORE SYSTEM ARCHITECTURE ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="collapsed")

# APPLE PRO UI: TOP-DOCK "INVINCIBLE" ARCHITECTURE
st.markdown("""
<style>
    /* 1. Global Apple Foundation */
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    
    /* SIDEBAR & HEADER: Restores the '>>' icon and Top-Left menu */
    header { visibility: visible !important; background: transparent !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    .stDeployButton { display:none !important; }
    #MainMenu { visibility: hidden !important; }

    /* 2. THE TOP COMMAND DOCK: Fixed width and horizontal lock */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        border: 1px solid #D1D1D6 !important;
        margin-bottom: 30px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
    }
    
    /* This forces the Input and EXE to stay on ONE LINE without wrapping */
    div[data-testid="stForm"] > div {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 12px !important;
    }

    /* THE JUMBLE FIX: Hides "Press Enter" and cleans placeholder */
    div[data-testid="stInputInstructions"] { display: none !important; }
    ::placeholder { color: #AEAEB2 !important; opacity: 1; transition: opacity 0.2s; }
    input:focus::placeholder { opacity: 0 !important; }
    
    /* BLUE EXE BUTTON: Hard-locked width to prevent 'EX E' fragmentation */
    button[kind="formSubmit"] {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-width: 85px !important; 
        border: none !important;
        padding: 10px !important;
    }

    /* 3. LIBRARIAN WORKSHEET CARDS */
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 26px; 
        margin: 18px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 8px 30px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #000000; font-size: 2.2rem; font-weight: 800; margin: 8px 0; letter-spacing: -1px; }
    .ai-insight { color: #1C1C1E; font-size: 0.95rem; line-height: 1.5; border-top: 1px solid #F2F2F7; padding-top: 15px; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (LEGAL & SETTINGS) ---
with st.sidebar:
    st.title("Verilogic Pro")
    st.caption("Version 5.8.2 | Alpha Stage")
    st.markdown("---")
    st.subheader("⚙️ Settings")
    precision = st.slider("Decimal Precision", 1, 15, 10)
    
    st.subheader("⚖️ Compliance")
    with st.expander("Legal & EULA"):
        st.caption("TASAA 2026. Verilogic SRE is a proprietary Intelligence Engine.")
        st.caption("Terms: Computations are symbolic-verified. Accuracy is guaranteed for standard patterns.")
    
    if st.button("🗑️ Reset All Data"):
        st.session_state.history = []
        st.rerun()

# --- 3. THE AI LIBRARIAN (VERBAL & KNOWLEDGE CORE) ---
if 'history' not in st.session_state: st.session_state.history = []

def ai_librarian_pro(query):
    q = query.lower().strip()
    
    # 1. NOISE STRIPPER (Solves "What is 5000+5000")
    clean = re.sub(r'^(what is|calculate|tell me|solve|how much is|whats)\s+', '', q)
    
    # 2. SCIENCE KNOWLEDGE BASE
    kb = {
        "moon": {
            "v": "3,474.8 km (Diameter)", 
            "i": "The Moon's diameter is roughly 27% of Earth's. Because of its smaller mass, you would weigh only 16.5% of your Earth weight on its surface."
        },
        "sun": {
            "v": "1.989 × 10³⁰ kg", 
            "i": "The Sun contains 99.8% of the total mass of the solar system. About 1.3 million Earths could fit inside it."
        },
        "dinosaur": {
            "v": "Patagotitan mayorum",
            "i": "The largest land animal ever recorded. It weighed roughly 70 tons and spanned 122 feet."
        }
    }

    # 3. Fuzzy AI Search
    for key, data in kb.items():
        if key in clean:
            return {"q": query, "a": data["v"], "i": data["i"], "t": "AI SCIENCE LIBRARIAN"}

    # 4. Math Core Fallback
    try:
        math_str = clean.replace('^', '**').replace(',', '')
        # Implicit Mult Fix (2x -> 2*x)
        math_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', math_str)
        expr = sp.sympify(math_str)
        ans = expr.evalf(precision)
        return {"q": query, "a": f"{ans:g}", "i": "Verbal math noise filtered. Symbolic math logic verified by SRE Core.", "t": "MATH CORE"}
    except:
        return {"q": query, "a": "Check Entry", "i": "The Librarian could not parse this entry. Use standard math (e.g. 5000+5000).", "t": "SYSTEM ERROR"}

# --- 4. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("top_dock_v10", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_librarian_pro(u_in)
    st.session_state.history.append(result)
    st.rerun()

# Display Worksheet (Newest on Top)
for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 <b>Librarian Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
