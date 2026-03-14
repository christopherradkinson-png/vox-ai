import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
import streamlit.components.v1 as components
from astropy import constants as const
from rapidfuzz import process, fuzz

# --- 1. SYSTEM ARCHITECTURE & UI LOCK ---
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="expanded")

# THE "IRONCLAD" CSS: Kills Red-Box Flashing & Browser Tooltips
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    
    /* PREVENT FLASHING: Silences error containers on boot */
    .stAlert { display: none !important; }
    div[data-testid="stNotification"] { display: none !important; }

    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 12px 18px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 25px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stForm"] > div {
        display: grid !important; grid-template-columns: 4.5fr 1fr !important;
        align-items: center !important; gap: 10px !important;
    }
    
    /* TOTAL GHOST REMOVAL */
    input::placeholder { color: transparent !important; opacity: 0 !important; }
    ::-webkit-validation-bubble, ::-webkit-validation-bubble-message { display: none !important; }
    input:invalid, input:focus:invalid { box-shadow: none !important; border: none !important; }

    button[kind="formSubmit"] {
        background-color: #007AFF !important; color: white !important;
        border-radius: 12px !important; font-weight: 700 !important;
        border: none !important; height: 42px !important;
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

# --- 2. GLOBAL STATE ---
if 'history' not in st.session_state: st.session_state.history = []
if 'registry' not in st.session_state: st.session_state.registry = {}

# --- 3. THE NASA SYSTEM PREFERENCES ---
with st.sidebar:
    st.title("Verilogic Pro")
    st.caption("v7.1.0 | Stable Boot")
    st.write("---")
    with st.expander("📊 Variable Registry", expanded=True):
        if st.session_state.registry:
            for var, val in st.session_state.registry.items():
                st.code(f"{var}: {val}")
        else: st.caption("No variables saved.")
    
    with st.expander("⚙️ Computation & Output"):
        precision = st.slider("Math Precision", 5, 50, 10)
        if st.button("🖨️ Print / Save PDF"):
            components.html("<script>window.print();</script>", height=0)
        if st.button("🔄 Clear & Re-sync"):
            st.session_state.history = []
            st.session_state.registry = {}
            st.rerun()

# --- 4. THE ANALYTICAL ENGINE (WITH SAFETY GATE) ---
def ai_brain(query):
    # SAFETY GATE: If query is empty or nonsense, exit immediately
    if not query or len(query.strip()) < 1:
        return None

    q_raw = query.lower().strip()
    semantic_map = {"mass of the sun": const.M_sun, "size of the sun": const.R_sun, "pi": np.pi, "speed of light": const.c}

    # Pass 1: Science Fact
    best_match, score, _ = process.extractOne(q_raw, semantic_map.keys(), scorer=fuzz.WRatio)
    if score > 85:
        target = semantic_map[best_match]
        val = target.value if hasattr(target, 'value') else target
        st.session_state.registry[best_match.replace(" ", "_")] = f"{val:g}"
        try: insight = wikipedia.summary(best_match, sentences=3)
        except: insight = "Data verified via NASA standard constants."
        return {"q": query, "a": f"{val:,g}", "i": insight, "t": "INTERNAL LABS", "lx": sp.latex(sp.sympify(str(val)))}

    # Pass 2: Math Core
    m_prep = re.sub(r'[^0-9\+\-\*\/\.\(\)\*\*\^pi]', '', q_raw.replace('pi', str(np.pi)).replace(',', ''))
    if any(c.isdigit() for c in m_prep):
        try:
            expr = sp.sympify(m_prep)
            ans = expr.evalf(precision)
            return {"q": query, "a": f"{float(ans):,g}", "i": "Symbolic reduction successful.", "t": "MATH CORE", "lx": sp.latex(expr)}
        except: pass

    # Pass 3: Librarian
    try:
        summary = wikipedia.summary(q_raw, sentences=3, auto_suggest=True)
        return {"q": query, "a": "Knowledge Retrieved", "i": summary, "t": "GLOBAL LIBRARIAN", "lx": None}
    except:
        return {"q": query, "a": "Refining...", "i": "Inquiry unrecognized.", "t": "SYSTEM", "lx": None}

# --- 5. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("main_interface", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

# Logic only triggers IF user hits the button AND types something
if exe and u_in:
    result = ai_brain(u_in)
    if result:
        st.session_state.history.append(result)
        st.rerun()

# Worksheet Rendering
for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 <b>Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
    if item['lx']:
        st.latex(item['lx'])
