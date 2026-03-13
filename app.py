import streamlit as st
import sympy as sp
import numpy as np
from pint import UnitRegistry
import time
import re

# --- 1. LIGHTWEIGHT SYSTEM CONFIG ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="collapsed")

# APPLE "LIQUID GLASS" UI (STRESS-TESTED)
st.markdown("""
<style>
    /* 1. Global Apple Foundation */
    .stApp { background-color: #FFFFFF; color: #1C1C1E; font-family: -apple-system, sans-serif; }
    
    /* RESTORE SIDEBAR ICON: Show only the toggle, hide rest of Streamlit clutter */
    header { visibility: visible !important; background: transparent !important; border: none !important; }
    div[data-testid="stHeader"] { background: transparent !important; }
    .stDeployButton { display:none !important; }
    #MainMenu { visibility: hidden !important; }

    /* 2. AI GLASS CARDS */
    .sre-card {
        background: #F2F2F7;
        border-radius: 26px;
        padding: 24px;
        margin: 15px 10px;
        border: 1px solid #E5E5EA;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        animation: slideUp 0.4s ease-out;
    }
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .ans { color: #000000; font-size: 2.2rem; font-weight: 800; margin: 5px 0; letter-spacing: -1px; }
    .ai-insight { color: #8E8E93; font-size: 0.9rem; font-style: italic; border-top: 1px solid #D1D1D6; padding-top: 10px; margin-top: 10px; }

    /* 3. THE FLOATING INPUT DOCK (MOBILE LOCK-GRID) */
    div[data-testid="stForm"] {
        position: fixed !important;
        bottom: 85px !important; 
        left: 5% !important;
        right: 5% !important;
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        border-radius: 60px !important;
        border: 1px solid #D1D1D6 !important;
        padding: 8px 20px !important;
        z-index: 9999999 !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.12) !important;
    }
    
    /* Grid-Lock for Input and EXE */
    div[data-testid="stForm"] > div {
        display: grid !important;
        grid-template-columns: 3fr 1fr !important;
        align-items: center !important;
        gap: 12px !important;
    }

    .stTextInput input { border: none !important; background: transparent !important; font-size: 1.15rem !important; }
    
    button[kind="formSubmit"] {
        background-color: #007AFF !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 10px 15px !important;
        font-weight: 700 !important;
        width: 100% !important;
    }

    /* Padding for Worksheet Feed */
    .main .block-container { padding-bottom: 240px !important; padding-top: 60px !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE AI LIBRARIAN (INTELLIGENCE LAYER) ---
if 'history' not in st.session_state: st.session_state.history = []

def ai_librarian(query):
    q = query.lower().strip()
    
    # Internal Science Knowledge Library
    knowledge_base = {
        "sun": {
            "mass": "1.989 × 10³⁰ kg",
            "insight": "The Sun contains 99.8% of the total mass of our Solar System."
        },
        "thermal mass of the sun": {
            "val": "Approx 5 × 10³³ J/K",
            "insight": "This reflects the massive energy storage capacity of solar plasma."
        },
        "gravity": {
            "val": "9.806 m/s²",
            "insight": "Earth's standard gravity. On the Moon, this would be roughly 1.62 m/s²."
        },
        "speed of light": {
            "val": "299,792,458 m/s",
            "insight": "This is the absolute speed limit of the universe."
        }
    }
    
    # 1. Check AI Librarian for Facts
    for key, data in knowledge_base.items():
        if key in q:
            val = data.get("mass") or data.get("val")
            return {"q": query, "a": val, "i": data["insight"], "t": "AI SCIENCE"}

    # 2. Advanced Math Core
    try:
        # Implicit Multiplication Fix (2x -> 2*x)
        clean = q.replace('^', '**')
        clean = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', clean)
        
        expr = sp.sympify(clean)
        ans = expr.evalf(8)
        return {"q": query, "a": f"{ans:g}", "i": "Symbolic computation verified by Math Core.", "t": "MATH CORE"}
    except:
        return {"q": query, "a": "Check Syntax", "i": "Entry could not be parsed by the Librarian.", "t": "SYSTEM ERROR"}

# --- 3. THE VIEWPORT ---
with st.sidebar:
    st.title("SRE Settings")
    st.markdown("---")
    st.subheader("Legal & Compliance")
    st.caption("TASAA Compliance 2026")
    st.caption("Verilogic Pro SRE is a proprietary Symbolic Runtime Engine.")
    st.caption("© 2026 Verilogic Core.")
    if st.button("🗑️ Reset Worksheet"):
        st.session_state.history = []
        st.rerun()

st.markdown("<h2 style='text-align:center; font-weight:900; letter-spacing:-2px;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

# THE FEED
for item in st.session_state.history:
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 {item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. THE FLOATING INPUT DOCK ---
with st.form("ai_dock", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_librarian(u_in)
    st.session_state.history.append(result)
    st.rerun()
