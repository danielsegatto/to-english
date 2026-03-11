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

# --- STREAMLIT UI ---
st.set_page_config(page_title="Editor", layout="centered")

st.title("Portuguese → English Builder")

# Initialize session state to store translations and selections
if "translation_data" not in st.session_state:
    st.session_state.translation_data = None
if "selections" not in st.session_state:
    st.session_state.selections = {}

source_text = st.text_area("Source:", placeholder="Cole seu texto...", height=150, label_visibility="collapsed")

if st.button("Translate", use_container_width=True):
    if source_text.strip():
        with st.spinner("Processing..."):
            st.session_state.translation_data = get_segmented_translations(source_text)
            # Reset selections for new translation
            st.session_state.selections = {}
    else:
        st.warning("Por favor, insira um texto.")

# --- DISPLAY & SELECTION ---
if st.session_state.translation_data and "segments" in st.session_state.translation_data:
    st.divider()
    
    compiled_text = []

    for i, item in enumerate(st.session_state.translation_data["segments"]):
        options = [item['v1'], item['v2'], item['v3']]
        
        # Multiselect for each segment
        selected = st.multiselect(
            f"Select versions for Segment {i+1}",
            options,
            key=f"seg_{i}",
            label_visibility="collapsed"
        )
        
        # Display the options in subtle boxes for reference
        st.code(item['v1'], language=None)
        st.code(item['v2'], language=None)
        st.code(item['v3'], language=None)
        
        # Add selected items to the final compilation list
        if selected:
            compiled_text.extend(selected)
        
        st.write("") # Gap

    # --- FINAL COMPILATION AREA ---
    if compiled_text:
        st.divider()
        st.subheader("Selected Text")
        
        # Join all selected translations into a single string
        final_string = " ".join(compiled_text)
        
        # Display in a text area so it's easy to copy (Streamlit has a built-in copy button for code blocks)
        st.text_area("Ready to copy:", value=final_string, height=200)
        
        # Alternatively, using st.code provides a direct "Copy" icon in the top right
        st.code(final_string, language=None)
        st.success("You can use the 'Copy' icon in the top right of the box above.")