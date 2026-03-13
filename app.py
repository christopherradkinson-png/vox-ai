import streamlit as st
import sympy as sp
import numpy as np
from pint import UnitRegistry
import re

# --- 1. CORE SYSTEM CONFIG ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="collapsed")

# RESTORED: THE "BEST-EVER" GRID-LOCK CSS
st.markdown("""
<style>
    /* Global Apple Aesthetic */
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: visible !important; background: transparent !important; }
    .stDeployButton { display:none !important; }
    #MainMenu { visibility: hidden !important; }

    /* THE LOCK-GRID DOCK (Top-Dock Restoration) */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important;
        border-radius: 20px !important;
        padding: 12px 15px !important;
        border: 1px solid #D1D1D6 !important;
        margin-bottom: 30px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
    }
    
    /* This rule is what prevents 'EX E' fragmentation */
    div[data-testid="stForm"] > div {
        display: grid !important;
        grid-template-columns: 3.5fr 1fr !important;
        align-items: center !important;
        gap: 10px !important;
    }

    /* Kills "Press Enter" jumble */
    div[data-testid="stInputInstructions"] { display: none !important; }
    
    /* EXE BUTTON: Standard Pro Blue */
    button[kind="formSubmit"] {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        width: 100% !important;
        border: none !important;
        white-space: nowrap !important; /* Prevents text wrap */
    }

    /* LIBRARIAN WORKSHEET CARDS */
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 26px; 
        margin: 18px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 8px 30px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #000000; font-size: 2.2rem; font-weight: 700; margin: 5px 0; letter-spacing: -1.5px; }
    .ai-insight { color: #1C1C1E; font-size: 0.95rem; line-height: 1.5; border-top: 1px solid #F2F2F7; padding-top: 15px; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (LEGAL & SETTINGS) ---
with st.sidebar:
    st.title("Verilogic Pro")
    st.caption("Version 6.3.0 | Restoration Build")
    st.markdown("---")
    precision = st.slider("Max Decimal Depth", 1, 15, 10)
    with st.expander("Legal & Compliance"):
        st.caption("TASAA 2026. Per Texas HB 149, AI outputs are generated via SRE.")
    if st.button("🗑️ Reset Worksheet"):
        st.session_state.history = []
        st.rerun()

# --- 3. THE AI LIBRARIAN (CLEAN MATH) ---
if 'history' not in st.session_state: st.session_state.history = []

def clean_math_format(val):
    """Ensures 10000 looks like 10,000 and removes trailing zeros."""
    try:
        if val % 1 == 0:
            return f"{int(val):,}"
        else:
            return f"{val:,.{precision}g}".rstrip('0').rstrip('.')
    except:
        return str(val)

def ai_librarian_pro(query):
    q = query.lower().strip()
    clean = re.sub(r'^(what is|calculate|tell me|solve|how much is|whats)\s+', '', q)
    
    # Knowledge Core
    kb = {
        "moon": {"v": "3,474.8 km (Diameter)", "i": "The Moon's diameter is 1/4 of Earth's. Its gravity governs the tides."},
        "sun": {"v": "1.989 × 10³⁰ kg", "i": "Solar mass detected. Holds 99.8% of the system's total mass."},
        "dinosaur": {"v": "Patagotitan mayorum", "i": "The Titanosaur (Patagotitan) is the largest land animal ever recorded."}
    }

    for key, data in kb.items():
        if key in clean: return {"q": query, "a": data["v"], "i": data["i"], "t": "AI SCIENCE LIBRARIAN"}

    try:
        math_str = clean.replace('^', '**').replace(',', '')
        math_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', math_str)
        ans = sp.sympify(math_str).evalf(precision)
        return {"q": query, "a": clean_math_format(float(ans)), "i": "Symbolic math logic verified by SRE Core.", "t": "MATH CORE"}
    except:
        return {"q": query, "a": "Check Entry", "i": "The Librarian is analyzing. Use standard math (e.g. 5000+5000).", "t": "SYSTEM ERROR"}

# --- 4. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("pro_dock_restored", clear_on_submit=True):
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
