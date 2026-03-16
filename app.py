import streamlit as st
import google.generativeai as genai

# --- 1. MINIMAL UI ---
st.set_page_config(page_title="Verilogic Pro", layout="centered")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 10px !important; }
    .stButton > button { width: 100%; background-color: #007AFF; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE STABLE ENGINE ---
def get_brain():
    try:
        # Pull API key from Streamlit secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # We call the model name directly without any 'v1beta' flags
        # This fixes the 404 error by hitting the stable production bridge
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Engine Failure: {e}")
        return None

# --- 3. MAIN APP ---
st.title("🧬 Verilogic Pro")

user_input = st.text_area("What is your query?", placeholder="e.g., What is the size of the sun?", height=150)

if st.button("Execute"):
    if user_input:
        model = get_brain()
        if model:
            with st.spinner("Processing on Production Bridge..."):
                try:
                    # We bake 'Show Your Work' into the core prompt
                    prompt = f"System: You are Verilogic Pro. Provide a step-by-step 'Show Your Work' derivation for: {user_input}. Use LaTeX for all math."
                    
                    response = model.generate_content(prompt)
                    
                    st.divider()
                    if response.text:
                        st.markdown(response.text)
                    else:
                        st.warning("Empty response. Please check API quota.")
                except Exception as e:
                    # This catches the 404 error if the library isn't updated
                    st.error(f"Handshake Error: {e}")
                    st.info("If 404 persists, Reboot the app in the Streamlit Dashboard to clear the cache.")
    else:
        st.warning("Please enter a query.")
