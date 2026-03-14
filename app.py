import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import pandas as pd
from astropy import constants as const
from astropy import units as u
from rapidfuzz import process, fuzz

# --- 1. SYSTEM ARCHITECTURE & UI LOCK ---
st.set_page_config(page_title="Verilogic Pro SRE", layout="centered")

if 'history' not in st.session_state: st.session_state.history = []

# THE "IRONCLAD" CSS: High-contrast, Centered, Mobile-Ready
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    
    .v-header { text-align: center; color: #1C1C1E; font-weight: 900; font-size: 2.2rem; margin-top: -50px; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 700; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 30px; }

    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 15px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 25px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }

    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 24px; 
        margin: 15px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #1C1C1E; font-size: 2.1rem; font-weight: 800; margin: 5px 0; letter-spacing: -1px; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE ANTICIPATORY ANALYTICAL ENGINE ---
def smart_engine(query):
    # CLEANING: Handle common typos and spacing
    q_raw = query.lower().strip()
    
    # PASS 1: MATH HEURISTIC (The "2x+9x" Fix)
    # Detects math characters or variables even without an "=" sign
    if any(c.isdigit() or c in "xyz+-*/^()" for c in q_raw):
        try:
            # FIX: Convert implicit multiplication (e.g., 2x -> 2*x)
            math_ready = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', q_raw)
            x, y, z = sp.symbols('x y z')
            
            # If it's an equation
            if "=" in math_ready:
                lhs, rhs = math_ready.split("=")
                eq = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
                sol = sp.solve(eq)
                return {"q": query, "a": f"x = {sol}", "i": "Equation solved via symbolic isolation.", "t": "ALGEBRA", "lx": sp.latex(eq)}
            # If it's just an expression (e.g., 2x+9x)
            else:
                simplified = sp.simplify(math_ready)
                return {"q": query, "a": str(simplified), "i": "Expression simplified via symbolic reduction.", "t": "MATH CORE", "lx": sp.latex(simplified)}
        except:
            pass # Math failed? Move to Science/Wiki

    # PASS 2: SCIENCE FUZZY MATCH (Handle "Sun Sise" -> "Sun Size")
    science_map = {
        "size of the sun": const.R_sun.to(u.km),
        "mass of the sun": const.M_sun,
        "speed of light": const.c,
        "gravity": const.G,
        "distance to moon": 384400
    }
    
    best_match, score, _ = process.extractOne(q_raw, science_map.keys(), scorer=fuzz.WRatio)
    
    if score > 80:
        data = science_map[best_match]
        val = data.value if hasattr(data, 'value') else data
        return {"q": query, "a": f"{val:,.2f}", "i": f"Data retrieved for '{best_match}'. Verified via NASA/Astropy.", "t": "ASTRO CORE", "lx": sp.latex(val)}

    # PASS 3: GLOBAL LIBRARIAN (Wikipedia)
    try:
        # Wikipedia summary with auto-suggest for typos
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        return {"q": query, "a": "Knowledge Retrieved", "i": summary, "t": "LIBRARIAN", "lx": None}
    except:
        return {"q": query, "a": "Refining...", "i": "Query unrecognized. Try '2x+9x' or 'Size of the Sun'.", "t": "SYSTEM", "lx": None}

# --- 3. THE VIEWPORT ---
st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ANTICIPATORY RESEARCH ENGINE v13.5</div>', unsafe_allow_html=True)

with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Enter math, equations, or facts...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    # Inserts newest result at the top
    st.session_state.history.insert(0, smart_engine(u_in))

# Render Session History
for item in st.session_state.history:
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:0.9rem; color:#3A3A3C; line-height:1.4;">💡 <b>Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item.get('lx'):
        st.latex(item['lx'])

with st.sidebar:
    st.title("SRE Tools")
    if st.button("🗑️ Clear & Reset Workspace"):
        st.session_state.history = []
        st.rerun()
