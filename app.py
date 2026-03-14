import streamlit as st
import sympy as sp
import wikipedia
import re
import yfinance as yf
from duckduckgo_search import DDGS

# --- 1. THE BRAIN ENGINE (Llama-3 via Free Bridge) ---
def ask_the_brain(query):
    """Uses a free, no-token bridge to Llama-3-8B"""
    try:
        with DDGS() as ddgs:
            # We tell the AI to be a precise Science/Finance assistant
            prompt = f"System: Answer concisely. User: {query}"
            results = ddgs.chat(prompt, model='llama-3-70b')
            return results
    except Exception as e:
        return None

# --- 2. THE MULTI-DOMAIN ENGINE ---
def almighty_engine(query):
    q_raw = query.lower().strip()
    
    # PASS 1: Finance (Real-time Stocks)
    if any(x in q_raw for x in ["price", "stock", "market"]):
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', q_raw.upper())[-1]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": query, "a": f"${price:,.2f}", "i": f"Live market data for {ticker}.", "t": "FINANCE"}
        except: pass

    # PASS 2: Symbolic Math (SymPy)
    if any(c.isdigit() for c in q_raw) and any(op in q_raw for op in "+-*/^"):
        try:
            res = sp.simplify(re.sub(r'(\d)([a-z])', r'\1*\2', q_raw))
            return {"q": query, "a": str(res), "i": "Verified via SymPy Core.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # PASS 3: The "Brain" (Llama-3 Intelligence)
    # This handles "Size of the sun", "Who is...", "Explain chemistry..."
    brain_response = ask_the_brain(query)
    if brain_response:
        return {"q": query, "a": "Analysis Complete", "i": brain_response, "t": "LLAMA-3 BRAIN"}

    # PASS 4: Wikipedia (Last Resort)
    try:
        summary = wikipedia.summary(query, sentences=2)
        return {"q": query, "a": "Retrieved", "i": summary, "t": "LIBRARIAN"}
    except:
        return {"q": query, "a": "Active", "i": "System online.", "t": "SYSTEM"}

# --- 3. PRO UI ---
st.set_page_config(page_title="Verilogic Pro", layout="centered")
if 'history' not in st.session_state: st.session_state.history = []

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .main-title { text-align: center; font-weight: 900; font-size: 2.5rem; color: #1C1C1E; }
    .card { background: #F2F2f7; border-radius: 18px; padding: 20px; margin: 10px 0; border: 1px solid #E5E5EA; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .meta { color: #007AFF; font-weight: 800; font-size: 0.75rem; text-transform: uppercase; }
    .ans-text { font-size: 1.8rem; font-weight: 800; color: #1C1C1E; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#007AFF; font-weight:bold;">ALMIGHTY BRAIN v45.0</p>', unsafe_allow_html=True)

with st.form("main", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="What is the size of the sun? / 2x+5x / AAPL price", label_visibility="collapsed")
    if st.form_submit_button("EXECUTE"):
        with st.spinner("Llama-3 is thinking..."):
            res = almighty_engine(u_in)
            st.session_state.history.insert(0, res)

for item in st.session_state.history:
    st.markdown(f'''
    <div class="card">
        <div class="meta">{item['t']} | {item['q']}</div>
        <div class="ans-text">= {item['a']}</div>
        <div style="font-size: 1rem; color: #3A3A3C; line-height: 1.5;">{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if 'lx' in item: st.latex(item['lx'])
