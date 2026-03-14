import streamlit as st
import google.generativeai as genai
import yfinance as yf
import pandas as pd
import plotly.express as px
from PIL import Image
import wikipedia
import sympy
from fpdf import FPDF

# --- 1. THE VAULT HANDSHAKE ---
try:
    # Pulls your existing key from the Streamlit Vault
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # THE FIX: Using the stable model name to stop the 404 error
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("❌ API Key Error: Check your Streamlit Secrets Vault.")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Verilogic Pro Engine", page_icon="🧬", layout="wide")
st.title("🧬 Verilogic Pro Engine v125.0")

# --- 3. THE MULTI-TOOL SIDEBAR ---
menu = st.sidebar.selectbox("Select Engine Module", 
    ["AI Logic Center", "Market Analysis", "Advanced Math", "Visual Scanner"])

# --- MODULE: AI LOGIC CENTER ---
if menu == "AI Logic Center":
    st.subheader("🤖 AI Intelligence")
    query = st.text_input("Enter your request:", placeholder="Ask anything...")
    
    if st.button("Execute Logic"):
        if query:
            with st.spinner("🧠 Thinking..."):
                try:
                    response = model.generate_content(query)
                    st.markdown("### Engine Output:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"📡 Connection Issue: {e}")
        else:
            st.warning("Please enter a query.")

# --- MODULE: MARKET ANALYSIS ---
elif menu == "Market Analysis":
    st.subheader("📈 Financial Data Engine")
    ticker = st.text_input("Ticker Symbol:", "NVDA")
    if st.button("Fetch Data"):
        try:
            data = yf.Ticker(ticker).history(period="1mo")
            if not data.empty:
                st.plotly_chart(px.line(data, y="Close", title=f"{ticker} Trends"))
            else:
                st.error("Ticker not found.")
        except:
            st.error("Finance Engine Error.")

# --- MODULE: ADVANCED MATH ---
elif menu == "Advanced Math":
    st.subheader("🔢 Math Solver")
    eq = st.text_input("Equation:", "x**2 - 4")
    if st.button("Solve"):
        try:
            x = sympy.symbols('x')
            st.success(f"Roots: {sympy.solve(eq, x)}")
        except:
            st.error("Math Syntax Error.")

# --- MODULE: VISUAL SCANNER ---
elif menu == "Visual Scanner":
    st.subheader("👁️ Image Intelligence")
    file = st.file_uploader("Upload...", type=["jpg", "png"])
    if file and st.button("Scan"):
        img = Image.open(file)
        st.image(img, width=300)
        with st.spinner("Scanning..."):
            res = model.generate_content(["Describe this image:", img])
            st.write(res.text)

st.sidebar.markdown("---")
st.sidebar.caption("System Status: **Online**")
