import streamlit as st
import sympy as sp
import re
st.set_page_config(page_title="Vox AI", page_icon="⚡")
class VERILOGIC_CORE:
def init(self):
self.reserved = ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'exp', 'pi']
def scrub(self, q):
q = "".join(i for i in q if ord(i) < 128).lower().strip()
q = q.replace(' ', '').replace('=', '')
for f in self.reserved:
q = q.replace(f, f"SHIELD_{f}")
q = re.sub(r"(\d)([a-z])", r"\1*\2", q) q = re.sub(r"()([a-z0-9(])", r"\1*\2", q)
for f in self.reserved:
q = q.replace(f"SHIELD_{f}", f)
q = q.replace('^', '**').rstrip('+-*/')
while q.count('(') > q.count(')'):
q += ')'
while q.count(')') > q.count('('):
q = '(' + q
return q
def brain(self, q):
try:
clean_q = self.scrub(q)
res = sp.simplify(sp.sympify(clean_q))
return str(res)
except:
return "ERROR: UNVERIFIABLE"
st.title("VOX AI: Verilogic-125")
if 'ai' not in st.session_state:
st.session_state.ai = VERILOGIC_CORE()
user_query = st.text_input("Enter Query (e.g. 5sin(pi/2)):")
if user_query:
result = st.session_state.ai.brain(user_query)
st.success(f"Result: {result}")
