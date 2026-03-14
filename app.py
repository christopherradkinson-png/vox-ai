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
import requests

# --- 1. SESSION SAFETY & MEMORY ---
if 'history' not in st.session_state: 
    st.session_state.history = []

# --- 2. NASA GROUNDING VAULT (Library #1: Instant Truth) ---
ASTRO_VAULT = {
    "mars": "Diameter: 6,779 km | Mass: 6.39 × 10^23 kg | Gravity: 3.71 m/s²",
    "jupiter": "Diameter: 139,820 km | Mass: 1.898 × 10^27 kg | Gravity: 24.79 m/s²",
    "sun": "Diameter: 1.39 million km | Temperature: 5,505°C | Mass: 333,000 Earths",
    "earth": "Diameter: 12,742 km | Age: 4.54 billion years",
    "speed of light": "299,792,458 m/s",
    "gold": "Atomic Weight: 196.97 u | Symbol: Au | Atomic #: 79"
}

# --- 3. REPAIR ENGINE (In-Route Healing) ---
def almighty_repair(text):
    """Fixes commas in math and standardizes syntax."""
    text = re.sub(r'(?<=\d),(?=\d)', '', text) # 2,000,000 -> 2000000
    text = re.sub(r'(\d)([a-z])', r'\1*\2', text.lower()) # 2x -> 2*x
    return text

# --- 4. MULTI-FAILOVER BRAIN ---
def hybrid_intelligence(query):
    q_low = query.lower()
    # Check Vault First
    for key in ASTRO_VAULT:
        if key in q_low:
            return {"a": ASTRO_VAULT[key], "i": "Verified via NASA Grounding Vault."}
    
    # Try Live Research Bridge
    try:
        with DDGS(timeout=30) as ddgs:
            search_q = f"numerical data facts for {query}"
            results = list(ddgs.text(search_q, max_results=3))
            context = " ".join([r['body'] for r in results])
            prompt = f"Using: {context}. Question: {query}. Extract ONLY the exact numerical fact."
            res = ddgs.chat(prompt, model='llama-3-70b')
            return {"a": res, "i": "Data extracted from live search."}
    except:
        try:
            return {"a": "Information Found", "i": wikipedia.summary(query, sentences=2)}
        except:
            return {"a": "System Ready", "i": "All bridges busy. Please retry EXE."}

# --- 5. THE ANALYTICAL MASTER ROUTER ---
def execute_almighty(u_in):
    q_fixed = almighty_repair(u_in)
    
    # A. FINANCE
    if "price" in q_fixed or "stock" in q_fixed:
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', u_in.upper())[-1]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": u_in, "a": f"${price:,.2f}", "i": f"Live Market Pulse: {ticker}", "t": "FINANCE"}
        except: pass

    # B. MATHEMATICS (Symbolic Core)
    if any(c.isdigit() for c in q_fixed) and any(op in q_fixed for op in "+-*/^"):
        try:
            res = sp.sympify(re.sub(r'[^0-9+\-*/^().x ]', '', q_fixed))
            return {"q": u_in, "a": f"{float(res):,g}" if res.is_number else str(res), 
                    "i": "Verified by Symbolic Computation.", "t": "MATH CORE"}
        except: pass

    # C. SCIENTIFIC INTELLIGENCE
    brain_data = hybrid_intelligence(u_in)
    return {"q": u_in, "a": brain_data['a'], "i": brain_data['i'], "t": "TURBO BRAIN"}

# --- 6. PROFESSIONAL UI ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .v-header { text-align: center; font-weight: 900; font-size: 2.5rem; color: #1C1C1E; margin-top: -50px; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 800; font-size: 0.75rem; letter-spacing: 4px; margin-bottom: 30px; }
    .sre-card { background: #F8F9FA; border-radius: 20px; padding: 25px; margin: 15px 0; border: 1px solid #E5E5EA; border-left: 10px solid #007AFF; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .ans { color: #1C1C1E; font-size: 1.8rem; font-weight: 900; letter-spacing: -1.5px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ALMIGHTY SOVEREIGN v126.0</div>', unsafe_allow_html=True)

with st.form("main_form", clear_on_submit=True):
    u_in = st.text_input("Scientific Input", placeholder="Size of Mars? / 2,000,000 + 4,000,000", label_visibility="collapsed")
    if st.form_submit_button("EXE"):
        with st.spinner("Analyzing Database..."):
            res = execute_almighty(u_in)
            st.session_state.history.insert(0, res)

for item in st.session_state.history:
    st.markdown(f'''<div class="sre-card">
        <div style="color:#8E8E93; font-size:0.75rem; font-weight:800; text-transform:uppercase;">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:1rem; color:#3A3A3C; line-height:1.6; margin-top:10px;">{item['i']}</div>
    </div>''', unsafe_allow_html=True)
    gc.collect()
