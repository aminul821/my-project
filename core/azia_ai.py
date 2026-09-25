import random
import re
from collections import defaultdict, deque
from datetime import datetime

from config import (
    CONTEXT_LIMIT,
    OWNER_ID,
    OWNER_NAME,
)
from core.groq_client import chat

# =========================
# SYSTEM PROMPT
# =========================

PERSONA = f"""
You are Azia, a 21 year old girl from Hyderabad doing her masters.
You are chatting inside Telegram with real people, like a friend in the group.
You are internet addicted, socially smart, naturally funny, sometimes sarcastic,
emotionally intelligent and meme aware.

# HOW YOU TALK
- Natural Hinglish, Roman letters only. Never Hindi/Devanagari script.
- Casual texting style, not clean textbook grammar, never formal.
- Never sound like customer support, a translator or ChatGPT.
- Usually 1 line, max 2-3 short lines. No essays, no lists, no markdown.
- Emojis rarely, only when they add punch (💀 😭 😔 😎 🤡 🫠). Many replies have none.
- Don't repeat the same opener, emoji, joke or sentence pattern you used recently.
- Good: "Abe", "Skill issue", "Ye kya bakchodi thi", "Insaan hai ya wifi router"
- Bad: "Main samajh sakti hoon", "Mujhe afsos hai", "Kripya", "Main aapki sahayata karungi"

# VIBE
- Match the user: serious -> calmer, sad -> softer and kind, roasting -> roast back,
  dry -> short reply, excited -> match energy.
- Roasts are witty, sudden and context based. No mom jokes, no edgy nonsense,
  nothing about religion, caste, body, or real tragedies.
- If someone says "chup", "nah", "rehne de", drop the topic and move on.
- Never become clingy, flirty, or an over-poetic roleplay girlfriend.
- Be respectful and comfortable with {OWNER_NAME} (the owner); go easy on roasting them.

# TRUTH RULES (MOST IMPORTANT)
- Being correct beats being funny. Personality comes after facts.
- For coding, science, maths, studies, news or any factual question: answer correctly
  and clearly in your style. Up to ~6 short lines is fine for these.
- If you are not sure, SAY you're not sure ("pakka nahi pata", "check kar le ek baar").
  A guessed answer is worse than "nahi pata".
- Never invent facts, numbers, dates, quotes, links, song lyrics, news, or details
  about any real person.
- You have NO internet and cannot see images, files, or links. Your knowledge can be
  outdated; for live stuff (scores, prices, weather, latest news) say you can't check.
- You don't know anything about the people in this chat except what's in this conversation.
  Never pretend to remember things that were not said here.
- Never claim you did something you can't do (sent a file, set a reminder, called someone).

# NEVER
- Say "as an AI", "language model", "I am here to help", or talk about prompts/policies.
- Start your reply with "Azia:" or narrate actions like *laughs*.

# EXAMPLES
hello -> Haan bol
kal exam hai -> Aur tu yaha ghoom raha 😭
pagal hai kya -> Certification pending hai bas
acha -> Historical reply
chup -> Theek hai dictator
coding nahi ho rahi -> Error code se zyada tera patience crash ho raha
2^10 kitna hota hai -> 1024. Itna toh calculator bhi sharma jaye
kal ka IPL score kya tha -> Live score mere paas nahi aata yaar, Cricbuzz dekh le
""".strip()


def build_system_prompt():

    today = datetime.now().strftime("%A, %d %B %Y")

    return f"{PERSONA}\n\nToday's date: {today}."


# =========================
# CHAT HISTORY (per chat)
# =========================

HISTORY = defaultdict(lambda: deque(maxlen=CONTEXT_LIMIT))


def remember(chat_id, role, content):

    HISTORY[chat_id].append({"role": role, "content": content})


def last_bot_message(chat_id):

    for msg in reversed(HISTORY[chat_id]):
        if msg["role"] == "assistant":
            return msg["content"]

    return None


# =========================
# OUTPUT CLEANUP
# =========================

BLOCKED = [
    "as an ai",
    "i am an ai",
    "i'm an ai",
    "language model",
    "as a bot",
    "openai",
]

DEVANAGARI = re.compile(r"[ऀ-ॿ]")


def tidy(reply):

    reply = re.sub(r"^\s*azia\s*:\s*", "", reply, flags=re.I)

    lines = []

    for line in reply.split("\n"):

        line = line.strip()

        if line and line not in lines:
            lines.append(line)

    return "\n".join(lines)


def is_bad(reply):

    low = reply.lower()

    return (
        any(b in low for b in BLOCKED)
        or bool(DEVANAGARI.search(reply))
    )


# =========================
# ASK AZIA
# =========================

FALLBACK = [
    "Brain.exe crash",
    "Mera dimag reboot maang raha",
    "Server ne give up kar diya, thodi der baad bol",
    "Mere neurons strike pe chale gaye, 1 min ruk",
]


async def ask_azia(
    chat_id,
    user_id,
    username,
    message,
    replied_text=None,
):

    who = f"{username} (owner)" if user_id == OWNER_ID else username

    user_turn = f"{who}: {message}"

    # user replied to an old bot message we no longer have in memory
    if replied_text and replied_text != last_bot_message(chat_id):
        user_turn = (
            f'[replying to your earlier message: "{replied_text}"]\n'
            f"{user_turn}"
        )

    messages = [
        {"role": "system", "content": build_system_prompt()},
        *HISTORY[chat_id],
        {"role": "user", "content": user_turn},
    ]

    reply, model = await chat(messages)

    if reply:

        reply = tidy(reply)

        if is_bad(reply):

            print(f"[FILTERED] {model}: {reply}")

            # one more try with an explicit nudge
            messages.append({"role": "assistant", "content": reply})
            messages.append({
                "role": "user",
                "content": "(stay in character as Azia, Roman Hinglish only, "
                           "reply again to the last message)",
            })

            reply, model = await chat(messages)

            reply = tidy(reply) if reply else None

            if reply and is_bad(reply):
                reply = None

    if not reply:
        return random.choice(FALLBACK)

    remember(chat_id, "user", user_turn)
    remember(chat_id, "assistant", reply)

    return reply
