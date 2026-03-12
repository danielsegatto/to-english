import streamlit as st
import streamlit.components.v1 as components
from translator import get_segmented_translations # Import the logic

# --- CALLBACKS ---
def handle_translation():
    """Manages input clearing and state resets."""
    if st.session_state.source_text_key.strip():
        st.session_state.text_to_process = st.session_state.source_text_key
        st.session_state.source_text_key = ""
        st.session_state.translation_data = None
        st.session_state.run_id += 1 
    else:
        st.session_state.text_to_process = None

# --- UI SETUP ---
st.set_page_config(page_title="Translator", layout="centered")

if "translation_data" not in st.session_state:
    st.session_state.translation_data = None
if "text_to_process" not in st.session_state:
    st.session_state.text_to_process = None
if "run_id" not in st.session_state:
    st.session_state.run_id = 0

source_text = st.text_area(
    "Source:", 
    placeholder="...", 
    height=150, 
    label_visibility="collapsed",
    key="source_text_key" 
)

if st.button("Translate (Ctrl+Enter)", use_container_width=True, on_click=handle_translation, key="translate_btn"):
    if st.session_state.text_to_process:
        with st.spinner("Processing..."):
            st.session_state.translation_data = get_segmented_translations(st.session_state.text_to_process)

# --- RESULTS DISPLAY ---
if st.session_state.translation_data and "segments" in st.session_state.translation_data:
    st.divider()
    selected_versions = []
    rid = st.session_state.run_id

    for i, item in enumerate(st.session_state.translation_data["segments"]):
        # Dynamic keys prevent persistence
        v1_check = st.checkbox(item['v1'], key=f"run_{rid}_seg_{i}_v1")
        if v1_check: selected_versions.append(item['v1'])
            
        v2_check = st.checkbox(item['v2'], key=f"run_{rid}_seg_{i}_v2")
        if v2_check: selected_versions.append(item['v2'])
            
        v3_check = st.checkbox(item['v3'], key=f"run_{rid}_seg_{i}_v3")
        if v3_check: selected_versions.append(item['v3'])
        
        st.write("") 

    if selected_versions:
        st.divider()
        st.code(" ".join(selected_versions), language=None)

# --- JS COMPONENTS ---
components.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.keyCode === 13) {
            const buttons = doc.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.innerText.includes("Translate (Ctrl+Enter)")) {
                    btn.click();
                    break;
                }
            }
        }
    });
    </script>
    """, height=0, width=0)