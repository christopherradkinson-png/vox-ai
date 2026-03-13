import streamlit as st
import sympy as sp
from pint import UnitRegistry
import re

# --- 1. CORE SYSTEM STABILITY ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro', layout='centered', initial_sidebar_state="collapsed")

# APPLE PRO UI: TOP-DOCK ARCHITECTURE (STOPS THE FLASH-BUG)
st.markdown("""
<style>
    /* Global Apple Foundation */
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: visible !important; background: transparent !important; }
    .stDeployButton { display:none !important; }

    /* THE TOP COMMAND DOCK (Million-Dollar Fix) */
    /* Moving input to top prevents the iOS keyboard from breaking the render cycle */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        border: 1px solid #D1D1D6 !important;
        margin-bottom: 30px !important;
    }
    div[data-testid="stForm"] > div {
        display: grid !important;
        grid-template-columns: 3fr 1fr !important;
        align-items: center !important;
        gap: 10px !important;
    }

    /* EXE BUTTON */
    button[kind="formSubmit"] {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        width: 100% !important;
    }

    /* LIBRARIAN CARDS */
    .sre-card {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 24px;
        margin: 15px 0;
        border: 1px solid #E5E5EA;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .meta { color: #007AFF; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
    .ans { color: #000000; font-size: 2rem; font-weight: 700; margin: 5px 0; }
    .ai-insight { color: #8E8E93; font-size: 0.9rem; font-style: italic; border-top: 1px solid #F2F2F7; padding-top: 10px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 2. PERSISTENT KNOWLEDGE ENGINE ---
if 'history' not in st.session_state:
    st.session_state.history = []

def ai_librarian(query):
    q = query.lower().strip()
    kb = {
        "sun": {"v": "1.989 × 10³⁰ kg", "i": "The Sun contains 99.8% of the Solar System's mass."},
        "thermal": {"v": "Approx 5 × 10³³ J/K", "i": "Solar plasma thermal mass (heat capacity)."},
        "gravity": {"v": "9.806 m/s²", "i": "Earth standard gravity. Mars is 3.72 m/s²."},
        "speed of light": {"v": "299,792,458 m/s", "i": "The universal speed limit."}
    }

    for key, data in kb.items():
        if key in q: return {"q": query, "a": data["v"], "i": data["i"], "t": "AI SCIENCE"}

    try:
        clean = q.replace('^', '**')
        clean = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', clean)
        ans = sp.sympify(clean).evalf(8)
        return {"q": query, "a": f"{ans:g}", "i": "Mathematical pattern verified.", "t": "MATH CORE"}
    except:
        return {"q": query, "a": "Checking...", "i": "Syntactical anomaly. Try standard math (e.g. 5+5).", "t": "SYSTEM"}

# --- 3. VIEWPORT ---
with st.sidebar:
    st.title("SRE Settings")
    if st.button("🗑️ Reset All"):
        st.session_state.history = []
        st.rerun()

st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

# --- 4. THE COMMAND DOCK (TOP OF SCREEN) ---
with st.form("top_dock", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    # Proactive Calculation: Done before rendering the feed
    result = ai_librarian(u_in)
    st.session_state.history.append(result)
    st.rerun()

# --- 5. THE HISTORY FEED (STABLE) ---
for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 {item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
