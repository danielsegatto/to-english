import streamlit as st
import streamlit.components.v1 as components

def inject_keyboard_shortcut():
    """Injects JavaScript for shortcuts and forces a custom tab title."""
    components.html(
        """
        <script>
        const doc = window.parent.document;
        
        // Overwrite the default Streamlit title suffix
        doc.title = "BR ➡️ US";

        doc.addEventListener('keydown', function(e) {
            // 1. Keyboard Shortcut (Ctrl+Enter) to Translate
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const buttons = doc.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.innerText.includes("Translate")) {
                        btn.click();
                        e.preventDefault();
                        break;
                    }
                }
            }

            // 2. Keyboard Shortcut ('/') to Focus Input
            if (e.key === '/' && 
                doc.activeElement.tagName !== 'TEXTAREA' && 
                doc.activeElement.tagName !== 'INPUT') {
                
                e.preventDefault(); 
                const textArea = doc.querySelector('textarea');
                if (textArea) {
                    textArea.focus();
                }
            }
        }, true);
        </script>
        """, height=0, width=0
    )