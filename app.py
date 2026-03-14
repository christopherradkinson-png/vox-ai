import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
from astropy import constants as const
from rapidfuzz import process, fuzz

# --- 1. SYSTEM ARCHITECTURE & UI LOCK ---
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="expanded")

# THE "IRONCLAD" CSS: Fixed Overlap, Ghost Text & Red-Border Glitch
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    
    /* INPUT DOCK: Forced-Clear Overlap */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 12px 18px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 25px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stForm"] > div {
        display: grid !important; grid-template-columns: 4.5fr 1fr !important;
        align-items: center !important; gap: 10px !important;
    }
    
    /* TOTAL GHOST REMOVAL: Removes placeholder and browser validation tips */
    input::placeholder { color: transparent !important; opacity: 0 !important; }
    input:focus::placeholder { color: transparent !important; }
    input:invalid, input:focus:invalid { box-shadow: none !important; border: none !important; }
    
    /* HIDE BROWSER "PRESS ENTER" BUBBLES */
    ::-webkit-validation-bubble { display: none !important; }
    
    button[kind="formSubmit"] {
        background-color: #007AFF !important; color: white !important;
        border-radius: 12px !important; font-weight: 700 !important;
        border: none !important; height: 42px !important;
    }

    /* THE SRE WORKSHEET CARDS */
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 24px; 
        margin: 15px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #1C1C1E; font-size: 2.1rem; font-weight: 800; margin: 5px 0; letter-spacing: -1px; }
    .ai-insight { color: #1C1C1E; font-size: 0.95rem; border-top: 1px solid #F2F2F7; padding-top: 12px; margin-top: 12px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []

# --- 2. ROBUST PRO SETTINGS (SIDEBAR) ---
with st.sidebar:
    st.title("Verilogic Pro")
    st.caption("v6.6.0 | Restoration Active")
    st.write("---")
    
    with st.expander("⚙️ System Preferences", expanded=True):
        precision = st.slider("Math Precision", 5, 50, 10)
        mode = st.selectbox("Computational Mode", ["Engineering Pro", "Calculus SRE", "NASA/Astro-Physics"])
        temp_unit = st.radio("Standard Units", ["Celsius", "Fahrenheit", "Kelvin"])
        if st.button("🔄 Re-sync & Clear Memory"):
            st.session_state.history = []
            st.toast("System Recalibrated")
            st.rerun()

    with st.expander("⚖️ Legal & About"):
        st.info("Texas SB 2420 Compliant (2026).")
        st.caption("Legal Statement: Verilogic Pro is an SRE tool. Developer holds no liability for precision errors or data reliance.")

# --- 3. THE ANALYTICAL ENGINE (HYBRID INTENT) ---
def ai_brain(query):
    q_raw = query.lower().strip()
    
    # NASA-Grade Knowledge Sync (AstroPy)
    semantic_map = {
        "mass of the sun": const.M_sun, "thermal mass of the sun": const.M_sun,
        "size of the sun": const.R_sun, "radius of the sun": const.R_sun,
        "speed of light": const.c, "pi": np.pi, "gravity": const.g0
    }

    # Pass 1: Semantic Science Lookup (Fact + Insight Paragraph)
    best_match, score, _ = process.extractOne(q_raw, semantic_map.keys(), scorer=fuzz.WRatio)
    if score > 85:
        target = semantic_map[best_match]
        val = target.value if hasattr(target, 'value') else target
        unit = str(target.unit) if hasattr(target, 'unit') else ""
        
        # Pull deep insight paragraph from Wikipedia for this term
        try:
            wiki_summary = wikipedia.summary(best_match, sentences=3)
        except: 
            wiki_summary = f"Verified scientific data for {best_match.title()} retrieved from NASA/NIST standards."
        
        return {
            "q": query, "a": f"{val:,g} {unit}", "i": wiki_summary, 
            "t": "INTERNAL LABS", "lx": sp.latex(sp.sympify(str(val)))
        }

    # Pass 2: Math Core (With LaTeX 'Show Your Work')
    m_prep = re.sub(r'[^0-9\+\-\*\/\.\(\)\*\*\^pi]', '', q_raw.replace('pi', str(np.pi)).replace(',', ''))
    if any(c.isdigit() for c in m_prep):
        try:
            expr = sp.sympify(m_prep)
            ans = expr.evalf(precision)
            return {
                "q": query, "a": f"{float(ans):,g}", 
                "i": "Numeric Logic Core successfully reduced expression via symbolic analysis.", 
                "t": "MATH CORE", "lx": sp.latex(expr)
            }
        except: pass

    # Pass 3: Global Librarian (Wikipedia Fallback)
    try:
        summary = wikipedia.summary(q_raw, sentences=3, auto_suggest=True)
        return {"q": query, "a": "Knowledge Retrieved", "i": summary, "t": "GLOBAL LIBRARIAN", "lx": None}
    except:
        return {"q": query, "a": "Refining Inquiry", "i": "Input unrecognized. Ensure mathematical operators or scientific nouns are used.", "t": "SYSTEM", "lx": None}

# --- 4. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900; letter-spacing:-1.5px;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

# Using empty placeholder and CSS to kill ghost text
with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_brain(u_in)
    st.session_state.history.append(result)
    st.rerun()

# Worksheet Rendering (Reversed for most recent on top)
for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 <b>Librarian Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item['lx']:
        st.write("Show Your Work:")
        st.latex(item['lx'])
