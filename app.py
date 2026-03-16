import streamlit as st
import google.generativeai as genai

# --- 1. UI SETUP (CLEAN & FUNCTIONAL) ---
st.set_page_config(page_title="Verilogic Pro", layout="centered")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 12px !important; border: 1px solid #d1d1d6 !important; }
    .stButton > button { 
        background-color: #007AFF; color: white; border-radius: 10px; 
        width: 100%; font-weight: 600; border: none; padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE SETUP (FORCING PRODUCTION V1) ---
def get_brain():
    try:
        # Pull API key from Streamlit secrets
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("Missing GOOGLE_API_KEY in Secrets.")
            return None
            
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # We use the standard model name. This forces the library 
        # to use the 'v1' production path and bypass the 404 Beta error.
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Engine Failure: {e}")
        return None

# --- 3. MAIN INTERFACE ---
st.title("🧬 Verilogic Pro")

user_query = st.text_area("What is your query?", placeholder="e.g., Size of the sun...", height=150)

if st.button("Execute"):
    if user_query:
        model = get_brain()
        if model:
            with st.spinner("Connecting to Production Engine..."):
                try:
                    # We bake the 'Show Your Work' instructions directly into the prompt.
                    # This ensures it works without breaking the API handshake.
                    prompt = f"System: You are Verilogic Pro. Provide a step-by-step 'Show Your Work' derivation for: {user_query}. Use LaTeX."
                    
                    response = model.generate_content(prompt)
                    
                    st.divider()
                    if response.text:
                        st.markdown(response.text)
                    else:
                        st.warning("The engine returned an empty response. Check API quota.")
                except Exception as e:
                    # This catches that 404 error if the server cache isn't cleared
                    st.error(f"Handshake Error: {e}")
                    st.info("CRITICAL: Go to Streamlit Dashboard -> Manage App -> Reboot App.")
    else:
        st.warning("Please provide a query.")
