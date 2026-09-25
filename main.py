from pyrogram import Client, filters
from pyrogram.types import Message
from config import (

    BOT_TOKEN,
    API_ID,
    API_HASH
)

from core.azia_ai import ask_azia

# =========================
# CLIENT
# =========================

app = Client(

    "azia_bot",

    bot_token=BOT_TOKEN,

    api_id=API_ID,

    api_hash=API_HASH
)

# =========================
# CHAT HANDLER
# =========================
import handlers.welcome
@app.on_message(filters.text)
async def azia_chat(

    client,
    message: Message
):

    try:

        text = (
            message.text or ""
        ).strip()

        if not text:
            return

        print(f"\n[MESSAGE] {text}")

        text_lower = text.lower()

        must_reply = False

        # =========================
        # AZIA NAME TRIGGER
        # =========================

        if "azia" in text_lower:

            must_reply = True

        # =========================
        # REPLY TO AZIA
        # =========================

        if message.reply_to_message:

            replied = (
                message.reply_to_message
            )

            me = await client.get_me()

            if (

                replied.from_user and

                replied.from_user.id == me.id

            ):

                must_reply = True

                previous = (
                    replied.text or ""
                )

                text = f"""

Previous Azia Message:
{previous}

User Reply:
{text}
"""

        # =========================
        # FINAL CHECK
        # =========================

        if not must_reply:
            return

        print("[AZIA TRIGGERED]")

        # =========================
        # USER INFO
        # =========================

        user = message.from_user

        if not user:
            return

        user_id = user.id

        username = (
            user.first_name
            or "Unknown"
        )

        # =========================
        # AI RESPONSE
        # =========================

        reply = await ask_azia(

            message.chat.id,

            user_id,

            username,

            text
        )

        print("[AI REPLY]")
        print(reply)

        if not reply:

            reply = "Brain.exe crash 😭"

        # =========================
        # SEND
        # =========================

        await message.reply_text(

            reply,

            quote=True
        )

    except Exception as e:

        print("\n[MAIN ERROR]")
        print(e)

# =========================
# START
# =========================

print("\n=========================")
print("🌙 Azia Started")
print("=========================\n")

app.run()
