import streamlit as st
import sympy as sp
import streamlit.components.v1 as components
import json

# 1. APPLE PRO & TEXAS COMPLIANCE (SB 2420 - 2026)
st.set_page_config(page_title="Verilogic Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. STATE & LOGIC
if "history" not in st.session_state: st.session_state.history = []
if "input" not in st.session_state: st.session_state.input = ""

def solve_math(val):
    if val == "AC": st.session_state.input = ""
    elif val == "=":
        if st.session_state.input:
            try:
                q = st.session_state.input.replace('×', '*').replace('÷', '/')
                expr = sp.sympify(q)
                res = float(expr.evalf())
                st.session_state.history.append({"q": st.session_state.input, "l": sp.latex(expr), "r": f"{res:,.4f}"})
                st.session_state.input = ""
            except: st.toast("Check Syntax")
    else:
        st.session_state.input += str(val)

# 3. SIDEBAR: ROBUST SETTINGS & TEXAS LEGAL JARGON
with st.sidebar:
    st.title("⚙️ System Hub")
    st.subheader("⚖️ Legal & Compliance")
    with st.expander("Texas App Store Act (2026)"):
        st.caption("Pursuant to SB 2420: This app is rated for ages 13+. No minor data is collected.")
    with st.expander("Texas Consumer Notice (DTPA)"):
        st.caption("VENUE: Disputes established in Texas. Tool provided 'as-is'.")
    with st.expander("Engineering Disclaimer"):
        st.error("STRICT LIABILITY: Not for life-critical structural use.")

# 4. NOTEBOOK CANVAS
st.markdown("""
    <style>
    .main { background-color: #fbfbfd; }
    [data-testid="stHeader"] { visibility: hidden; }
    .canvas { height: 40vh; overflow-y: auto; padding: 20px; background: white; border-radius: 20px; border-bottom: 2px solid #eee; }
    footer, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'<div style="border-left: 5px solid #007aff; padding: 15px; margin-bottom: 10px; background:#f9f9fb; border-radius:15px;">{st.latex(item["l"])}<div style="font-size:1.8rem; font-weight:800; color:#007aff;">= {item["r"]}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div style="padding:20px; border-left:5px solid #ff9f0a; font-size:1.8rem; background:#f2f2f7; border-radius:15px;"><b>{st.session_state.input or "0"}</b><span style="color:#ff9f0a;">|</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. THE IRONCLAD GRID (The Final Solution)
# This CSS Grid is physically impossible to stack vertically on mobile.
calc_html = """
<style>
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 15px; background: #f2f2f7; border-radius: 0 0 20px 20px; }
    button { height: 65px; border-radius: 15px; border: none; background: white; font-size: 1.4rem; font-weight: 600; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    button:active { background: #e5e5ea; transform: scale(0.95); }
    .op { background: #ff9f0a; color: white; }
    .eq { background: #007aff; color: white; }
    .ac { background: #a5a5a5; color: black; }
</style>
<div class="grid">
    <button class="ac" onclick="send('AC')">AC</button><button onclick="send('sqrt(')">√</button><button onclick="send('**2')">x²</button><button class="op" onclick="send('/')">÷</button>
    <button onclick="send('7')">7</button><button onclick="send('8')">8</button><button onclick="send('9')">9</button><button class="op" onclick="send('*')">×</button>
    <button onclick="send('4')">4</button><button onclick="send('5')">5</button><button onclick="send('6')">6</button><button class="op" onclick="send('-')">-</button>
    <button onclick="send('1')">1</button><button onclick="send('2')">2</button><button onclick="send('3')">3</button><button class="op" onclick="send('+')">+</button>
    <button onclick="send('0')">0</button><button onclick="send('.')">.</button><button onclick="send('pi')">π</button><button class="eq" onclick="send('=')">=</button>
</div>
<script>
    const send = (val) => { window.parent.postMessage({type: 'streamlit:setComponentValue', value: val}, '*'); };
</script>
"""

clicked = components.html(calc_html, height=420)
if clicked:
    solve_math(clicked)
    st.rerun()
