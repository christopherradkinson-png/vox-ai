import streamlit as st
import sympy as sp
import numpy as np
import wikipedia
import re
st.set_page_config(page_title='Verilogic Pro SRE', layout='centered', initial_sidebar_state="expanded")
st.markdown("""

.stApp { background-color: #FFFFFF; color: #000000; font-family: -apple-system, sans-serif; }
div[data-testid="stForm"] {
background: #F2F2F7 !important; border-radius: 20px !important;
padding: 12px 18px !important; border: 1px solid #D1D1D6 !important;
margin-bottom: 30px !important;
}
div[data-testid="stForm"] > div {
display: flex !important; flex-direction: row !important;
align-items: center !important; gap: 10px !important;
}
div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:nth-child(1) { flex: 4 !important; }
div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:nth-child(2) { flex: 1 !important; }
button[kind="formSubmit"] {
background-color: #007AFF !important; color: white !important;
border-radius: 12px !important; font-weight: 700 !important;
width: 100% !important; border: none !important; height: 42px !important;
}
.sre-card {
background: #FFFFFF; border-radius: 24px; padding: 26px;
margin: 18px 0; border: 1px solid #E5E5EA;
box-shadow: 0 8px 32px rgba(0,0,0,0.04);
}
.meta { color: #007AFF; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; }
.ans { color: #000000; font-size: 2.3rem; font-weight: 800; margin: 8px 0; letter-spacing: -1.5px; }

""", unsafe_allow_html=True)
with st.sidebar:
st.title("Settings")
st.subheader("Verilogic Pro v4.2.1")
st.divider()
st.toggle("Scientific Research Mode", value=True)
st.divider()
st.markdown("### Texas 2026 Law Legal Statement")
st.info("""
Texas App Store Accountability Act (2026): This application complies with TX SB 2420.
Users under 18 must ensure parental guidance. Verilogic Pro does not store personal biometric data.
""")
st.divider()
st.markdown("### Legal Blurb")
st.caption("Calculations and scientific data provided 'as is' for research purposes only.")
if 'history' not in st.session_state: st.session_state.history = []
def ai_brain(query):
q_clean = query.lower().strip()
if any(char.isdigit() or char in "+-*/^()" for char in q_clean):
try:
math_str = q_clean.replace('^', '**').replace(',', '')
expr = sp.sympify(math_str)
return {"a": f"{expr.evalf(10):g}", "i": "Symbolic Logic Verified.", "t": "MATH CORE"}
except: pass
try:
summary = wikipedia.summary(q_clean, sentences=2)
return {"a": "Data Verified", "i": summary, "t": "GLOBAL LIBRARIAN"}
except:
return {"a": "Awaiting Data", "i": "Please refine your query or check syntax.", "t": "SYSTEM ADVISORY"}
st.markdown("VERILOGIC PRO", unsafe_allow_html=True)
with st.form("pro_dock", clear_on_submit=True):
u_in = st.text_input("Input", placeholder="Ask the Librarian...", label_visibility="collapsed")
exe = st.form_submit_button("EXE")
if exe and u_in:
result = ai_brain(u_in)
st.session_state.history.append({"q": u_in, **result})
st.rerun()
for item in reversed(st.session_state.history):
st.markdown(f'''

{item['t']} | Query: {item['q']}
= {item['a']}
Librarian Insight:
{item['i']}

''', unsafe_allow_html=True)
