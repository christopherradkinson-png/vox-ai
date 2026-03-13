import streamlit as st
import sympy as sp
import streamlit.components.v1 as components

# 1. CORE CONFIG
st.set_page_config(page_title="Verilogic Pro", layout="centered")

# 2. THE NOTEBOOK CANVAS (Standard Streamlit for History)
st.markdown("""
    <style>
    .main { background-color: #fbfbfd; font-family: -apple-system, sans-serif; }
    [data-testid="stHeader"] { visibility: hidden; }
    .canvas { height: 45vh; overflow-y: auto; padding: 20px; border-bottom: 2px solid #e5e5ea; background: white; }
    .entry { border-left: 5px solid #007aff; padding-left: 15px; margin-bottom: 20px; }
    footer, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history = []
if "input_buffer" not in st.session_state: st.session_state.input_buffer = ""

# 3. MATH ENGINE
def solve():
    if not st.session_state.input_buffer: return
    try:
        q = st.session_state.input_buffer.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(q)
        res = float(expr.evalf())
        st.session_state.history.append({"q": st.session_state.input_buffer, "l": sp.latex(expr), "r": f"{res:,.4f}"})
        st.session_state.input_buffer = ""
    except: st.toast("Check Syntax")

# 4. HISTORY DISPLAY
st.markdown('<div class="canvas">', unsafe_allow_html=True)
for item in reversed(st.session_state.history):
    st.markdown(f'<div class="entry"><small style="opacity:0.3;">{item["q"]}</small><br>{st.latex(item["l"])}<br><b style="color:#007aff; font-size:1.6rem;">= {item["r"]}</b></div>', unsafe_allow_html=True)
st.markdown(f'<div style="padding:15px; border-left:5px solid #ff9f0a; font-size:1.5rem; background:#f2f2f7; border-radius:10px;"><b>{st.session_state.input_buffer or "0"}</b><span style="color:#ff9f0a;">|</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. THE IRONCLAD HTML KEYBOARD (Bypasses Streamlit Layout)
# This raw HTML creates a grid that CANNOT stack.
calc_html = """
<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        padding: 15px;
        background-color: #f2f2f7;
        border-radius: 0 0 20px 20px;
    }
    button {
        height: 60px;
        border-radius: 12px;
        border: none;
        background-color: white;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    button:active { background-color: #d1d1d6; }
    .op { background-color: #ff9f0a; color: white; }
    .ac { background-color: #a5a5a5; color: black; }
</style>

<div class="grid-container">
    <button class="ac" onclick="send('AC')">AC</button>
    <button onclick="send('sqrt(')">√</button>
    <button onclick="send('**2')">x²</button>
    <button class="op" onclick="send('/')">÷</button>
    <button onclick="send('7')">7</button><button onclick="send('8')">8</button><button onclick="send('9')">9</button>
    <button class="op" onclick="send('*')">×</button>
    <button onclick="send('4')">4</button><button onclick="send('5')">5</button><button onclick="send('6')">6</button>
    <button class="op" onclick="send('-')">-</button>
    <button onclick="send('1')">1</button><button onclick="send('2')">2</button><button onclick="send('3')">3</button>
    <button class="op" onclick="send('+')">+</button>
    <button onclick="send('0')">0</button><button onclick="send('.')">.</button><button onclick="send('pi')">π</button>
    <button class="op" style="background-color:#007aff" onclick="send('=')">=</button>
</div>

<script>
    function send(val) {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: val}, '*');
    }
</script>
"""

# Render the custom keyboard and listen for clicks
clicked_key = components.html(calc_html, height=400)

if clicked_key:
    if clicked_key == "AC": 
        st.session_state.input_buffer = ""
    elif clicked_key == "=": 
        solve()
    else: 
        st.session_state.input_buffer += clicked_key
    st.rerun()
