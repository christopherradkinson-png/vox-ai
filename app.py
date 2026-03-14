import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from scipy import linalg, stats, optimize
from mendeleev import element
from astropy import constants as const
from astropy import units as u
from rapidfuzz import process, fuzz

# --- 1. PERFORMANCE CACHING (The "Sentinel" Fix) ---
@st.cache_data(ttl=3600, max_entries=100)
def cached_wiki(query):
    try: return wikipedia.summary(query, sentences=2, auto_suggest=True)
    except: return None

@st.cache_data(ttl=600)
def cached_finance(ticker):
    try: return yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
    except: return None

# --- 2. SYSTEM UI & BRANDING ---
st.set_page_config(page_title="Verilogic Pro Sentinel", layout="centered")

if 'history' not in st.session_state: st.session_state.history = []
if 'registry' not in st.session_state: st.session_state.registry = {}

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; font-family: -apple-system, sans-serif; }
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

# --- 3. THE REPAIRED ENGINE ---
def sentinel_engine(query):
    q_raw = query.lower().strip()
    
    # PASS 1: ASTRO & SCIENCE (Unit-Safe)
    science_map = {"size of the sun": const.R_sun, "speed of light": const.c}
    match, score, _ = process.extractOne(q_raw, science_map.keys(), scorer=fuzz.WRatio)
    if score > 85:
        data = science_map[match]
        val_km = data.to(u.km).value if hasattr(data, 'to') else data
        wiki = cached_wiki(match) or "Verified via NASA/Astropy standard constants."
        return {"q": query, "a": f"{val_km:,.0f} km", "i": wiki, "t": "ASTRO CORE", "lx": sp.latex(data)}

    # PASS 2: FINANCE (Cached)
    if "price" in q_raw:
        ticker = re.findall(r'[a-zA-Z]{1,5}', q_raw.upper())
        price = cached_finance(ticker[0]) if ticker else None
        if price: return {"q": query, "a": f"${price:,.2f}", "i": f"Latest market data for {ticker[0]}.", "t": "FINANCE", "lx": None}

    # PASS 3: SMART MATH (Implicit Fix)
    try:
        math_ready = re.sub(r'(\d)([a-z])', r'\1*\2', q_raw)
        res = sp.simplify(math_ready)
        return {"q": query, "a": str(res), "i": "Symbolic reduction successful.", "t": "MATH CORE", "lx": sp.latex(res)}
    except: pass

    # PASS 4: LIBRARIAN
    wiki_res = cached_wiki(query)
    if wiki_res: return {"q": query, "a": "Knowledge Found", "i": wiki_res, "t": "LIBRARIAN", "lx": None}
    
    return {"q": query, "a": "System Stable", "i": "Ready for next input.", "t": "SYSTEM", "lx": None}

# --- 4. THE VIEWPORT ---
st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">SRE SENTINEL ENVIRONMENT v27.0</div>', unsafe_allow_html=True)

with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Math, Science, Stock Prices, or Chemistry...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    res = sentinel_engine(u_in)
    # Memory Cap: Keep only last 50 items to prevent bloat
    st.session_state.history.insert(0, res)
    st.session_state.history = st.session_state.history[:50]

for item in st.session_state.history:
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:0.9rem; color:#3A3A3C; line-height:1.5;">💡 <b>Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item.get('lx'): st.latex(item['lx'])
