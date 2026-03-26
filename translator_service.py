import json
from groq import Groq
from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    SYSTEM_PROMPT,
    TEMPERATURE,
    MAX_COMPLETION_TOKENS,
    TOP_P,
    REASONING_EFFORT,
)

def get_segmented_translations(full_text):
    """Sends text to the AI and returns the structured JSON response."""
    if not GROQ_API_KEY:
        return {
            "error": "Missing GROQ_API_KEY environment variable. Set it and try again."
        }

    formatted_prompt = SYSTEM_PROMPT.format(text=full_text)
    try:
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": formatted_prompt}],
            temperature=TEMPERATURE,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
            top_p=TOP_P,
            reasoning_effort=REASONING_EFFORT,
            stream=False,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}