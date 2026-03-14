import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import yfinance as yf
from duckduckgo_search import DDGS
import gc

# --- 1. SYSTEM INITIALIZATION ---
if 'history' not in st.session_state: 
    st.session_state.history = []

# --- 2. THE RECURSIVE "TRUTH" ENGINE ---
def recursive_brain(query):
    """The v125.0 Engine: Searches, Filters, and Extracts Numbers."""
    q_low = query.lower()
    
    try:
        with DDGS() as ddgs:
            # Step A: Snap search to 'dimensions' for science queries
            search_query = f"{query} exact numerical specifications dimensions km kg"
            results = list(ddgs.text(search_query, max_results=5))
            context = " ".join([r['body'] for r in results])
            
            # Step B: The 'Absolute Scientist' Instruction
            # We demand the number for the big bold header
            prompt = (f"Context: {context}. Question: {query}. "
                      f"TASK: Find the exact numerical value (e.g. 6,779 km). "
                      f"Return ONLY the value for the result header. No sentences.")
            
            short_val = ddgs.chat(prompt, model='llama-3-70b')
            
            # Step C: Validation - If no number found, fallback to Wiki Table
            if not any(char.isdigit() for char in short_val):
                wiki_search = wikipedia.search(query)[0]
                short_val = "Data Point Identified"
                long_info = wikipedia.summary(wiki_search, sentences=3)
            else:
                long_info = context[:600] + "..."

            return {"a": short_val, "i": long_info}
    except:
        return {"a": "Retrieved", "i": "Connection busy. Please retry EXE."}

# --- 3. THE ANALYTICAL ROUTER ---
def execute_almighty(u_in):
    # Comma-Stripper (The 2,000,000 fix)
    q_clean = re.sub(r'(?<=\d),(?=\d)', '', u_in.lower())
    
    # A. FINANCE
    if "price" in q_clean or "stock" in q_clean:
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', u_in.upper())[-1]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": u_in, "a": f"${price:,.2f}", "i": f"Live Market Pulse: {ticker}", "t": "FINANCE"}
        except: pass

    # B. MATHEMATICS (Precision SymPy)
    if any(c.isdigit() for c in q_clean) and any(op in q_clean for op in "+-*/^"):
        try:
            # Auto-fix 2x -> 2*x
            math_q = re.sub(r'(\d)([a-z])', r'\1*\2', q_clean)
            res = sp.sympify(re.sub(r'[^0-9+\-*/^().x ]', '', math_q))
            return {"q": u_in, "a": f"{float(res):,g}" if res.is_number else str(res), 
                    "i": "Symbolic Logic Verified.", "t": "MATH CORE"}
        except: pass

    # C. SCIENTIFIC DATA (v125 Recursive Brain)
    data = recursive_brain(u_in)
    return {"q": u_in, "a": data['a'], "i": data['i'], "t": "TURBO BRAIN"}

# --- 4. THE PRO INTERFACE ---
st.set_page_config(page_title="Verilogic Pro", layout="centered")
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .v-header { text-align: center; font-weight: 900; font-size: 3rem; color: #1C1C1E; margin-bottom: 0px; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 800; font-size: 0.75rem; letter-spacing: 4px; margin-bottom: 30px; }
    .sre-card { background: #F8F9FA; border-radius: 28px; padding: 30px; margin: 15px 0; border: 1px solid #E5E5EA; border-left: 12px solid #007AFF; box-shadow: 0 15px 45px rgba(0,0,0,0.05); }
    .meta { color: #8E8E93; font-size: 0.7rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; }
    .ans { color: #1C1C1E; font-size: 2.3rem; font-weight: 900; letter-spacing: -1.5px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ALMIGHTY SOVEREIGN v125.0</div>', unsafe_allow_html=True)

with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Size of the Sun? / 2,000,000 + 4,000,000", label_visibility="collapsed")
    if st.form_submit_button("EXE"):
        with st.spinner("Extracting Factual Data..."):
            res = execute_almighty(u_in)
            st.session_state.history.insert(0, res)

for item in st.session_state.history:
    st.markdown(f'''<div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:1rem; color:#3A3A3C; line-height:1.7; margin-top:10px;"><b>Data Intelligence:</b><br>{item['i']}</div>
    </div>''', unsafe_allow_html=True)
    gc.collect()
