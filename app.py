import streamlit as st
import requests
import json
import numpy as np
import plotly.graph_objects as go

# --- 1. UI SETUP ---
st.set_page_config(page_title="Verilogic Pro", layout="wide")

# --- 2. THE ENGINE (MANUALLY CONSTRUCTED PIECE-BY-PIECE) ---
def call_google_ai(prompt_text):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "Error: Missing API Key in Secrets."
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    url = f"https://generativelanguage.googleapis.com{api_key}"
    
    # WE BUILD THE JSON MANUALLY TO PREVENT SYNTAX ERRORS
    parts_item = {"text": prompt_text}
    contents_item = {"parts": [parts_item]}
    payload = {"contents": [contents_item]}
    
    headers = {'Content-Type': 'application/json'}

    try:
        # We send the payload as a clean JSON object
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            return response_data['candidates'][0]['content']['parts'][0]
        else:
            return f"API Error: {response.status_code}"
    except Exception as e:
        return f"Connection Failed: {str(e)}"

# --- 3. MAIN INTERFACE ---
st.title("🧬 Verilogic Pro")
st.caption("v12.0 | Hand-Verified Stable")

user_query = st.text_area("Enter Math or Physics Query:", height=150)

if st.button("Execute Pro Logic"):
    if user_query:
        with st.spinner("Solving..."):
            # System instruction for "Show Your Work"
            full_prompt = f"Show your work step-by-step for: {user_query}. Use LaTeX."
            answer = call_google_ai(full_prompt)
            st.divider()
            st.markdown(answer)
    else:
        st.warning("Please enter a query.")

# --- 4. 3D GRAPHING ---
with st.expander("📈 3D Graphing Engine"):
    formula = st.text_input("Function (z=)", "np.sin(np.sqrt(X**2 + Y**2))")
    if st.button("Generate Graph"):
        try:
            x, y = np.linspace(-10, 10, 80), np.linspace(-10, 10, 80)
            X, Y = np.meshgrid(x, y)
            Z = eval(formula, {"np": np, "X": X, "Y": Y, "sqrt": np.sqrt, "sin": np.sin})
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Formula Error: {e}")
