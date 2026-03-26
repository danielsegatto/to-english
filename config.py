import os

# API Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_NAME = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
TEMPERATURE = float(os.environ.get("GROQ_TEMPERATURE", "1"))
MAX_COMPLETION_TOKENS = int(os.environ.get("GROQ_MAX_COMPLETION_TOKENS", "8192"))
TOP_P = float(os.environ.get("GROQ_TOP_P", "1"))
REASONING_EFFORT = os.environ.get("GROQ_REASONING_EFFORT", "medium")

# AI Personality and Instructions
SYSTEM_PROMPT = """
You are a translation editor specializing in Brazilian Portuguese to English. 
Your task is to:
1. Divide the provided text into logical, readable segments (sentences or short meaningful phrases).
2. If a sentence is long, break it into individual phrases. 
  - Favor more segments over fewer. 
  - Each segment should represent a single, focused idea or action.
  - A segment should typically be a single clause or a short phrase.
3. For EACH segment, provide 3 distinct and high-quality English translations.

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