import streamlit as st
import google.generativeai as genai
import numpy as np
import plotly.graph_objects as go

# --- 1. BASIC UI ---
st.set_page_config(page_title="Verilogic Pro", layout="wide")

# --- 2. THE ENGINE (NO FRILLS, JUST THE BRIDGE) ---
def get_brain():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        # We use the direct model name. No beta, no experimental flags.
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Engine Connection Failure: {e}")
        return None

# --- 3. THE APP ---
st.title("🧬 Verilogic Pro")
query = st.text_area("What is your query?", height=150)

if st.button("Execute"):
    if query:
        model = get_brain()
        if model:
            with st.spinner("Processing..."):
                try:
                    # We bake the 'Show Your Work' into the prompt itself.
                    # No extra buttons to break.
                    prompt = f"Provide a step-by-step derivation for: {query}. Use LaTeX."
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Handshake Error: {e}")
    else:
        st.warning("Please enter a query.")

# --- 4. DIAGNOSTICS ---
with st.expander("System Info"):
    st.write("Status: Connected to Google Production v1")
