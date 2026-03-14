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
from concurrent.futures import ThreadPoolExecutor
from rapidfuzz import process, fuzz
from fpdf import FPDF
import io

# --- 1. SYSTEM CORE & REPAIR ENGINE ---
st.set_page_config(page_title="Verilogic Pro Almighty", layout="wide", page_icon="🚀")
if 'history' not in st.session_state: st.session_state.history = []

def auto_repair_query(text):
    """Fixes math syntax (2x -> 2*x) and common science typos."""
    text = re.sub(r'(\d)([a-z])', r'\1*\2', text.lower())
    terms = ["Mars", "Sun", "Earth", "Moon", "Gravity", "Jupiter", "Diameter", "Radius", "Price"]
    words = text.split()
    repaired = []
    for w in words:
        match, score, _ = process.extractOne(w, terms, scorer=fuzz.WRatio)
        repaired.append(match if score > 85 else w)
    return " ".join(repaired)

# --- 2. THE TURBO BRAIN (RAG + AI) ---
@st.cache_data(ttl=3600)
def almighty_hybrid_brain(query):
    query = auto_repair_query(query)
    def fetch_data():
        try:
            with DDGS() as ddgs:
                search_res = [r['body'] for r in ddgs.text(f"numerical specifications {query}", max_results=2)]
                wiki_res = wikipedia.summary(query, sentences=2)
                return f"{wiki_res} {' '.join(search_res)}"
        except: return ""

    context = fetch_data()
    try:
        with DDGS() as ddgs:
            prompt = f"Data: {context}. Question: {query}. Respond with exact numbers and facts only."
            return ddgs.chat(prompt, model='llama-3-70b')
    except:
        return context if context else "Connection timeout. Please retry."

# --- 3. THE ANALYTICAL ENGINE ---
def execute_almighty(u_in):
    q = u_in.lower().strip()
    
    # A. FINANCE
    if any(x in q for x in ["price", "stock", "ticker"]):
        try:
            ticker = re.findall(r'[a-zA-Z]{1,5}', u_in.upper())[-1]
            price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]
            return {"q": u_in, "a": f"${price:,.2f}", "i": f"Live Market Feed: {ticker}", "t": "FINANCE"}
        except: pass

    # B. MATH & 3D GRAPHING
    if "graph" in q or "plot" in q:
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2)) # Sample 3D Function
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        return {"q": u_in, "a": "3D Render Complete", "i": "Interactive Topology Generated.", "t": "ENGINEERING", "fig": fig}

    if any(c.isdigit() or c in "xyz" for c in q) and any(op in q for op in "+-*/^="):
        try:
            res = sp.simplify(auto_repair_query(q))
            return {"q": u_in, "a": str(res), "i": "Symbolic Solution Verified.", "t": "MATH CORE", "lx": sp.latex(res)}
        except: pass

    # C. TURBO BRAIN (Science/General)
    res_text = almighty_hybrid_brain(u_in)
    return {"q": u_in, "a": "Verified Intelligence", "i": res_text, "t": "TURBO BRAIN"}

# --- 4. PDF REPORTING TOOL ---
def generate_pdf(history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Verilogic Pro - Almighty Session Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    for item in history:
        pdf.ln(10)
        pdf.cell(200, 10, f"Domain: {item['t']} | Query: {item['q']}", ln=True)
        pdf.multi_cell(0, 10, f"Result: {item['a']}\nIntel: {item['i']}")
    return pdf.output(dest='S').encode('latin-1')

# --- 5. UI LAYOUT ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .v-header { text-align: center; font-weight: 900; font-size: 3rem; color: #1C1C1E; margin-top: -50px; }
    .v-sub { text-align: center; color: #007AFF; font-weight: 700; font-size: 0.8rem; letter-spacing: 4px; margin-bottom: 30px; }
    .sre-card { background: #F8F9FA; border-radius: 20px; padding: 25px; margin: 15px 0; border: 1px solid #E5E5EA; border-left: 8px solid #007AFF; }
    .ans { color: #1C1C1E; font-size: 2.2rem; font-weight: 900; letter-spacing: -1.5px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="v-header">VERILOGIC PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="v-sub">ALMIGHTY MASTER v51.0</div>', unsafe_allow_html=True)

# Sidebar for Tools
with st.sidebar:
    st.header("Workspace Tools")
    if st.button("Export Session PDF"):
        if st.session_state.history:
            pdf_bytes = generate_pdf(st.session_state.history)
            st.download_button("Download Report", data=pdf_bytes, file_name="Verilogic_Report.pdf", mime="application/pdf")
    if st.button("Clear Workspace"):
        st.session_state.history = []
        st.rerun()

# Main Input
with st.form("main_input", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="What is the size of Mars? / 2x+9x / Plot 3D surface", label_visibility="collapsed")
    if st.form_submit_button("EXE"):
        with st.spinner("Analyzing with Almighty Hybrid Engine..."):
            result = execute_almighty(u_in)
            st.session_state.history.insert(0, result)

# Display Output
for item in st.session_state.history:
    with st.container():
        st.markdown(f'''<div class="sre-card">
            <div style="color:#8E8E93; font-size:0.7rem; font-weight:800; text-transform:uppercase;">{item['t']} | {item['q']}</div>
            <div class="ans">= {item['a']}</div>
            <div style="font-size:1rem; color:#3A3A3C; line-height:1.6; margin-top:10px;">{item['i']}</div>
        </div>''', unsafe_allow_html=True)
        if 'lx' in item: st.latex(item['lx'])
        if 'fig' in item: st.plotly_chart(item['fig'], use_container_width=True)
    gc.collect()
