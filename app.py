import streamlit as st
import sympy as sp
import numpy as np
from pint import UnitRegistry
import re
import time

# --- 1. CORE SYSTEM ARCHITECTURE ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="collapsed")

# APPLE PRO UI: THE "INVINCIBLE" GRID-LOCK
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: visible !important; background: transparent !important; }
    div[data-testid="stInputInstructions"] { display: none !important; }
    ::placeholder { color: #AEAEB2 !important; opacity: 1; }
    
    /* THE TOP COMMAND DOCK: Fixed Grid-Lock */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 12px 18px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 30px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stForm"] > div {
        display: grid !important; grid-template-columns: 3.5fr 1fr !important;
        align-items: center !important; gap: 12px !important;
    }
    button[kind="formSubmit"] {
        background-color: #007AFF !important; color: white !important;
        border-radius: 12px !important; font-weight: 700 !important;
        width: 100% !important; border: none !important;
        white-space: nowrap !important;
    }

    /* LIBRARIAN WORKSHEET CARDS */
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 26px; 
        margin: 18px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 8px 32px rgba(0,0,0,0.04);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    .ans { color: #000000; font-size: 2.3rem; font-weight: 800; margin: 8px 0; letter-spacing: -1.5px; }
    .ai-insight {
        color: #1C1C1E; font-size: 0.95rem; line-height: 1.6; 
        border-top: 1px solid #F2F2F7; padding-top: 15px; margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE ADVANCED LIBRARIAN CORE ---
if 'history' not in st.session_state: st.session_state.history = []

def ai_brain(query):
    # 1. SEMANTIC CHATTER STRIPPER
    q_clean = query.lower().strip()
    q_clean = re.sub(r'^(what is|calculate|tell me|solve|how much is|whats|how far is|distance to|size of|mass of|how many)\s+', '', q_clean)
    
    # 2. THE LIBRARIAN INTELLIGENCE (Pattern Inference)
    patterns = {
        r"pi\b": (np.pi, "", "Pi (π) is the ratio of a circle's circumference to its diameter, approximately 3.14159."),
        r"dinosaurs?.*exist": ("0 (Non-Avian)", "", "Non-avian dinosaurs went extinct ~66 million years ago. However, modern birds are technically avian dinosaurs."),
        r"sun.*mass": (1.989e30, "kg", "Solar mass represents 99.8% of the system's total mass."),
        r"sun.*distance": (1.496e8, "km", "This is 1 Astronomical Unit (AU). Light travels this in 8 minutes and 20 seconds."),
        r"moon.*distance": (384400, "km", "The lunar orbital distance is roughly 30 Earth diameters."),
        r"gravity": (9.806, "m/s²", "Standard Earth gravitational acceleration at sea level."),
        r"light": (299792458, "m/s", "The universal speed limit (c). Nothing with mass can reach this.")
    }

    for pattern, (val, unit, insight) in patterns.items():
        if re.search(pattern, q_clean):
            formatted_val = f"{val:g}" if isinstance(val, (int, float)) else val
            return {"q": query, "a": f"{formatted_val} {unit}", "i": insight, "t": "AI SCIENCE LIBRARIAN"}

    # 3. MATH ENGINE (Unbound Calculation)
    try:
        math_str = q_clean.replace('^', '**').replace(',', '')
        # Implicit Mult (2x -> 2*x)
        math_str = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', math_str)
        
        expr = sp.sympify(math_str)
        ans = expr.evalf(10)
        formatted = f"{int(ans):,}" if ans % 1 == 0 else f"{ans:g}"
        return {"q": query, "a": formatted, "i": "Symbolic Logic Verified. Verbal noise filtered for precision.", "t": "MATH CORE"}
    except:
        return {"q": query, "a": "Check Entry", "i": "The Librarian is searching. Ensure your syntax is clear (e.g. 5+5) or ask a science query.", "t": "SYSTEM ERROR"}

# --- 3. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("pro_dock_v31", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_brain(u_in)
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
