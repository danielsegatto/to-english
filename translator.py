import json
from litellm import completion
import os

# API configuration
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
    """Sends text to GPT-OSS-120B and returns structured JSON."""
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