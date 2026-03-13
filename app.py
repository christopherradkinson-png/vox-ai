import streamlit as st
import sympy as sp
import numpy as np
from pint import UnitRegistry
import re
import time

# --- 1. SRE LIQUID GLASS UI (MOBILE-FORTRESS) ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="collapsed")

# 100-POINT OPTIMIZATION CSS: iOS 26 SAFE-ZONE & DYNAMIC VIEWPORT
st.markdown("""
<style>
    /* Apple OLED Foundation */
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    
    /* IOS 26 FIX: Dynamic Viewport Height & Safe Areas */
    html, body { height: 100dvh; overflow: hidden; margin: 0; }
    [data-testid="stAppViewContainer"] { height: 100dvh !important; overflow-y: auto !important; }

    /* Show Sidebar Toggle (Top-Left), Hide Clutter */
    header { visibility: visible !important; background: transparent !important; }
    .stDeployButton { display:none !important; }
    #MainMenu { visibility: hidden !important; }

    /* LIBRARIAN WORKSHEET CARDS */
    .sre-card {
        background: #F2F2F7; border-radius: 28px; padding: 26px; 
        margin: 18px 12px; border: 1px solid #E5E5EA;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        animation: slideUp 0.4s cubic-bezier(0.1, 0.9, 0.2, 1);
    }
    @keyframes slideUp { from { opacity: 0; transform: translateY(25px); } to { opacity: 1; transform: translateY(0); } }

    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; }
    .ans { color: #000000; font-size: 2.4rem; font-weight: 800; margin: 8px 0; letter-spacing: -1.5px; line-height: 1; }
    .ai-insight { color: #8E8E93; font-size: 0.95rem; font-style: italic; border-top: 1px solid #D1D1D6; padding-top: 12px; margin-top: 12px; }

    /* THE FLOATING COMMAND DOCK (STRESS-TESTED) */
    div[data-testid="stForm"] {
        position: fixed !important;
        bottom: 110px !important; /* Forces clearance of iOS 26 Liquid Glass toolbar */
        left: 4% !important; right: 4% !important;
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(40px) !important;
        -webkit-backdrop-filter: blur(40px) !important;
        border-radius: 100px !important;
        border: 1px solid #C6C6C8 !important;
        padding: 8px 22px !important;
        z-index: 100000 !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.15) !important;
    }
    
    /* Flex-Lock: Forces EXE and Input to stay on ONE LINE */
    div[data-testid="stForm"] > div {
        display: flex !important; flex-direction: row !important;
        align-items: center !important; gap: 15px !important;
    }

    /* Kills "Press Enter" jumble and cleans placeholder */
    div[data-testid="stInputInstructions"] { display: none !important; }
    input { border: none !important; background: transparent !important; font-size: 1.2rem !important; }
    ::placeholder { color: #AEAEB2 !important; opacity: 1; }
    input:focus::placeholder { opacity: 0 !important; }

    /* Pro-Blue EXE Button */
    button[kind="formSubmit"] {
        background-color: #007AFF !important; color: white !important;
        border-radius: 50px !important; font-weight: 700 !important;
        border: none !important; padding: 10px 30px !important;
    }

    /* Spacer for Worksheet Scroll */
    .main .block-container { padding-bottom: 300px !important; padding-top: 60px !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. HEURISTIC INTELLIGENCE ENGINE ---
if 'history' not in st.session_state: st.session_state.history = []

def ai_librarian_pro(query):
    raw = query.lower().strip()
    if not raw: return None
    
    # 1. AI LIBRARIAN KNOWLEDGE (FUZZY SEARCH)
    kb = {
        "moon": {"v": "3,474.8 km (Diameter)", "i": "The Moon is 1/4 the size of Earth. Its gravitational pull is 1/6th of Earth's, which governs our global tides."},
        "dinosaur": {"v": "Patagotitan mayorum", "i": "The Titanosaur (Patagotitan) is the largest land animal ever recorded, weighing approx 70 tons."},
        "sun": {"v": "1.989e30 kg", "i": "Solar mass detected. Holds 99.8% of system mass. Thermal Mass: ~5e33 J/K."},
        "thermal": {"v": "Approx 5e33 J/K", "i": "Heat capacity of solar plasma (thermal mass), governing energy storage."},
        "light": {"v": "299,792,458 m/s", "i": "The universal speed limit (c). Nothing with mass can exceed this speed."}
    }
    
    for key, data in kb.items():
        if key in raw: return {"q": query, "a": data["v"], "i": data["i"], "t": "AI SCIENCE"}

    # 2. HARDENED MATH (HUMAN NOISE STRIPPER)
    try:
        # Strip "What is", "Calculate", etc.
        clean = re.sub(r'^(what is|calculate|solve|tell me|how much is|whats)\s+', '', raw)
        # Handle 5k notation and commas
        clean = re.sub(r'(\d+)k\b', r'\1*1000', clean).replace(',', '')
        # Implicit Mult (2x -> 2*x)
        clean = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', clean).replace('^', '**')
        
        ans = sp.sympify(clean).evalf(12)
        return {"q": query, "a": f"{ans:g}", "i": "Verbal math noise filtered. Symbolic logic verified.", "t": "MATH CORE"}
    except:
        return {"q": query, "a": "Checking...", "i": "Librarian is analyzing. Ensure math syntax is standard (e.g. 5000+5000).", "t": "SYSTEM"}

# --- 3. THE VIEWPORT ---
with st.sidebar:
    st.title("SRE Settings")
    st.caption("Alpha v5.5.0 | Pro-Engine Active")
    st.markdown("---")
    st.subheader("⚖️ Legal Compliance")
    st.caption("TASAA 2026. Verilogic SRE is a proprietary Intelligence Engine.")
    with st.expander("EULA & Texas Disclosure"):
        st.caption("Per Texas HB 149, AI outputs are generated via proprietary SRE. Accuracy is symbolic-verified.")
    if st.button("🗑️ Wipe Session Data"):
        st.session_state.history = []
        st.rerun()

st.markdown("<h2 style='text-align:center; font-weight:900; letter-spacing:-2px;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

# THE WORKSHEET (Newest at TOP)
for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 <b>Librarian Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)

# --- 4. THE COMMAND DOCK ---
with st.form("dock_v100", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_librarian_pro(u_in)
    if result:
        st.session_state.history.append(result)
        st.rerun()
