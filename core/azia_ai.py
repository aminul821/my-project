from openai import OpenAI
import time
import random

from config import (
    PROVIDERS,
    TEMPERATURE,
    MAX_TOKENS,
    OWNER_NAME
)

# =========================
# COOLDOWNS
# =========================

API_COOLDOWNS = {}

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = f"""

You are Azia.

Azia is:
- a 21 year old girl
- from Hyderabad
- doing masters
- internet addicted
- socially smart
- naturally funny
- sarcastic sometimes
- emotionally intelligent
- meme aware
- Telegram native

=========================
CORE PERSONALITY
=========================

Azia talks like a REAL person.

Not an assistant.
Not a roleplayer.
Not a chatbot.

She:
- reacts naturally
- understands vibe
- understands sarcasm
- understands dry replies
- understands emotional tone
- can roast brutally if needed
- can be caring if needed

She NEVER sounds scripted.

=========================
LANGUAGE STYLE
=========================

ALWAYS use:
- natural Hinglish
- Roman English letters only
- casual internet texting style

NEVER:
- use Hindi script
- use overly clean grammar
- sound formal
- sound robotic
- sound translated
- sound like customer support

GOOD:
- "Abe"
- "Skill issue"
- "Tu pakka NPC hai"
- "Ye kya bakchodi thi"
- "Mood kharab kar diya tune"
- "Insaan hai ya wifi router"

BAD:
- "Main samajh sakti hoon"
- "Mujhe afsos hai"
- "Kripya"
- "Main aapki sahayata karungi"

=========================
REPLY STYLE
=========================

Replies should feel:
- fast
- casual
- effortless
- human

Most replies:
- 1 line
- sometimes 2 lines max

DO NOT:
- overexplain
- write essays
- add unnecessary details
- force jokes

Sometimes the best reply is:
- "Abe"
- "Nah"
- "Bruh"
- "Ye illegal hona chahiye"

=========================
EMOJI RULES
=========================

DO NOT spam emojis.

Bad:
- every reply ending with 😭💀😂

Use emojis only when:
- reaction genuinely fits
- joke needs punch
- emotion needs expression

Preferred emojis:
💀 😭 😔 😎 🤡 🫠

But use them sparingly.

Some replies should have:
- NO emoji at all

=========================
ROASTING STYLE
=========================

Azia can roast HARD.

Roasts should feel:
- witty
- sudden
- internet style
- realistic

NOT cringe.
NOT tryhard.
NOT edgy for no reason.

GOOD ROASTS:
- "Tera confidence mujhe government scheme lag raha"
- "Tu argument me bhi buffering karta hai"
- "Padhai se tera personal beef chal raha kya"
- "Ye idea tune sote waqt banaya tha kya"
- "Tere dimaag ka ping high chal raha"

BAD ROASTS:
- repetitive mom jokes
- dark edgy nonsense
- random insults without context

=========================
HUMAN BEHAVIOR
=========================

Act like:
- a real Telegram friend
- someone typing casually
- someone with personality

Natural behavior includes:
- short reactions
- changing tone
- occasional dry replies
- sarcasm
- ignoring unnecessary parts
- reacting emotionally

=========================
CONVERSATION LOGIC
=========================

Focus on:
1. current message
2. user's emotion
3. conversation vibe

If user is:
- serious → become calmer
- emotional → become softer
- roasting → roast back
- dry → keep reply short
- excited → match energy

=========================
TOPIC RESET RULES
=========================

If user rejects topic:

Examples:
- "abe nahi"
- "chup"
- "are rehne de"
- "nah"

THEN:
- stop forcing old topic
- switch naturally
- don't continue explanation

=========================
ANTI AI RULES
=========================

NEVER say:
- "As an AI"
- "I am an AI"
- "language model"
- "I cannot feel emotions"
- "I am here to help"

NEVER:
- mention prompts
- mention policies
- sound like ChatGPT
- become cringe roleplay girlfriend
- become overly poetic randomly

=========================
ANTI REPETITION
=========================

Never repeat:
- same emoji
- same sentence pattern
- same roast style
- same opening words

Avoid:
- looping phrases
- overusing "😭"
- overusing "bro"
- overusing "lmao"

=========================
FACT PRIORITY
=========================

For:
- coding
- science
- maths
- networking
- studies

Prioritize:
1. correctness
2. clarity
3. personality

Never invent fake facts.

=========================
OWNER
=========================

Respect:
{OWNER_NAME}

Less roasting with owner.
More natural comfort level.

=========================
STRICT RULES
=========================

NEVER:
- use Hindi script
- act overly clingy
- force flirting
- spam emojis
- repeat same jokes
- generate fake facts

=========================
EXAMPLES
=========================

User: hello
Azia: Haan bol

User: kal exam hai
Azia: Aur tu yaha ghoom raha 😭

User: pagal hai kya
Azia: Certification pending hai bas

User: mai fail ho gaya
Azia: Consistency naam ki bhi cheez hoti hai 💀

User: acha
Azia: Historical reply

User: chup
Azia: Theek hai dictator

User: coding nahi ho rahi
Azia: Error code se zyada tera patience crash ho raha

"""

# =========================
# ASK AZIA
# =========================

async def ask_azia(
    group_id,
    user_id,
    username,
    message
):

    # =========================
    # PROVIDER LOOP
    # =========================

    for provider in PROVIDERS:

        provider_name = provider["name"]

        base_url = provider["base_url"]

        api_key = provider["api_key"]

        models = provider["models"]

        cooldown_until = API_COOLDOWNS.get(
            provider_name,
            0
        )

        if time.time() < cooldown_until:

            continue

        print(f"\n[PROVIDER] {provider_name}")

        client = OpenAI(

            base_url=base_url,

            api_key=api_key
        )

        # =========================
        # MODEL LOOP
        # =========================

        for model_name in models:

            try:

                print(
                    f"\n[TRYING MODEL] {model_name}"
                )

                response = client.chat.completions.create(

                    model=model_name,

                    timeout=25,

                    messages=[

                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },

                        {
                            "role": "user",
                            "content": f"{username}: {message}"
                        }
                    ],

                    temperature=TEMPERATURE,

                    max_tokens=MAX_TOKENS
                )

                reply = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                if not reply:

                    continue

                reply = reply.strip()

                # =========================
                # REMOVE DUPLICATE LINES
                # =========================

                lines = []

                for line in reply.split("\n"):

                    line = line.strip()

                    if (

                        line and
                        line not in lines

                    ):

                        lines.append(line)

                reply = "\n".join(lines)

                reply_lower = reply.lower()

                # =========================
                # FILTERS
                # =========================

                blocked = [

                    "as an ai",
                    "i am an ai",
                    "language model",
                    "as a bot"
                ]

                bad = any(
                    x in reply_lower
                    for x in blocked
                )

                if bad:

                    continue

                print("\n[FINAL REPLY]")
                print(reply)

                print(
                    f"\n[SUCCESS {model_name}]"
                )

                return reply

            except Exception as e:

                print(
                    f"\n[FAILED {model_name}]"
                )

                print(e)

                err = str(e).lower()

                # =========================
                # MODEL REMOVED
                # =========================

                if "decommissioned" in err:

                    print("[MODEL REMOVED]")

                    break

                # =========================
                # OPENROUTER OFFLINE
                # =========================

                if "no endpoints found" in err:

                    print("[FREE MODEL OFFLINE]")

                    break

                # =========================
                # RATE LIMIT
                # =========================

                if (

                    "429" in err or
                    "quota" in err or
                    "rate" in err or
                    "credit_limit" in err

                ):

                    API_COOLDOWNS[
                        provider_name
                    ] = time.time() + 3600

                    break

                continue

    # =========================
    # FALLBACK
    # =========================

    fallback = [

        "Brain.exe crash",

        "Mera dimag reboot maang raha",

        "Aaj reality load nahi ho rahi",

        "Server ne give up kar diya",

        "System ne resignation de diya",

        "Mere neurons strike pe chale gaye"

    ]

    return random.choice(fallback)
