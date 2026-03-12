import streamlit as st
from litellm import completion
import json
import os

# --- APP CONFIGURATION ---
api_key = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """
You are a translation editor specializing in Brazilian Portuguese to English. 
Your task is to:
1. Divide the provided text into logical, readable segments (sentences or short meaningful phrases).
2. For EACH segment, provide 3 distinct and high-quality English translations.

Return ONLY a JSON object with this exact structure:
{{
  "segments": [
    {{
      "original": "Texto original em português",
      "v1": "First English variation",
      "v2": "Second English variation",
      "v3": "Third English variation"
    }},
    ...
  ]
}}

Text to process (PT-BR): {text}
"""

def get_segmented_translations(full_text):
    formatted_prompt = SYSTEM_PROMPT.format(text=full_text)
    try:
        response = completion(
            model="groq/openai/gpt-oss-120b",
            messages=[{"role": "user", "content": formatted_prompt}],
            api_key=api_key,
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Translator Builder", layout="centered")

st.title("Portuguese → English Builder")

# Initialize session state
if "translation_data" not in st.session_state:
    st.session_state.translation_data = None

source_text = st.text_area("Source:", placeholder="Cole seu texto...", height=150, label_visibility="collapsed")

if st.button("Translate", use_container_width=True):
    if source_text.strip():
        with st.spinner("Processing..."):
            st.session_state.translation_data = get_segmented_translations(source_text)
    else:
        st.warning("Por favor, insira um texto.")

# --- DISPLAY & INDIVIDUAL CHECKBOXES ---
if st.session_state.translation_data and "segments" in st.session_state.translation_data:
    st.divider()
    
    selected_versions = []

    for i, item in enumerate(st.session_state.translation_data["segments"]):
        # Create three checkboxes for the three versions
        # We use a unique key for each checkbox based on segment index and version number
        
        v1_check = st.checkbox(item['v1'], key=f"seg_{i}_v1")
        if v1_check:
            selected_versions.append(item['v1'])
            
        v2_check = st.checkbox(item['v2'], key=f"seg_{i}_v2")
        if v2_check:
            selected_versions.append(item['v2'])
            
        v3_check = st.checkbox(item['v3'], key=f"seg_{i}_v3")
        if v3_check:
            selected_versions.append(item['v3'])
        
        st.write("") # Small spacing between segments

    # --- FINAL COMPILATION AREA ---
    if selected_versions:
        st.divider()
        st.subheader("Selected Text")
        
        # Join all selected translations
        final_string = " ".join(selected_versions)
        
        # Display in a code block for the one-click "Copy" icon
        st.code(final_string, language=None)
        
        # Optional: Clear button to reset checkboxes
        if st.button("Reset All Selections"):
            for key in st.session_state.keys():
                if key.startswith("seg_"):
                    st.session_state[key] = False
            st.rerun()