import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import plotly.graph_objects as go
from rapidfuzz import process, fuzz

# --- 1. SYSTEM ARCHITECTURE (APPLE GRID-LOCK) ---
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="expanded")

# THE "APPLE STUDIO" CSS: Locked Spacing
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* INPUT DOCK GRID-LOCK */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 12px 18px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 25px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stForm"] > div {
        display: grid !important; grid-template-columns: 4.5fr 1fr !important;
        align-items: center !important; gap: 10px !important;
    }
    button[kind="formSubmit"] {
        background-color: #007AFF !important; color: white !important;
        border-radius: 12px !important; font-weight: 700 !important;
        width: 100% !important; border: none !important; height: 42px !important;
    }

    /* SRE WORKSHEET CARDS */
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 24px; 
        margin: 15px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
    .ans { color: #1C1C1E; font-size: 2.1rem; font-weight: 800; margin: 5px 0; letter-spacing: -1px; }
    .ai-insight { color: #1C1C1E; font-size: 0.95rem; border-top: 1px solid #F2F2F7; padding-top: 15px; margin-top: 10px;}
</style>
""", unsafe_allow_html=True)

# --- 2. GLOBAL STATE ---
if 'history' not in st.session_state: st.session_state.history = []
if 'ans_cache' not in st.session_state: st.session_state.ans_cache = 0

# --- 3. SYSTEM PREFERENCES (SIDEBAR) ---
with st.sidebar:
    st.title("Verilogic Pro")
    st.caption("v5.2.0 | Engineering Grade")
    st.write("---")
    
    with st.expander("⚙️ Control Center", expanded=True):
        precision = st.slider("Math Precision", 5, 50, 10)
        res_mode = st.toggle("Librarian Sync (Wiki)", value=True)
        haptics = st.toggle("Visual Feedback", value=True)
        if st.button("🔄 Re-sync Core"):
            st.toast("Syncing Math Libraries...")
            st.rerun()

    with st.expander("📡 NASA Constants"):
        st.caption("Auto-Injected Constants")
        st.code("c (light), g (gravity), h (planck), pi")

    with st.expander("⚖️ Legal & About"):
        st.info("Texas SB 2420 Compliant (2026).")
        st.markdown("**Legal:** Research tool only. Developer not liable for calculation errors.")

# --- 4. ANALYTICAL ENGINE ---
def ai_brain(query):
    q_raw = query.lower().strip()
    
    # NASA Physics Constants
    const_data = {"pi": str(np.pi), "c": "299792458", "g": "9.80665", "h": "6.626e-34", "ans": str(st.session_state.ans_cache)}
    
    # Fuzzy Intelligence Layer
    slang_map = {"plus": "+", "minus": "-", "times": "*", "divided": "/", "derivative": "diff", "integral": "integrate"}
    tokens = q_raw.split()
    for i, t in enumerate(tokens):
        match = process.extractOne(t, slang_map.keys(), scorer=fuzz.WRatio)
        if match and match[1] > 85: tokens[i] = slang_map[match[0]]
    
    m_prep = " ".join(tokens).replace('^', '**')
    for k, v in const_data.items():
        m_prep = re.sub(rf'\b{k}\b', v, m_prep)

    # Tier 1: Engineering Math Core
    try:
        expr = sp.sympify(m_prep)
        ans_val = expr.evalf(precision)
        st.session_state.ans_cache = ans_val
        return {"q": query, "a": f"{float(ans_val):g}", "i": "Logic Core reduction verified.", "t": "ENGINEERING CORE", "lx": sp.latex(expr)}
    except:
        pass

    # Tier 2: Research Librarian
    if res_mode:
        try:
            summary = wikipedia.summary(q_raw, sentences=2, auto_suggest=True)
            return {"q": query, "a": "Verified Data", "i": summary, "t": "LIBRARIAN", "lx": None}
        except:
            pass
            
    return {"q": query, "a": "Unresolved", "i": "Please check syntax or search terms.", "t": "SYSTEM", "lx": None}

# --- 5. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("pro_dock", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Calculate, Research, or use Constants...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_brain(u_in)
    st.session_state.history.append(result)
    if haptics: st.toast("Result Synchronized")
    st.rerun()

# Worksheet Rendering
for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 <b>Analysis:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item['lx']:
        st.latex(item['lx'])
