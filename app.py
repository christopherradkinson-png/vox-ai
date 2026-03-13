import streamlit as st
import sympy as sp
import numpy as np
from pint import UnitRegistry
import re

# --- 1. ENGINE INITIALIZATION ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered')

# APPLE PRO UI: ULTRA-MODERN
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #1C1C1E; font-family: -apple-system, sans-serif; }
    .sre-card {
        background: #F2F2F7; border-radius: 20px; padding: 25px; 
        margin: 15px 0; border: 1px solid #D1D1D6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    .ans { color: #000000; font-size: 2.4rem; font-weight: 900; margin: 10px 0; letter-spacing: -1.5px; }
    .insight { color: #1C1C1E; font-size: 0.95rem; line-height: 1.5; border-top: 1px solid #CECED2; padding-top: 15px; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. THE SEMANTIC AI LAYER ---
def ai_semantic_cleaner(text):
    """Translates human slang/errors into machine-readable data."""
    t = text.lower().strip()
    # Slang & Context Mapping
    mappings = {
        r"(big ball of fire|the sun)": "sun",
        r"(moon|big white rock)": "moon",
        r"(dino|giant lizards)": "dinosaur",
        r"(how heavy|weight|mass)": "mass",
        r"(how big|size|length)": "size",
        r"(how far|distance)": "distance",
        r"(pi|pie|3.14)": "pi"
    }
    for pattern, replacement in mappings.items():
        t = re.sub(pattern, replacement, t)
    return t

def verilogic_engine(user_input):
    # Stage 1: AI Semantic Translation
    clean_query = ai_semantic_cleaner(user_input)
    
    # Stage 2: Scientific Knowledge Layer (The 'Librarian')
    # This acts as your local "Offline Library"
    knowledge_base = {
        "sun": {
            "mass": ("1.989 x 10^30 kg", "99.8% of our solar system's total mass."),
            "distance": ("149.6 Million km", "Equivalent to 1 Astronomical Unit (AU).")
        },
        "dinosaur": {
            "size": ("Patagotitan (37m)", "Titanosaurs are the largest land animals in history."),
            "extinct": ("66 Million Years ago", "Non-avian dinosaurs were wiped out by an asteroid.")
        },
        "pi": ("3.1415926535", "The ratio of a circle's circumference to its diameter.")
    }

    # Search for a match in the science logic
    for subject, metrics in knowledge_base.items():
        if subject in clean_query:
            for metric, (val, insight) in metrics.items():
                if metric in clean_query:
                    return {"a": val, "i": f"AI identified subject '{subject}'. {insight}", "t": "ADVANCED LIBRARIAN"}

    # Stage 3: Symbolic Math Core (The 'Mathematician')
    try:
        # Auto-correct common math data entry errors
        math_str = clean_query.replace('x', '*').replace('^', '**').replace(',', '')
        # Handle implicit multiplication like '2pi' -> '2*pi'
        math_str = re.sub(r'(\d)([a-z\(])', r'\1*\2', math_str)
        
        expr = sp.sympify(math_str)
        result = expr.evalf(10)
        return {"a": f"{result:g}", "i": "Math core automatically corrected input syntax for precision.", "t": "MATH CORE"}
    except:
        return {"a": "Awaiting Data", "i": "Librarian is standing by. Please provide a subject (Sun, Dinosaur) or an equation (5+5).", "t": "CONTEXT ENGINE"}

# --- 3. UI VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("main_dock", clear_on_submit=True):
    u_in = st.text_input("Command", placeholder="Ask the Librarian or Calculate...", label_visibility="collapsed")
    if st.form_submit_button("EXE"):
        if u_in:
            res = verilogic_engine(u_in)
            st.session_state.history.append({"q": u_in, **res})
            st.rerun()

for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="insight"><b>AI Insight:</b> {item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
