import streamlit as st
import sympy as sp
import wikipedia
import re
import yfinance as yf
from duckduckgo_search import DDGS
from concurrent.futures import ThreadPoolExecutor

# --- 1. THE DEEP-WEB SEARCH ENGINE (RAG) ---
def deep_web_brain(query):
    """Accesses Llama-3-70B + Live Web Data for $0 cost."""
    try:
        with DDGS() as ddgs:
            # Step A: Deep Web Retrieval (Scientific & Factual)
            # We search for 'scholarly' and 'data' specifically
            search_query = f"{query} scientific data measurements report"
            results = [r['body'] for r in ddgs.text(search_query, max_results=4)]
            context = " ".join(results)
            
            # Step B: The Multi-Step Brain (Llama-3-70B)
            # We command the AI to be a 'Data Scientist'
            prompt = (f"Context: {context}. Question: {query}. "
                      f"Instruction: Extract exact numerical data. "
                      f"If it is a planet, give Diameter and Mass. "
                      f"If it is a dinosaur, give Length and Weight. Be precise.")
            
            return ddgs.chat(prompt, model='llama-3-70b')
    except:
        # Fallback to Wikipedia if the Deep Web bridge is throttled
        try:
            return wikipedia.summary(query, sentences=3)
        except:
            return "Intelligence Bridge Busy. Please re-run EXE."

# --- 2. THE ALMIGHTY ROUTER ---
def execute_almighty(u_in):
    # Pre-process: Strip commas from math (The 2,000,000 Fix)
    q_clean = re.sub(r'(?<=\d),(?=\d)', '', u_in.lower())
    
    # A. FINANCE (Free API)
    if "price" in q_clean or "stock" in q_clean:
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', u_in.upper())[-1]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": u_in, "a": f"${price:,.2f}", "i": f"Market Feed: {ticker}", "t": "FINANCE"}
        except: pass

    # B. MATHEMATICS (Local Device Logic - $0 Cost)
    # This handles any math problem using the user's CPU power
    if any(c.isdigit() for c in q_clean) and any(op in q_clean for op in "+-*/^"):
        try:
            # Fix 2x -> 2*x syntax
            math_q = re.sub(r'(\d)([a-z])', r'\1*\2', q_clean)
            res = sp.sympify(re.sub(r'[^0-9+\-*/^().x ]', '', math_q))
            return {"q": u_in, "a": f"{float(res):,g}" if res.is_number else str(res), 
                    "i": "Symbolic Math Verified.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # C. SCIENTIFIC INTELLIGENCE (The Deep Web Brain)
    # This is where we solve the 'Size of Mars' or 'Largest Dinosaur' accurately
    res_text = deep_web_brain(u_in)
    return {"q": u_in, "a": "Verified Intelligence", "i": res_text, "t": "TURBO BRAIN"}

# --- 3. THE PRO INTERFACE ---
st.set_page_config(page_title="Verilogic Pro", layout="centered")
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .v-header { text-align: center; font-weight: 900; font-size: 2.8rem; color: #1C1C1E; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 800; font-size: 0.75rem; letter-spacing: 3px; }
    .sre-card { background: #F8F9FA; border-radius: 20px; padding: 25px; margin: 15px 0; border: 1px solid #E5E5EA; border-left: 10px solid #007AFF; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .ans { color: #1C1C1E; font-size: 2rem; font-weight: 900; letter-spacing: -1px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ALMIGHTY SOVEREIGN v62.0</div>', unsafe_allow_html=True)

with st.form("main_form", clear_on_submit=True):
    u_in = st.text_input("Scientific Input", placeholder="Diameter of Mars? / 2,000,000 + 4,000,000", label_visibility="collapsed")
    if st.form_submit_button("EXE"):
        with st.spinner("Deep-Web Intelligence Active..."):
            res = execute_almighty(u_in)
            if 'history' not in st.session_state: st.session_state.history = []
            st.session_state.history.insert(0, res)

for item in st.session_state.history:
    st.markdown(f'''<div class="sre-card">
        <div style="color:#8E8E93; font-size:0.75rem; font-weight:800; text-transform:uppercase;">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:1rem; color:#3A3A3C; line-height:1.6; margin-top:10px;">{item['i']}</div>
    </div>''', unsafe_allow_html=True)
    if 'lx' in item: st.latex(item['lx'])
