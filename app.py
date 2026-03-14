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
    # Uses the key you saved in Streamlit Settings > Secrets
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # FIXED: Using gemini-1.5-flash to prevent the "NotFound" error
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("❌ API Key Missing or Invalid! Go to Settings > Secrets and add: GOOGLE_API_KEY = 'your_key'")
    st.stop()

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Verilogic Pro Engine", page_icon="🧬", layout="wide")
st.title("🧬 Verilogic Pro Engine v125.0")
st.markdown("---")

# --- 3. THE MULTI-TOOL SIDEBAR ---
menu = st.sidebar.selectbox("Select Engine Module", 
    ["AI Logic Center", "Market Analysis", "Advanced Math", "Visual Scanner"])

# --- MODULE: AI LOGIC CENTER ---
if menu == "AI Logic Center":
    st.subheader("🤖 AI Intelligence & Web Search")
    query = st.text_input("Enter complex query:", placeholder="Analyze the impact of...")
    
    if st.button("Execute Logic"):
        if query:
            with st.spinner("Processing..."):
                try:
                    # Attempting a quick Wikipedia context pull
                    wiki_summary = wikipedia.summary(query, sentences=2)
                    context = f"Context: {wiki_summary}\n\nUser Question: {query}"
                except:
                    context = query
                    
                response = model.generate_content(context)
                st.write(response.text)
        else:
            st.warning("Please enter a query first.")

# --- MODULE: MARKET ANALYSIS ---
elif menu == "Market Analysis":
    st.subheader("📈 Financial Data Engine")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, NVDA):", "AAPL")
    
    if st.button("Fetch Market Data"):
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1mo")
            if not data.empty:
                fig = px.line(data, y="Close", title=f"{ticker} Performance - Last 30 Days")
                st.plotly_chart(fig)
                st.dataframe(data.tail())
            else:
                st.error("Ticker not found or no data available.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

# --- MODULE: ADVANCED MATH ---
elif menu == "Advanced Math":
    st.subheader("🔢 Symbolic Math Solver")
    equation = st.text_input("Enter Equation (e.g., x**2 + 5*x + 6):", "x**2 + 5*x + 6")
    
    if st.button("Solve"):
        try:
            x = sympy.symbols('x')
            solution = sympy.solve(equation, x)
            st.success(f"Roots for {equation}: {solution}")
        except Exception as e:
            st.error(f"Math Error: {e}. Please use Python math syntax (e.g., * for multiply).")

# --- MODULE: VISUAL SCANNER ---
elif menu == "Visual Scanner":
    st.subheader("👁️ Image Intelligence")
    uploaded_file = st.file_uploader("Upload image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=400)
        if st.button("Deep Scan"):
            with st.spinner("Analyzing image..."):
                response = model.generate_content(["Analyze this image for patterns and data:", img])
                st.write(response.text)

st.sidebar.markdown("---")
st.sidebar.caption("System Status: **Active**")
st.sidebar.info("Model: Gemini 1.5 Flash")
