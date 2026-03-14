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
    # This connects to the GOOGLE_API_KEY you saved in Settings > Secrets
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("❌ API Key Missing! Go to Settings > Secrets and add: GOOGLE_API_KEY = 'your_key'")
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
        with st.spinner("Processing..."):
            # Combine AI with a Wikipedia context check
            try:
                wiki_summary = wikipedia.summary(query, sentences=2)
                context = f"Context: {wiki_summary}\n\nUser Question: {query}"
            except:
                context = query
                
            response = model.generate_content(context)
            st.write(response.text)

# --- MODULE: MARKET ANALYSIS ---
elif menu == "Market Analysis":
    st.subheader("📈 Financial Data Engine")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, NVDA):", "AAPL")
    
    if st.button("Fetch Market Data"):
        data = yf.Ticker(ticker).history(period="1mo")
        fig = px.line(data, y="Close", title=f"{ticker} Performance - Last 30 Days")
        st.plotly_chart(fig)
        st.dataframe(data.tail())

# --- MODULE: ADVANCED MATH ---
elif menu == "Advanced Math":
    st.subheader("🔢 Symbolic Math Solver")
    equation = st.text_input("Enter Equation (e.g., x**2 + 2*x + 1):", "x**2 + 5*x + 6")
    
    if st.button("Solve"):
        x = sympy.symbols('x')
        solution = sympy.solve(equation, x)
        st.success(f"Roots for {equation}: {solution}")

# --- MODULE: VISUAL SCANNER ---
elif menu == "Visual Scanner":
    st.subheader("👁️ Image Intelligence")
    uploaded_file = st.file_uploader("Upload image...", type=["jpg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=400)
        if st.button("Deep Scan"):
            response = model.generate_content(["Analyze this image for patterns and data:", img])
            st.write(response.text)

st.sidebar.markdown("---")
st.sidebar.caption("System Status: **Active**")
