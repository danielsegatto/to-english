import streamlit as st
from litellm import completion
import json
import os

# --- APP CONFIGURATION ---
# Ensure your GROQ_API_KEY is set in GitHub Codespaces Secrets
api_key = os.environ.get("GROQ_API_KEY")

# --- PERMANENT PROMPT SETTINGS ---
# You can adjust these instructions right here in the code
SYSTEM_PROMPT = """
You are a professional translator. Provide 3 distinct English translations for the text provided.
Return ONLY a JSON object with exactly these keys:
- "v1": Formal and professional (for business/official use).
- "v2": Natural and idiomatic (how a native speaker actually talks).
- "v3": Creative or poetic (captures the mood and artistic essence).

Text to translate: {text}
"""

def get_translations(source_text):
    """
    Sends the hard-coded prompt to GPT-OSS-120B and returns the JSON result.
    """
    # Inject the user's text into our permanent prompt
    formatted_prompt = SYSTEM_PROMPT.format(text=source_text)
    
    try:
        response = completion(
            model="groq/openai/gpt-oss-120b",
            messages=[{"role": "user", "content": formatted_prompt}],
            api_key=api_key,
            response_format={ "type": "json_object" }
        )
        
        # Parse the JSON string into a Python Dictionary
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        return {"error": str(e)}

# --- STREAMLIT UI ---
st.set_page_config(page_title="AI Triple Translator", layout="centered")

st.title("🎯 Triple English Translator")
st.markdown("Enter your text below to get three distinct AI-powered English variations.")

# Simplified Input: Only the text to translate
source_text = st.text_area("Source Text:", placeholder="Enter text in any language...", height=150)

if st.button("Translate Now", use_container_width=True):
    if not source_text.strip():
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Generating translations..."):
            results = get_translations(source_text)
        
        if "error" in results:
            st.error(f"API Error: {results['error']}")
        else:
            st.divider()
            
            # Displaying results in a clean vertical list for better readability
            # Version 1: Formal
            st.subheader("🏛️ Formal Version")
            st.info(results.get("v1", "Translation missing"))
            
            # Version 2: Idiomatic
            st.subheader("🗣️ Natural / Idiomatic")
            st.success(results.get("v2", "Translation missing"))
            
            # Version 3: Poetic
            st.subheader("✨ Creative / Poetic")
            st.warning(results.get("v3", "Translation missing"))