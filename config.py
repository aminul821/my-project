import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# =========================
# TELEGRAM BOT CONFIG
# =========================
# Never hardcode these. Put them in .env (see .env.example).

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

API_ID = int(os.getenv("API_ID", "0") or 0)

API_HASH = os.getenv("API_HASH", "")

BOT_USERNAME = os.getenv("BOT_USERNAME", "azia_smartai_bot").lower().lstrip("@")

# =========================
# OWNER
# =========================

OWNER_ID = int(os.getenv("OWNER_ID", "5041960003"))

OWNER_NAME = os.getenv("OWNER_NAME", "Aman")

# =========================
# GROQ API KEYS (ROTATION)
# =========================
# Any of these work, all found keys are merged and de-duplicated:
#   GROQ_API_KEYS=key1,key2,key3
#   GROQ_API_KEY_1=key1  GROQ_API_KEY_2=key2 ...
#   GROQ_API_KEY=key1
# Keys must come from DIFFERENT Groq accounts/orgs, otherwise
# they share one rate limit and rotation does nothing.


def _load_groq_keys():

    keys = []

    keys += os.getenv("GROQ_API_KEYS", "").split(",")

    i = 1
    while os.getenv(f"GROQ_API_KEY_{i}"):
        keys.append(os.getenv(f"GROQ_API_KEY_{i}"))
        i += 1

    keys.append(os.getenv("GROQ_API_KEY", ""))

    seen = []
    for k in keys:
        k = (k or "").strip()
        if k and k not in seen:
            seen.append(k)

    return seen


GROQ_API_KEYS = _load_groq_keys()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# =========================
# AI MODELS (PRIORITY ORDER)
# =========================
# llama-3.3-70b-versatile and llama-3.1-8b-instant were shut down
# by Groq on 2026-08-16. Current recommended replacements:
#   openai/gpt-oss-120b  -> best quality / least hallucination
#   qwen/qwen3.6-27b     -> strong non-OpenAI fallback
#   openai/gpt-oss-20b   -> fastest, highest rate limits
# Override with GROQ_MODELS=model_a,model_b. Models that Groq no
# longer lists are skipped automatically at runtime.

MODELS = [
    m.strip()
    for m in os.getenv(
        "GROQ_MODELS",
        "openai/gpt-oss-120b,qwen/qwen3.6-27b,openai/gpt-oss-20b",
    ).split(",")
    if m.strip()
]

# Low temperature = fewer made-up facts, still casual.
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.4"))

# Reasoning models spend tokens thinking before answering. If this
# is too low (the old value was 90) the reply comes back empty.
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "700"))

REQUEST_TIMEOUT = 30

# =========================
# GROUP SETTINGS
# =========================

# random reply chance (percent)
RANDOM_REPLY_CHANCE = 7

# cooldown between replies (seconds)
GROUP_REPLY_COOLDOWN = 15

# how many past messages per chat are sent to the model
CONTEXT_LIMIT = 12

# =========================
# MEMORY SETTINGS
# =========================

MEMORY_FILE = "memory.json"

GROUP_MEMORY_FILE = "group_memory.json"

CHAT_HISTORY_FILE = "chat_history.json"

# =========================
# LEAVE MESSAGES
# =========================

LEAVE_MESSAGES = [

    "Chalo ek competitor kam hua 😭",

    "Connection gaya ya self respect? 😔",

    "Group ne finally kisi ko hara diya 😭",

    "Bye 😈 cringe wapas leke aana",

    "Achievement unlocked: escape successful 😭"
]

# =========================
# RANDOM ROASTS
# =========================

RANDOM_ROASTS = [

    "Padhai toh clearly nahi ho rahi 😭",

    "Aap logon ka confidence illegal hai 😭",

    "Ye group aur mental stability ek saath nahi chal sakte 😔",

    "Kisi din productive bhi ho jao 😭",

    "Yaha sab experts hain bas topic nahi pata 😭"
]
