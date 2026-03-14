import streamlit as st
import google.generativeai as genai
import yfinance as yf
import pandas as pd
import plotly.express as px
from PIL import Image
import wikipedia
import sympy
from fpdf import FPDF
import requests

# --- 1. THE VAULT HANDSHAKE ---
try:
    # Use the key from your Streamlit Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Using the most stable model version
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("🔑 API Key Missing in Secrets! Please add GOOGLE_API_KEY to your Vault.")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Verilogic Pro Engine", page_icon="🧬", layout="wide")
st.title("🧬 Verilogic Pro Engine v125.0")

# --- 3. THE MULTI-TOOL SIDEBAR ---
menu = st.sidebar.selectbox("Select Engine Module", 
    ["AI Logic Center", "Market Analysis", "Advanced Math", "Visual Scanner"])

# --- MODULE: AI LOGIC CENTER (REPAIRED) ---
if menu == "AI Logic Center":
    st.subheader("🤖 AI Intelligence")
    query = st.text_input("Enter your request:", placeholder="Analyze...")
    
    if st.button("Execute Logic"):
        if query:
            with st.spinner("Connecting to Brain..."):
                try:
                    # The "Safety Shield" call
                    response = model.generate_content(query)
                    st.markdown("### Engine Output:")
                    st.write(response.text)
                except Exception as e:
                    # This catches the long error in your photo and explains it
                    st.error(f"📡 Connection Error: Google's server is busy or the API key is still 'warming up'. Try again in 10 seconds.")
                    st.info(f"Technical Detail: {e}")
        else:
            st.warning("Please enter a query.")

# --- MODULE: MARKET ANALYSIS ---
elif menu == "Market Analysis":
    st.subheader("📈 Financial Data Engine")
    ticker = st.text_input("Ticker:", "NVDA")
    if st.button("Fetch"):
        data = yf.Ticker(ticker).history(period="1mo")
        st.plotly_chart(px.line(data, y="Close"))

# --- MODULE: ADVANCED MATH ---
elif menu == "Advanced Math":
    st.subheader("🔢 Math Solver")
    eq = st.text_input("Equation:", "x**2 + 5*x + 6")
    if st.button("Solve"):
        x = sympy.symbols('x')
        st.success(f"Result: {sympy.solve(eq, x)}")

# --- MODULE: VISUAL SCANNER ---
elif menu == "Visual Scanner":
    st.subheader("👁️ Image Intelligence")
    file = st.file_uploader("Upload...", type=["jpg", "png"])
    if file and st.button("Scan"):
        img = Image.open(file)
        res = model.generate_content(["Describe this:", img])
        st.write(res.text)

st.sidebar.markdown("---")
st.sidebar.caption("Status: **System Ready**")
