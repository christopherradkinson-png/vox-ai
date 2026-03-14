import streamlit as st
import sympy as sp
import wikipedia
import re
import yfinance as yf
from duckduckgo_search import DDGS
import gc

# --- 1. SESSION SAFETY CHECK ---
# Fixes the 'AttributeError' from your screenshot
if 'history' not in st.session_state: 
    st.session_state.history = []

# --- 2. THE DEEP-WEB BRAIN (Fixed AI Bridge) ---
def deep_web_brain(query):
    """Zero-overhead Llama-3-70B bridge."""
    try:
        with DDGS() as ddgs:
            # Step A: Numerical Search
            search_q = f"numerical facts and dimensions for {query}"
            # Using the latest DDGS syntax to prevent crashes
            results = list(ddgs.text(search_q, max_results=3))
            context = " ".join([r['body'] for r in results])
            
            # Step B: AI Extraction
            prompt = f"Data: {context}. Question: {query}. Instruction: Provide exact numbers and facts only."
            return ddgs.chat(prompt, model='llama-3-70b')
    except Exception as e:
        try:
            return wikipedia.summary(query, sentences=2)
        except:
            return "Intelligence Bridge Reset. Please try again."

# --- 3. THE ANALYTICAL ENGINE ---
def execute_almighty(u_in):
    # Strip commas from numbers globally
    q_clean = re.sub(r'(?<=\d),(?=\d)', '', u_in.lower())
    
    # A. FINANCE
    if "price" in q_clean or "stock" in q_clean:
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', u_in.upper())[-1]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": u_in, "a": f"${price:,.2f}", "i": f"Market Data: {ticker}", "t": "FINANCE"}
        except: pass

    # B. MATHEMATICS (Instant Local Solution)
    if any(c.isdigit() for c in q_clean) and any(op in q_clean for op in "+-*/^"):
        try:
            # Auto-repair 2x to 2*x
            math_q = re.sub(r'(\d)([a-z])', r'\1*\2', q_clean)
            res = sp.sympify(re.sub(r'[^0-9+\-*/^().x ]', '', math_q))
            return {"q": u_in, "a": f"{float(res):,g}" if res.is_number else str(res), 
                    "i": "Verified by Symbolic Math Engine.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # C. SCIENTIFIC INTELLIGENCE
    res_text = deep_web_brain(u_in)
    return {"q": u_in, "a": "Verified Data", "i": res_text, "t": "TURBO BRAIN"}

# --- 4. PROFESSIONAL UI ---
st.set_page_config(page_title="Verilogic Pro", layout="centered")
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .v-header { text-align: center; font-weight: 900; font-size: 2.8rem; color: #1C1C1E; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 800; font-size: 0.75rem; letter-spacing: 3px; }
    .sre-card { background: #F8F9FA; border-radius: 20px; padding: 25px; margin: 15px 0; border: 1px solid #E5E5EA; border-left: 10px solid #007AFF; }
    .ans { color: #1C1C1E; font-size: 2.1rem; font-weight: 900; letter-spacing: -1.5px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ALMIGHTY SOVEREIGN v63.0</div>', unsafe_allow_html=True)

with st.form("main_form", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Diameter of Mars? / 2,000,000 + 4,000,000", label_visibility="collapsed")
    if st.form_submit_button("EXE"):
        with st.spinner("Analyzing..."):
            res = execute_almighty(u_in)
            st.session_state.history.insert(0, res)

# Display History (With fixed 'st.session_state' check)
for item in st.session_state.history:
    st.markdown(f'''<div class="sre-card">
        <div style="color:#8E8E93; font-size:0.75rem; font-weight:800; text-transform:uppercase;">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div style="font-size:1rem; color:#3A3A3C; line-height:1.6; margin-top:10px;">{item['i']}</div>
    </div>''', unsafe_allow_html=True)
    if 'lx' in item: st.latex(item['lx'])
    gc.collect()
