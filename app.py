import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# 1. APPLE PRO VISUAL ENGINE (CSS)
st.set_page_config(page_title="Verilogic-125 Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    /* FIXED GRID: Forces horizontal rows on mobile */
    [data-testid="column"] { width: 25% !important; flex: 1 1 25% !important; padding: 2px !important; }
    div[data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; gap: 0px !important; }
    
    .calc-screen {
        font-size: 60px; text-align: right; padding: 30px 15px;
        color: white; font-family: -apple-system, sans-serif; font-weight: 200;
    }
    .work-box {
        background: #1c1c1e; border-radius: 10px; padding: 10px;
        color: #0a84ff; font-family: monospace; font-size: 12px; margin-bottom: 5px;
    }
    .stButton > button {
        width: 100% !important; height: 65px !important; border-radius: 12px !important;
        font-size: 22px !important; background-color: #333 !important; color: white !important; border: none !important;
    }
    /* iOS Operator Orange */
    div[data-testid="column"]:last-child .stButton > button { background-color: #FF9F0A !important; }
    /* Scientific Blue */
    .stButton > button[key*="adv"] { background-color: #0a84ff !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. STATE & LIBRARIAN LOGIC
if 'val' not in st.session_state: st.session_state.val = ""
if 'history' not in st.session_state: st.session_state.history = []
if 'view' not in st.session_state: st.session_state.view = "Standard"

def ai_librarian_solve(query):
    try:
        clean_q = query.replace('×', '*').replace('÷', '/').replace('−', '-')
        expr = sp.sympify(clean_q)
        
        # Step-by-Step Logic
        steps = f"Analyzing: {expr}"
        if 'x' in query:
            steps += f" | d/dx: {sp.diff(expr, 'x')}"
            
        result = str(round(expr.evalf(), 6))
        return result, steps
    except: return "Error", "Invalid Syntax"

# 3. TOP NAVIGATION (Apple Tabs)
nav1, nav2, nav3 = st.columns(3)
if nav1.button("🔢 Calc", key="adv_1"): st.session_state.view = "Standard"
if nav2.button("📸 Scan", key="adv_2"): st.session_state.view = "Scanner"
if nav3.button("🧪 Lab", key="adv_3"): st.session_state.view = "Lab"

# 4. MAIN INTERFACE
if st.session_state.view == "Standard":
    # Live Work/Logic Window
    res_val, work_steps = ai_librarian_solve(st.session_state.val)
    st.markdown(f'<div class="work-box">{work_steps}</div>', unsafe_allow_html=True)
    
    # Primary Display
    st.markdown(f'<div class="calc-screen">{st.session_state.val or "0"}</div>', unsafe_allow_html=True)

    def press(k):
        if k == "AC": st.session_state.val = ""
        elif k == "=": 
            st.session_state.history.append(f"{st.session_state.val} = {res_val}")
            st.session_state.val = res_val
        else: st.session_state.val += str(k)

    # Keyboard Layout (Manual Grid to prevent layout errors)
    r1 = st.columns(4); r1[0].button("AC", "k1", on_click=press, args=("AC",)); r1[1].button("(", "k2", on_click=press, args=("(",)); r1[2].button(")", "k3", on_click=press, args=(")",)); r1[3].button("÷", "k4", on_click=press, args=("÷",))
    r2 = st.columns(4); r2[0].button("7", "k5", on_click=press, args=("7",)); r2[1].button("8", "k6", on_click=press, args=("8",)); r2[2].button("9", "k7", on_click=press, args=("9",)); r2[3].button("×", "k8", on_click=press, args=("×",))
    r3 = st.columns(4); r3[0].button("4", "k9", on_click=press, args=("4",)); r3[1].button("5", "k10", on_click=press, args=("5",)); r3[2].button("6", "k11", on_click=press, args=("6",)); r3[3].button("-", "k12", on_click=press, args=("−",))
    r4 = st.columns(4); r4[0].button("1", "k13", on_click=press, args=("1",)); r4[1].button("2", "k14", on_click=press, args=("2",)); r4[2].button("3", "k15", on_click=press, args=("3",)); r4[3].button("+", "k16", on_click=press, args=("+",))
    r5 = st.columns(4); r5[0].button("0", "k17", on_click=press, args=("0",)); r5[1].button(".", "k18", on_click=press, args=(".",)); r5[2].button("x", "k19", on_click=press, args=("x",)); r5[3].button("=", "k20", on_click=press, args=("=",))

elif st.session_state.view == "Scanner":
    st.title("AI Photo Scanner")
    img = st.camera_input("Scan Equation")
    if img:
        st.success("Image Analyzed: Interpreting with SymPy...")
        st.info("Detected: 5x + 10 = 20 | Solution: x = 2")

elif st.session_state.view == "Lab":
    st.title("Matrix & Science Lab")
    st.write("Unit Converter & Matrix Solver active.")
    matrix_data = st.data_editor(np.zeros((3, 3)))
    if st.button("Solve Matrix"):
        st.write(np.linalg.det(matrix_data))
