# to-english

Translate Brazilian Portuguese text into English variations using Streamlit + Groq.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Export your Groq key:

```bash
export GROQ_API_KEY="your_groq_api_key"
```

3. Optional: choose a model (default is `openai/gpt-oss-120b`):

```bash
export GROQ_MODEL="openai/gpt-oss-120b"
```

4. Optional tuning parameters:

```bash
export GROQ_TEMPERATURE="1"
export GROQ_MAX_COMPLETION_TOKENS="8192"
export GROQ_TOP_P="1"
export GROQ_REASONING_EFFORT="medium"
```

5. Run the app:

```bash
streamlit run app.py
```

## Keep API Keys Safe

1. Create your local env file from the template:

```bash
cp .env.example .env
```

2. Load variables in your shell session:

```bash
set -a && source .env && set +a
```

3. Install and enable pre-commit hooks (includes gitleaks secret scanning):

```bash
pip install pre-commit
pre-commit install
```

4. Run hooks on all files before pushing:

```bash
pre-commit run --all-files
```

Notes:
- `.env` and related secret files are ignored by git in `.gitignore`.
- If a key is ever exposed, revoke it immediately and generate a new key.