import streamlit as st
import sympy as sp
import re
st.set_page_config(page_title="Verilogic-125 SRE", layout="centered")
st.markdown(""".stApp {background-color: #0e1117; color: #ffffff;} .main-title {text-align: center; color: #4b90ff; font-family: monospace; font-weight: bold; font-size: 1.8rem;} .stTextInput>div>div>input {background-color: #1a1c23; color: #00ffcc; border: 2px solid #4b90ff; text-align: center;}VERILOGIC-125 CORE SRE""", unsafe_allow_html=True)
st.sidebar.title("SETTINGS")
st.sidebar.write("Verilogic-125: Vision, Voice, AI Assist.")
query = st.text_input("ENTER QUERY:", placeholder="Type math or theory...")
col1, col2 = st.columns(2)
up = col2.file_uploader("SCAN", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
try:
q_clean = query.lower().strip().replace(' ','')
if q_clean == 'p=np': st.info("AI ASSIST: P vs NP is a Millennium Prize Problem. Currently Unsolved.")
if '=' in query:
l, r = query.split('=')
res = str(sp.solve(sp.Eq(sp.sympify(l.strip()), sp.sympify(r.strip()))))
st.success("MATH RESULT: " + res)
elif query:
res = str(sp.simplify(sp.sympify(query)))
st.success("MATH RESULT: " + res)
except:
st.error("SYNTAX ERROR: Use * for multiply (e.g. 4*x)")
