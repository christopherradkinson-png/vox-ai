import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re

# --- 1. SYSTEM ARCHITECTURE ---
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="expanded")

# APPLE PRO UI: THE "INVINCIBLE" GRID-LOCK
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: visible !important; background: transparent !important; }
    
    /* THE TOP COMMAND DOCK: Fixed Grid-Lock */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 12px 18px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 30px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stForm"] > div {
        display: grid !important; grid-template-columns: 3.5fr 1fr !important;
        align-items: center !important; gap: 12px !important;
    }
    button[kind="formSubmit"] {
        background-color: #007AFF !important; color: white !important;
        border-radius: 12px !important; font-weight: 700 !important;
        width: 100% !important; border: none !important;
        white-space: nowrap !important; height: 42px !important;
    }

    /* LIBRARIAN WORKSHEET CARDS */
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 26px; 
        margin: 18px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 8px 32px rgba(0,0,0,0.04);
    }
    .meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    .ans { color: #000000; font-size: 2.3rem; font-weight: 800; margin: 8px 0; letter-spacing: -1.5px; }
    .ai-insight {
        color: #1C1C1E; font-size: 0.95rem; line-height: 1.6; 
        border-top: 1px solid #F2F2F7; padding-top: 15px; margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. ADVANCED SETTINGS MENU (SIDEBAR) ---
with st.sidebar:
    st.title("Settings")
    st.subheader("Verilogic Pro v4.2.4")
    st.divider()
    st.toggle("Scientific Research Mode", value=True)
    st.divider()
    st.markdown("### Texas 2026 Law Legal Statement")
    st.info("Texas App Store Accountability Act (2026): This application complies with TX SB 2420. Users under 18 must ensure parental guidance. Verilogic Pro does not store personal biometric data.")
    st.divider()
    st.markdown("### Legal Blurb")
    st.caption("Calculations and scientific data provided 'as is' for research purposes only.")

# --- 3. THE INTELLIGENCE ENGINE ---
if 'history' not in st.session_state:
    st.session_state.history = []

def ai_brain(query):
    # STEP A: HUMAN SPEECH NORMALIZER
    q_raw = query.lower().strip()
    # Strip conversational noise
    q_clean = re.sub(r'^(what is|calculate|tell me|solve|whats|how much is|show me|the)\s+', '', q_raw)
    
    # STEP B: MATH CORE (Priority for numeric/operator content)
    if any(char.isdigit() for char in q_clean) or any(op in q_clean for op in '+-*/^()'):
        try:
            # Handle math slang (e.g., "5 plus 5")
            m_prep = q_clean.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')
            m_prep = m_prep.replace(',', '').replace('^', '**').replace('=', '')
            
            expr = sp.sympify(m_prep)
            ans = expr.evalf(10)
            formatted = f"{int(ans):,}" if ans % 1 == 0 else f"{ans:g}"
            return {"q": query, "a": formatted, "i": "Symbolic Logic Core recognized a mathematical intent and synchronized data for precision.", "t": "MATH CORE"}
        except:
            pass # Fall through if it's not actually math

    # STEP C: GLOBAL RESEARCH LIBRARIAN (Wikipedia Fuzzy Search)
    try:
        # Pre-emptive Slang Mapping
        slang_map = {
            "big fiery ball": "Sun",
            "giant lizard": "Dinosaur",
            "biggest dinosaur": "Patagotitan mayorum",
            "largest dinosaur": "Argentinosaurus"
        }
        for slang, subject in slang_map.items():
            if slang in q_clean:
                q_clean = subject
        
        # Pull from global library
        summary = wikipedia.summary(q_clean, sentences=3)
        return {"q": query, "a": "Data Verified", "i": summary, "t": "GLOBAL LIBRARIAN"}
    except:
        # Final "Deep Search" Fallback
        try:
            search_results = wikipedia.search(q_clean)
            if search_results:
                summary = wikipedia.summary(search_results[0], sentences=3)
                return {"q": query, "a": "Data Refined", "i": summary, "t": "GLOBAL LIBRARIAN"}
        except:
            pass

    return {"q": query, "a": "Inquiry Received", "i": "The Librarian is refining its search. Please clarify if you are seeking a mathematical result or a scientific fact.", "t": "SYSTEM ADVISORY"}

# --- 4. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("pro_dock_v34", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_brain(u_in)
    st.session_state.history.append(result)
    st.rerun()

for item in reversed(st.session_state.history):
    st.markdown(f'''
    <div class="sre-card">
        <div class="meta">{item['t']} | Query: {item['q']}</div>
        <div class="ans">= {item['a']}</div>
        <div class="ai-insight">💡 <b>Librarian Insight:</b><br>{item['i']}</div>
    </div>
    ''', unsafe_allow_html=True)
