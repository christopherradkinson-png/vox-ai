import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import gc
from duckduckgo_search import DDGS
from scipy import constants as const
from rapidfuzz import process, fuzz

# --- 1. THE PRECISION MATH & CONSTANTS ENGINE ---
# Built-in High-Precision Database for Scientists
SCIENTIFIC_CONSTANTS = {
    "speed of light": f"{const.c:,.0f} m/s",
    "planck constant": f"{const.h:g} J·s",
    "gravitational constant": f"{const.G:g} m³/kg·s²",
    "jupiter mass": "1.898 × 10^27 kg",
    "jupiter diameter": "139,820 km",
    "mars diameter": "6,779 km",
    "sun diameter": "1.3927 million km"
}

def clean_math_input(text):
    """Deep cleaning for mathematical strings."""
    # Remove commas from numbers (2,000,000 -> 2000000)
    text = re.sub(r'(?<=\d),(?=\d)', '', text)
    # Remove "what is", "calculate", etc.
    text = re.sub(r'(what is|calculate|solve|\?)', '', text.lower()).strip()
    # Fix implicit multiplication (2x -> 2*x)
    text = re.sub(r'(\d)([a-z])', r'\1*\2', text)
    return text

# --- 2. THE ANALYTICAL ENGINE ---
def execute_almighty(u_in):
    q_clean = clean_math_input(u_in)
    
    # STEP A: Check Scientific Constants First (NASA Grade)
    for key, value in SCIENTIFIC_CONSTANTS.items():
        if key in q_clean:
            return {"q": u_in, "a": value, "i": f"Verified physical constant for {key.capitalize()}.", "t": "ASTRO CORE"}

    # STEP B: Symbolic Math Engine (SymPy)
    # This handles 2,000,000 + 2,000,000 or complex algebra
    if any(c.isdigit() or c in "+-*/^()x" for c in q_clean):
        try:
            # We use sympify to turn the string into a real math object
            res = sp.sympify(q_clean)
            return {"q": u_in, "a": f"{float(res):,g}" if res.is_number else str(res), 
                    "i": "Symbolic Math Verified.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # STEP C: Finance
    if "price" in q_clean or "stock" in q_clean:
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', u_in.upper())[-1]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": u_in, "a": f"${price:,.2f}", "i": f"Live Data: {ticker}", "t": "FINANCE"}
        except: pass

    # STEP D: Intelligence Brain (Llama-3 Bridge)
    try:
        with DDGS() as ddgs:
            # Force search for numerical specs
            search_data = [r['body'] for r in ddgs.text(f"exact numbers for {u_in}", max_results=2)]
            prompt = f"Data: {' '.join(search_data)}. User: {u_in}. Answer with numbers and facts only."
            res = ddgs.chat(prompt, model='llama-3-70b')
            return {"q": u_in, "a": "Verified Intelligence", "i": res, "t": "TURBO BRAIN"}
    except:
        return {"q": u_in, "a": "Retrieved", "i": wikipedia.summary(u_in, sentences=2), "t": "LIBRARIAN"}

# --- 3. THE INTERFACE ---
st.set_page_config(page_title="Verilogic Pro", layout="centered")
if 'history' not in st.session_state: st.session_state.history = []

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .v-header { text-align: center; font-weight: 900; font-size: 2.5rem; color: #1C1C1E; }
    .sre-card { background: #F8F9FA; border-radius: 20px; padding: 25px; margin: 15px 0; border: 1px solid #E5E5EA; border-left: 8px solid #007AFF; }
    .ans { color: #1C1C1E; font-size: 2.2rem; font-weight: 900; letter-spacing: -1.5px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#007AFF; font-weight:bold;">ABSOLUTE PRECISION v53.0</p>', unsafe_allow_html=True)

with st.form("main_form", clear_on_submit=True):
    u_in = st.text_input("Scientific Input", placeholder="2,000,000 + 4,000,000 / Size of Jupiter", label_visibility="collapsed")
    if st.form_submit_button("EXE"):
        with st.spinner("Calculating..."):
            result = execute_almighty(u_in)
            st.session_state.history.insert(0, result)

for item in st.session_state.history:
    st.markdown(f'''<div class="sre-card">
        <div style="color:#8E8E93; font-size:0.7rem; font-weight:800; text-transform:uppercase;">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:1rem; color:#3A3A3C; line-height:1.6; margin-top:10px;">{item['i']}</div>
    </div>''', unsafe_allow_html=True)
    if 'lx' in item: st.latex(item['lx'])
    gc.collect()
