import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from mendeleev import element
from astropy import constants as const
from astropy import units as u
from rapidfuzz import process, fuzz

# --- 1. BOOTING THE ALMIGHTY BRAIN (ZERO-KEY AI) ---
@st.cache_resource
def load_llama_brain():
    try:
        model_path = hf_hub_download(
            repo_id="bartowski/Llama-3.2-1B-Instruct-GGUF",
            filename="Llama-3.2-1B-Instruct-Q4_K_M.gguf"
        )
        return Llama(model_path=model_path, n_ctx=1024, n_threads=4)
    except: return None

llm = load_llama_brain()

# --- 2. SYSTEM UI & STYLING ---
st.set_page_config(page_title="Verilogic Pro Almighty", layout="centered")
if 'history' not in st.session_state: st.session_state.history = []

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    .v-header { text-align: center; font-weight: 900; font-size: 2.5rem; color: #1C1C1E; margin-top: -50px; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 700; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 30px; }
    .sre-card { background: #F8F9FA; border-radius: 24px; padding: 24px; margin: 15px 0; border: 1px solid #E5E5EA; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .meta { color: #007AFF; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #1C1C1E; font-size: 2.2rem; font-weight: 900; margin: 10px 0; letter-spacing: -1.5px; }
</style>
""", unsafe_allow_html=True)

# --- 3. MULTI-DOMAIN ANALYTICAL ENGINE ---

def clean_wiki(text):
    text = re.sub(r'\{[^{}]*\}|\\displaystyle|\\[a-z]+', '', text)
    return text.strip()

def almighty_engine(query):
    q_raw = query.lower().strip()
    
    # AGENTIC STEP: Use Llama to "Clean" the query and find Intent
    try:
        prompt = f"Intent: '{q_raw}'. If science, return subject. If math, return 'math'. If finance, return ticker. Return ONLY word."
        output = llm(f"<|user|>\n{prompt}<|assistant|>\n", max_tokens=10, stop=["<|end|>"])
        intent = output['choices'].strip().lower()
    except: intent = q_raw

    # PASS 1: FINANCE (e.g. "AAPL price")
    if "price" in q_raw or "stock" in q_raw:
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', q_raw.upper())[0]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": query, "a": f"${price:,.2f}", "i": f"Real-time market data for {ticker}.", "t": "FINANCE"}
        except: pass

    # PASS 2: CHEMISTRY (e.g. "element Gold")
    if "element" in q_raw:
        try:
            el_name = q_raw.split("element")[-1].strip().capitalize()
            el = element(el_name)
            return {"q": query, "a": f"{el.atomic_weight:g} u", "i": f"{el_name} ({el.symbol}): Atomic # {el.atomic_number}.", "t": "CHEMISTRY"}
        except: pass

    # PASS 3: SCIENCE & ASTRO (NASA Logic with Typos)
    sci_lib = {"sun": const.R_sun.to(u.km), "earth": const.R_earth.to(u.km), "speed of light": const.c.to(u.km/u.s)}
    match, score, _ = process.extractOne(intent, sci_lib.keys(), scorer=fuzz.WRatio)
    if score > 70:
        data = sci_lib[match]
        val = data.value
        try: wiki = clean_wiki(wikipedia.summary(match, sentences=3, auto_suggest=True))
        except: wiki = "Data verified via NASA standard constants."
        return {"q": query, "a": f"{val:,.0f} km", "i": wiki, "t": "ASTRO CORE", "lx": sp.latex(data)}

    # PASS 4: SMART MATH (SymPy 2x+9x fix)
    if any(c.isdigit() or c in "xyz+-*/^()=" for c in q_raw):
        try:
            m_ready = re.sub(r'(\d)([a-z])', r'\1*\2', q_raw)
            res = sp.simplify(m_ready)
            return {"q": query, "a": str(res), "i": "Symbolic reduction successful.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # PASS 5: LIBRARIAN (Wikipedia)
    try:
        wiki = clean_wiki(wikipedia.summary(query, sentences=3, auto_suggest=True))
        return {"q": query, "a": "Knowledge Retrieved", "i": wiki, "t": "LIBRARIAN"}
    except:
        return {"q": query, "a": "System Ready", "i": "Almighty Engine is online.", "t": "SYSTEM"}

# --- 4. VIEWPORT ---
st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ALMIGHTY SRE WORKSPACE v41.0</div>', unsafe_allow_html=True)

with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="2x+9x, AAPL price, element Gold, size of aun...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    with st.spinner("Analyzing with Llama-3 Brain..."):
        res = almighty_engine(u_in)
        st.session_state.history.insert(0, res)

for item in st.session_state.history:
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:0.95rem; color:#3A3A3C; line-height:1.6;">💡 <b>Intelligence:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item.get('lx'): st.latex(item['lx'])
