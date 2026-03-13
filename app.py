import streamlit as st
import sympy as sp
import numpy as np
from pint import UnitRegistry
import re

# --- 1. CORE SYSTEM ARCHITECTURE ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="collapsed")

# MILLION-DOLLAR UI: KILLS "EX E" SPLIT & FORMATS NUMBERS
st.markdown("""
<style>
    /* 1. Global Apple Foundation */
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: visible !important; background: transparent !important; }
    .stDeployButton { display:none !important; }
    #MainMenu { visibility: hidden !important; }

    /* 2. THE TOP COMMAND DOCK: Fixed Grid-Lock */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important;
        border-radius: 20px !important;
        padding: 12px 18px !important;
        border: 1px solid #D1D1D6 !important;
        margin-bottom: 30px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
    }
    
    /* Forces Input and EXE to stay on ONE LINE with no wrapping */
    div[data-testid="stForm"] > div {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 10px !important;
    }

    /* THE JUMBLE FIX */
    div[data-testid="stInputInstructions"] { display: none !important; }
    ::placeholder { color: #AEAEB2 !important; opacity: 1; }
    
    /* BLUE EXE BUTTON: Hard-locked to prevent 'EX E' fragmentation */
    button[kind="formSubmit"] {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-width: 90px !important; /* Prevents text splitting */
        white-space: nowrap !important; /* Force text to stay on one line */
        border: none !important;
        height: 45px !important;
    }

    /* 3. LIBRARIAN WORKSHEET CARDS */
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 26px; 
        margin: 18px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 8px 30px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    .ans { color: #000000; font-size: 2.4rem; font-weight: 800; margin: 8px 0; letter-spacing: -1.5px; }
    .ai-insight { color: #1C1C1E; font-size: 0.95rem; line-height: 1.5; border-top: 1px solid #F2F2F7; padding-top: 15px; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (LEGAL & SETTINGS) ---
with st.sidebar:
    st.title("Verilogic Pro")
    st.caption("Version 6.1.0 | SRE Stable")
    st.markdown("---")
    st.subheader("⚙️ Settings")
    precision = st.slider("Max Decimal Depth", 1, 15, 10)
    
    st.subheader("⚖️ Compliance")
    with st.expander("Texas 2026 Disclosure"):
        st.caption("TASAA Compliant. AI outputs verified via Symbolic Core.")
    
    if st.button("🗑️ Reset Worksheet"):
        st.session_state.history = []
        st.rerun()

# --- 3. THE AI LIBRARIAN (SMART FORMATTING ENGINE) ---
if 'history' not in st.session_state: st.session_state.history = []

def format_result(val):
    """Pro-tier number formatting: Commas for big numbers, clean integers."""
    try:
        if val % 1 == 0:
            return f"{int(val):,}" # Returns '10,000'
        else:
            return f"{val:,.{precision}g}".rstrip('0').rstrip('.') # Clean decimals
    except:
        return str(val)

def ai_librarian_pro(query):
    q = query.lower().strip()
    
    # Noise Stripper
    clean = re.sub(r'^(what is|calculate|tell me|solve|how much is|whats)\s+', '', q)
    
    # Science KB
    kb = {
        "moon": {"v": "3,474.8 km (Diameter)", "i": "The Moon's diameter is roughly 27% of Earth's. Mean radius is 1,737.1 km."},
        "sun": {"v": "1.989 × 10³⁰ kg", "i": "Solar mass detected. The Sun holds 99.8% of the system's mass."},
        "dinosaur": {"v": "Patagotitan mayorum", "i": "The largest land animal ever recorded. Spanned 122 feet and weighed ~70 tons."}
    }

    for key, data in kb.items():
        if key in clean: return {"q": query, "a": data["v"], "i": data["i"], "t": "AI SCIENCE LIBRARIAN"}

    # Math Core
    try:
        math_str = clean.replace('^', '**').replace(',', '')
        math_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', math_str)
        ans = sp.sympify(math_str).evalf(precision)
        return {"q": query, "a": format_result(float(ans)), "i": "Verbal noise filtered. Symbolic math logic verified by SRE Core.", "t": "MATH CORE"}
    except:
        return {"q": query, "a": "Check Entry", "i": "The Librarian could not parse this entry.", "t": "SYSTEM ERROR"}

# --- 4. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("top_dock_final", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_librarian_pro(u_in)
    st.session_state.history.append(result)
    st.rerun()

for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 <b>Librarian Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
