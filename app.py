import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
from astropy import constants as const
from astropy import units as u
from rapidfuzz import process, fuzz

# --- 1. SYSTEM UI: TITAN ARCHITECTURE ---
st.set_page_config(page_title="Verilogic Pro Titan", layout="centered")

if 'history' not in st.session_state: st.session_state.history = []

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    .v-header { text-align: center; color: #1C1C1E; font-weight: 900; font-size: 2.2rem; margin-top: -50px; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 700; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 30px; }
    
    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 15px !important; border: 1px solid #D1D1D6 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 24px; 
        margin: 15px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #1C1C1E; font-size: 2.4rem; font-weight: 900; margin: 5px 0; letter-spacing: -1.5px; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE TITAN ANALYTICAL ENGINE ---

def deep_scrub(text):
    """The 'Titan' Filter: Removes LaTeX, HTML, and formatting artifacts from insights"""
    # Specifically targets the {\displaystyle ...} junk seen in your screenshot
    text = re.sub(r'\{[^{}]*\}', '', text) 
    text = re.sub(r'\\displaystyle', '', text)
    text = re.sub(r'\\[a-z]+', '', text)
    text = re.sub(r'\s+', ' ', text) # Remove double spaces
    return text.strip()

def titan_engine(query):
    q_raw = query.lower().strip()
    
    # PASS 1: SCIENCE & ASTRO (NASA/ASTROPY DATA)
    # The 'Aun' fix: Using a 60% threshold to be even smarter about typos
    sci_lib = {
        "size of the sun": {"v": const.R_sun.to(u.km), "u": "kilometers", "desc": "Solar Radius"},
        "mass of the sun": {"v": const.M_sun, "u": "kg", "desc": "Solar Mass"},
        "speed of light": {"v": const.c.to(u.km/u.s), "u": "km/s", "desc": "Light Speed"},
    }
    
    match, score, _ = process.extractOne(q_raw, sci_lib.keys(), scorer=fuzz.WRatio)
    
    if score > 60:
        data = sci_lib[match]
        val = data['v'].value
        try: 
            wiki = deep_scrub(wikipedia.summary(match, sentences=3, auto_suggest=True))
        except: 
            wiki = f"The {data['desc']} is a fundamental constant in astrophysics, precisely measured at {val:,.0f} {data['u']}."
        
        return {
            "q": query, 
            "a": f"{val:,.0f} {data['u']}", 
            "i": wiki, 
            "t": "ASTRO CORE", 
            "lx": sp.latex(data['v'])
        }

    # PASS 2: MATH CORE (Symbolic Truth)
    if any(c.isdigit() or c in "xyz+-*/^()=" for c in q_raw):
        try:
            m_ready = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', q_raw) # 2x -> 2*x
            x = sp.symbols('x')
            if "=" in m_ready:
                lhs, rhs = m_ready.split("=")
                eq = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
                sol = sp.solve(eq)
                return {"q": query, "a": f"x = {sol}", "i": "Equation solved via symbolic isolation.", "t": "ALGEBRA", "lx": sp.latex(eq)}
            else:
                res = sp.simplify(m_ready)
                return {"q": query, "a": str(res), "i": "Symbolic reduction successful.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # PASS 3: GLOBAL LIBRARIAN
    try:
        wiki = deep_scrub(wikipedia.summary(query, sentences=3, auto_suggest=True))
        return {"q": query, "a": "Knowledge Retrieved", "i": wiki, "t": "LIBRARIAN", "lx": None}
    except:
        return {"q": query, "a": "Awaiting Command", "i": "Titan v33.0 is ready. Try 'size of aun' or '2x + 9x'.", "t": "SYSTEM", "lx": None}

# --- 3. VIEWPORT ---
st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">TITAN SRE WORKSPACE v33.0</div>', unsafe_allow_html=True)

with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Math, Science, or Fact Inquiry...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    res = titan_engine(u_in)
    st.session_state.history.insert(0, res)
    st.session_state.history = st.session_state.history[:50] # Optimized history

for item in st.session_state.history:
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:0.95rem; color:#3A3A3C; line-height:1.6;">💡 <b>Titan Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item.get('lx'): st.latex(item['lx'])
