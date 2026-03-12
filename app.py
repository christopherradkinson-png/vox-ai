import streamlit as st
from streamlit_elements import elements, mui, html, dashboard
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import io, base64

# 1. PAGE CONFIG
st.set_page_config(page_title="Verilogic Pro", layout="wide", initial_sidebar_state="collapsed")

# 2. STATE MANAGER
if "input" not in st.session_state: st.session_state.input = ""
if "layout" not in st.session_state:
    st.session_state.layout = [
        dashboard.Item("header", 0, 0, 12, 1, isResizable=False),
        dashboard.Item("display", 0, 1, 12, 2, isResizable=False),
        dashboard.Item("graph", 0, 3, 8, 5),
        dashboard.Item("work", 8, 3, 4, 5),
        dashboard.Item("btn_7", 0, 8, 3, 1), dashboard.Item("btn_8", 3, 8, 3, 1), dashboard.Item("btn_9", 6, 8, 3, 1), dashboard.Item("btn_div", 9, 8, 3, 1),
        dashboard.Item("btn_4", 0, 9, 3, 1), dashboard.Item("btn_5", 3, 9, 3, 1), dashboard.Item("btn_6", 6, 9, 3, 1), dashboard.Item("btn_mul", 9, 9, 3, 1),
        dashboard.Item("btn_1", 0, 10, 3, 1), dashboard.Item("btn_2", 3, 10, 3, 1), dashboard.Item("btn_3", 6, 10, 3, 1), dashboard.Item("btn_sub", 9, 10, 3, 1),
        dashboard.Item("btn_0", 0, 11, 3, 1), dashboard.Item("btn_dot", 3, 11, 3, 1), dashboard.Item("btn_eq", 6, 11, 3, 1), dashboard.Item("btn_add", 9, 11, 3, 1),
    ]

# 3. AI LOGIC ENGINE
def process_logic(query):
    if not query: return "0", "Ready", None
    try:
        q_clean = query.replace('×', '*').replace('÷', '/')
        expr = sp.sympify(q_clean)
        
        # Variable vs Number Logic
        eval_res = expr.evalf()
        res = str(round(float(eval_res), 4)) if eval_res.is_Number else str(expr)
        
        # Plotting Engine
        fig, ax = plt.subplots(figsize=(5,3), facecolor='black')
        x_vals = np.linspace(-10, 10, 200)
        try:
            f = sp.lambdify(sp.Symbol('x'), expr, 'numpy')
            ax.plot(x_vals, f(x_vals), color='#0a84ff', linewidth=2.5)
        except:
            ax.text(0.5, 0.5, f"Value: {res}", color='#0a84ff', ha='center', fontsize=14)
            
        ax.set_facecolor('black')
        ax.grid(color='#222', linestyle='-')
        ax.tick_params(colors='#666', labelsize=8)
        for spine in ax.spines.values(): spine.set_visible(False)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        plot_data = base64.b64encode(buf.getvalue()).decode()
        plt.close(fig) 
        return res, f"Analysis: {res}", f"data:image/png;base64,{plot_data}"
    except:
        return "Error", "Awaiting valid input...", None

def handle_click(val):
    if val == "=":
        res, _, _ = process_logic(st.session_state.input)
        if res != "Error": st.session_state.input = res
    else:
        st.session_state.input += str(val)

# 4. INTERFACE
with elements("verilogic_pro"):
    with dashboard.Grid(st.session_state.layout, draggable=True, resizable=True, rowHeight=60):
        
        with mui.Paper(key="header", sx={"display":"flex","alignItems":"center","padding":"0 20px","bgcolor":"#000","color":"#FFF","borderRadius":"15px 15px 0 0"}):
            mui.Typography("VERILOGIC PRO", sx={"fontWeight":"900","letterSpacing":"1.5px","flexGrow":1})
            mui.Button("RESET", size="small", onClick=lambda: st.session_state.update({"input": ""}), sx={"color":"#ff3b30"})

        with mui.Paper(key="display", sx={"display":"flex","justifyContent":"flex-end","alignItems":"center","padding":"20px","bgcolor":"#1c1c1e","color":"white"}):
            mui.Typography(st.session_state.input or "0", variant="h2")

        res_val, logic_text, plot_img = process_logic(st.session_state.input)

        with mui.Paper(key="graph", sx={"bgcolor":"#000","overflow":"hidden","display":"flex","justifyContent":"center"}):
            if plot_img: html.img(src=plot_img, style={"height":"100%","width":"auto"})
            else: mui.Typography("Enter Equation", sx={"color":"#333","mt":"20%"})

        with mui.Paper(key="work", sx={"padding":"20px","bgcolor":"#1c1c1e","borderLeft":"2px solid #0a84ff"}):
            mui.Typography("AI LIBRARIAN", variant="overline", sx={"color":"#0a84ff"})
            mui.Typography(logic_text, variant="h6", sx={"color":"#FFF"})

        # Keypad
        btns = [
            ("7","btn_7"), ("8","btn_8"), ("9","btn_9"), ("÷","btn_div"),
            ("4","btn_4"), ("5","btn_5"), ("6","btn_6"), ("×","btn_mul"),
            ("1","btn_1"), ("2","btn_2"), ("3","btn_3"), ("-","btn_sub"),
            ("0","btn_0"), (".","btn_dot"), ("=","btn_eq"), ("+","btn_add")
        ]
        for label, key in btns:
            bg = "#333" if label not in ["÷","×","-","+","="] else "#ff9f0a"
            if label == "=": bg = "#34c759"
            with mui.Button(key=key, variant="contained", onClick=lambda x=label: handle_click(x), sx={"bgcolor":bg, "borderRadius":"12px"}):
                mui.Typography(label)
