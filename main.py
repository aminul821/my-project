from pyrogram import Client

from config import (

    BOT_TOKEN,
    API_ID,
    API_HASH,
    GROQ_API_KEYS,
    MODELS
)

from handlers.chat import setup_chat
from handlers.welcome import setup_welcome

# =========================
# CHECKS
# =========================

if not (BOT_TOKEN and API_ID and API_HASH):

    raise SystemExit(
        "BOT_TOKEN / API_ID / API_HASH missing. Copy .env.example to .env and fill it."
    )

if not GROQ_API_KEYS:

    raise SystemExit(
        "No Groq keys found. Set GROQ_API_KEYS in .env."
    )

# =========================
# CLIENT
# =========================

app = Client(

    "azia_bot",

    bot_token=BOT_TOKEN,

    api_id=API_ID,

    api_hash=API_HASH
)

setup_welcome(app)

setup_chat(app)

# =========================
# START
# =========================

if __name__ == "__main__":

    print("\n=========================")
    print("🌙 Azia Started")
    print(f"Groq keys: {len(GROQ_API_KEYS)}")
    print(f"Models:    {', '.join(MODELS)}")
    print("=========================\n")

    app.run()
