import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import requests
from rapidfuzz import process, fuzz

# --- 1. THE CLOUD BRAIN (ZERO-RAM AI) ---
# Tip: Get a free token at https://huggingface.co
HF_TOKEN = st.secrets.get("HF_TOKEN", "") 
API_URL = "https://api-inference.huggingface.co"

def query_llama_cloud(prompt):
    if not HF_TOKEN: return "SYSTEM"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": f"<|user|>\n{prompt}<|assistant|>\n", "parameters": {"max_new_tokens": 10}}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        res_json = response.json()
        return res_json[0]['generated_text'].split("<|assistant|>")[-1].strip().upper()
    except: return "SYSTEM"

# --- 2. LIGHTWEIGHT KNOWLEDGE BASE (Replaces heavy Mendeleev/Astropy) ---
ELEMENTS = {"Gold": {"s": "Au", "w": 196.97, "n": 79}, "Iron": {"s": "Fe", "w": 55.84, "n": 26}}
CONSTANTS = {"sun": "695,700 km", "earth": "6,371 km", "speed of light": "299,792 km/s"}

# --- 3. SYSTEM UI ---
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

def almighty_engine(query):
    q_raw = query.lower().strip()
    
    # 🧠 CLOUD INTENT ROUTING
    intent_prompt = f"Categorize: '{q_raw}'. Options: [FINANCE, CHEM, MATH, ASTRO, WIKI]. One word only."
    intent = query_llama_cloud(intent_prompt)

    # 1. FINANCE
    if "price" in q_raw or "stock" in q_raw or "FINANCE" in intent:
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', q_raw.upper())[-1]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": query, "a": f"${price:,.2f}", "i": f"Live market data for {ticker}.", "t": "FINANCE"}
        except: pass

    # 2. CHEMISTRY
    if "element" in q_raw or "CHEM" in intent:
        name = q_raw.replace("element", "").strip().capitalize()
        if name in ELEMENTS:
            e = ELEMENTS[name]
            return {"q": query, "a": f"{e['w']} u", "i": f"{name} ({e['s']}): Atomic # {e['n']}.", "t": "CHEMISTRY"}

    # 3. MATH
    if any(c.isdigit() for c in q_raw) or "MATH" in intent:
        try:
            res = sp.simplify(re.sub(r'(\d)([a-z])', r'\1*\2', q_raw))
            return {"q": query, "a": str(res), "i": "Symbolic math verification complete.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # 4. WIKIPEDIA
    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        return {"q": query, "a": "Knowledge retrieved", "i": summary, "t": "LIBRARIAN"}
    except:
        return {"q": query, "a": "Online", "i": "Systems standing by.", "t": "SYSTEM"}

# --- 4. VIEWPORT ---
st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ALMIGHTY SRE WORKSPACE v42.0</div>', unsafe_allow_html=True)

with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="AAPL price, 2x+9x, element Gold...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    with st.spinner("Cloud Brain Analyzing..."):
        res = almighty_engine(u_in)
        st.session_state.history.insert(0, res)

for item in st.session_state.history:
    st.markdown(f'''<div class="sre-card"><div class="meta">{item['t']} | {item['q']}</div><div class="ans">= {item['a']}</div>
    <div style="font-size:0.9rem; color:#3A3A3C;">💡 {item['i']}</div></div>''', unsafe_allow_html=True)
    if 'lx' in item: st.latex(item['lx'])
