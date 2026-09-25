from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram.enums import ChatAction

import random
import time
import traceback

from config import (

    OWNER_ID,

    RANDOM_REPLY_CHANCE,

    GROUP_REPLY_COOLDOWN
)

from core.azia_ai import ask_azia

# =========================
# GROUP COOLDOWN
# =========================

GROUP_LAST_REPLY = {}

# =========================
# RANDOM REPLY
# =========================

def should_random_reply(

    text

):

    if not text:

        return False

    # ignore short msgs
    if len(text) < 4:

        return False

    # ignore commands
    if text.startswith("/"):

        return False

    # ignore links
    if "http" in text:

        return False

    return (

        random.randint(1, 100)

        <= RANDOM_REPLY_CHANCE
    )

# =========================
# MAIN CHAT
# =========================

async def group_chat(

    client,

    message: Message
):

    try:

        text = (

            message.text or ""

        ).strip()

        if not text:

            return

        user = message.from_user

        if not user:

            return

        group_id = message.chat.id

        user_id = user.id

        username = (

            user.first_name

            or "Unknown"
        )

        text_lower = text.lower()

        print(

            f"\n[MESSAGE] {username}: {text}"
        )

        # =========================
        # MUST REPLY
        # =========================

        must_reply = False

        # azia name
        if (

            "azia" in text_lower

            or "@azia_smartai_bot" in text_lower
        ):

            must_reply = True

        # =========================
        # REPLY TO AZIA
        # =========================

        if message.reply_to_message:

            replied = (

                message.reply_to_message
            )

            if (

                replied.from_user

                and replied.from_user.is_bot
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
        # OWNER PRIORITY
        # =========================

        if user_id == OWNER_ID:

            must_reply = True

        # =========================
        # RANDOM REPLY
        # =========================

        if not must_reply:

            if should_random_reply(

                text
            ):

                must_reply = True

        if not must_reply:

            return

        # =========================
        # COOLDOWN
        # =========================

        now = time.time()

        last = GROUP_LAST_REPLY.get(

            group_id,

            0
        )

        if (

            now - last

            < GROUP_REPLY_COOLDOWN
        ):

            if user_id != OWNER_ID:

                return

        GROUP_LAST_REPLY[
            group_id
        ] = now

        print(

            "[AZIA REPLYING]"
        )

        # =========================
        # TYPING
        # =========================

        await client.send_chat_action(

            group_id,

            ChatAction.TYPING
        )

        # =========================
        # AI
        # =========================

        print(

            "[CALLING AZIA AI]"
        )

        reply = await ask_azia(

            group_id,

            user_id,

            username,

            text
        )

        print(

            "[AZIA REPLY RECEIVED]"
        )

        print(reply)

        if not reply:

            return

        # =========================
        # SEND
        # =========================

        await message.reply_text(

            reply,

            quote=True
        )

    except Exception:

        print(

            "\n[CHAT HANDLER ERROR]"
        )

        traceback.print_exc()

# =========================
# START COMMAND
# =========================

async def start_cmd(

    client,

    message: Message
):

    await message.reply_text(

        "Haan 😭 Azia online hai."
    )

# =========================
# SETUP
# =========================

def setup_chat(app):

    app.add_handler(

        MessageHandler(

            group_chat,

            filters.text

            & filters.group
        )
    )

    app.add_handler(

        MessageHandler(

            start_cmd,

            filters.command("start")
        )
    )
