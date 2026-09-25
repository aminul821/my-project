import os
# =========================
# TELEGRAM BOT CONFIG
# =========================

BOT_TOKEN = "8183141918:AAFzF6WesnG2FrYsUhv9hPO4Uzy9zxJNO8Q"

API_ID = 2530306
API_HASH = "5ceff6daaeaa909c7d0084d092bff94f"

# =========================
# OWNER
# =========================

OWNER_ID = 5041960003

OWNER_NAME = "Aman"

# =========================
# HF API KEYS
# =========================

#HF_KEYS = [
 #  os.getenv("GROQ_API_KEY"),
  # os.getenv("GROQ_API_KEY"),
   # os.getenv("GROQ_API_KEY")

PROVIDERS = [

    {
        "name": "groq_1",

        "base_url": "https://api.groq.com/openai/v1",

        "api_key":os.getenv("GROQ_API_KEY") ,

        "models": [

            "llama-3.3-70b-versatile",

            "llama-3.1-8b-instant"
        ]
    },

    {
        "name": "groq_2",

        "base_url": "https://api.groq.com/openai/v1",

        "api_key": os.getenv("GROQ_API_KEY"),

        "models": [

            "llama-3.3-70b-versatile",

            "llama-3.1-8b-instant"
        ]
    },

    {
        "name": "groq_3",

        "base_url": "https://api.groq.com/openai/v1",

        "api_key":os.getenv("GROQ_API_KEY"),

        "models": [

            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    },
    {
        "name": "groq_4",

        "base_url": "https://api.groq.com/openai/v1",

        "api_key":os.getenv("GROQ_API_KEY"),

        "models": [

            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    },
    {
        "name": "groq_5",

        "base_url": "https://api.groq.com/openai/v1",

        "api_key":os.getenv("GROQ_API_KEY"),

        "models": [

            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    }
]
# =========================
# HF BASE URL
# =========================

#BASE_URL = "https://api.groq.com/openai/v1"

# =========================
# AI MODELS
# =========================
#========
# AI SETTINGS
# =========================
#MODELS = [

 ##   "llama-3.1-8b-instant",

   # "llama3-70b-8192"
#]

TEMPERATURE = 0.35

MAX_TOKENS = 90

# =========================
# GROUP SETTINGS
# =========================

# random reply chance
RANDOM_REPLY_CHANCE = 7

# cooldown between replies
GROUP_REPLY_COOLDOWN = 15

# context message count
CONTEXT_LIMIT = 6

# =========================
# MEMORY SETTINGS
# =========================

MEMORY_FILE = "memory.json"

GROUP_MEMORY_FILE = "group_memory.json"

CHAT_HISTORY_FILE = "chat_history.json"

# =========================
# WELCOME MESSAGES
# =========================

WELCOME_MESSAGES = [

    "Welcome 😭 ab group ki average IQ aur girne wali hai",

    "Aagaye boss 😈 attendance lag gayi",

    "Ek aur insaan internet barbaad karne aagaya 😭",

    "Welcome 😭 yaha logic optional hai",

    "Aaj ka new character enter ho gaya 😭"
]

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
