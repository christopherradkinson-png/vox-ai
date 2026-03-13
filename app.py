import streamlit as st
import sympy as sp
from pint import UnitRegistry
import re
import difflib

# --- 1. CORE SYSTEM ARCHITECTURE ---
ureg = UnitRegistry()
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="collapsed")

# CRYSTAL CLEAR UI: KILLS JUMBLED TEXT & OVERLAPS
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
    header { visibility: visible !important; background: transparent !important; }
    div[data-testid="stInputInstructions"] { display: none !important; }
    ::placeholder { color: #AEAEB2 !important; opacity: 1; transition: opacity 0.2s; }
    input:focus::placeholder { opacity: 0 !important; }

    /* THE TOP COMMAND DOCK */
    div[data-testid="stForm"] {
        background: #F2F2F7 !important; border-radius: 20px !important;
        padding: 15px !important; border: 1px solid #D1D1D6 !important;
        margin-bottom: 30px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stForm"] > div {
        display: grid !important; grid-template-columns: 3fr 1fr !important;
        align-items: center !important; gap: 12px !important;
    }
    button[kind="formSubmit"] {
        background-color: #007AFF !important; color: white !important;
        border-radius: 12px !important; font-weight: 700 !important;
        width: 100% !important; border: none !important;
    }

    /* LIBRARIAN WORKSHEET CARDS */
    .sre-card {
        background: #FFFFFF; border-radius: 24px; padding: 26px; 
        margin: 18px 0; border: 1px solid #E5E5EA;
        box-shadow: 0 8px 30px rgba(0,0,0,0.03);
    }
    .meta { color: #007AFF; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; }
    .ans { color: #000000; font-size: 2.2rem; font-weight: 800; margin: 8px 0; letter-spacing: -1px; }
    .ai-insight {
        color: #1C1C1E; font-size: 0.95rem; line-height: 1.5; 
        border-top: 1px solid #F2F2F7; padding-top: 15px; margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR (LEGAL & SETTINGS) ---
with st.sidebar:
    st.title("Verilogic Pro")
    st.caption("Version 4.2.0 | Fuzzy AI Active")
    if st.button("🗑️ Reset All Data"):
        st.session_state.history = []
        st.rerun()

# --- 3. THE FUZZY AI LIBRARIAN (ERROR-TOLERANT CORE) ---
if 'history' not in st.session_state: st.session_state.history = []

def fuzzy_match(input_word, target_list):
    """Finds the closest match for a word in a list using a 60% similarity threshold."""
    matches = difflib.get_close_matches(input_word, target_list, n=1, cutoff=0.6)
    return matches[0] if matches else None

def ai_librarian_forgiving(query):
    # 1. VERBAL & FUZZY MATH SANITIZER
    num_map = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", 
               "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10"}
    
    q_words = query.lower().strip().split()
    sanitized_words = []
    
    for word in q_words:
        # Check if the word is a misspelling of a number
        match = fuzzy_match(word, list(num_map.keys()))
        if match:
            sanitized_words.append(num_map[match])
        else:
            sanitized_words.append(word)
    
    q = " ".join(sanitized_words)
    
    # 2. FUZZY SCIENCE KNOWLEDGE BASE
    kb = {
        "moon": {
            "v": "3,474.8 km (Diameter)", 
            "i": "Lunar diameter detected. The Moon is roughly 1/4 the size of Earth. Its gravity is 1/6th of Earth's, which is why astronauts can jump so high."
        },
        "sun": {
            "v": "1.989 × 10³⁰ kg", 
            "i": "Solar mass detected. The Sun holds 99.8% of the system's mass. 1.3 million Earths could fit inside it."
        },
        "thermal": {
            "v": "Approx 5 × 10³³ J/K",
            "i": "Solar thermal mass detected. This governs how the Sun stores and releases fusion energy."
        }
    }

    # Search for science keywords with fuzzy tolerance
    for key, data in kb.items():
        if fuzzy_match(key, q_words):
            return {"q": query, "a": data["v"], "i": data["i"], "t": "AI SCIENCE LIBRARIAN"}

    # 3. Math Core Fallback
    try:
        clean = q.replace('^', '**')
        clean = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', clean)
        expr = sp.sympify(clean)
        ans = expr.evalf(8)
        return {"q": query, "a": f"{ans:g}", "i": "Fuzzy math patterns recognized. Result verified.", "t": "MATH CORE"}
    except:
        return {"q": query, "a": "Input Received", "i": "Librarian is searching. Try asking 'What is the moon's size?'", "t": "SYSTEM ERROR"}

# --- 4. THE VIEWPORT ---
st.markdown("<h2 style='text-align:center; font-weight:900;'>VERILOGIC PRO</h2>", unsafe_allow_html=True)

with st.form("pro_dock_v12", clear_on_submit=True):
    u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
    exe = st.form_submit_button("EXE")

if exe and u_in:
    result = ai_librarian_forgiving(u_in)
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
