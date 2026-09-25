from pyrogram import filters
from pyrogram.enums import ChatAction, ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

import random
import time
import traceback

from config import (

    OWNER_ID,

    BOT_USERNAME,

    RANDOM_REPLY_CHANCE,

    GROUP_REPLY_COOLDOWN,

    CONVO_WINDOW
)

from core.azia_ai import ask_azia

# =========================
# STATE
# =========================

GROUP_LAST_REPLY = {}

# (chat_id, user_id) -> last time Azia replied to that user
ACTIVE_CONVO = {}

BOT_ID = None

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

async def azia_chat(

    client,

    message: Message
):

    global BOT_ID

    try:

        text = (

            message.text or ""

        ).strip()

        if not text or text.startswith("/"):

            return

        user = message.from_user

        if not user or user.is_bot:

            return

        if BOT_ID is None:

            BOT_ID = (await client.get_me()).id

        chat_id = message.chat.id

        user_id = user.id

        username = (

            user.first_name

            or "Unknown"
        )

        is_private = (

            message.chat.type == ChatType.PRIVATE
        )

        text_lower = text.lower()

        print(

            f"\n[MESSAGE] {username}: {text}"
        )

        # =========================
        # MUST REPLY
        # =========================

        must_reply = is_private

        # azia name
        if (

            "azia" in text_lower

            or f"@{BOT_USERNAME}" in text_lower
        ):

            must_reply = True

        # =========================
        # REPLY TO AZIA
        # =========================

        replied_text = None

        replied = message.reply_to_message

        if (

            replied

            and replied.from_user

            and replied.from_user.id == BOT_ID
        ):

            must_reply = True

            replied_text = replied.text or None

        # =========================
        # OWNER PRIORITY
        # =========================

        if user_id == OWNER_ID:

            must_reply = True

        # =========================
        # ONGOING CONVERSATION
        # =========================
        # "Kaise ho" right after Azia answered you should
        # still get a reply without saying "azia" again.

        in_convo = (

            time.time() - ACTIVE_CONVO.get((chat_id, user_id), 0)

            < CONVO_WINDOW
        )

        # someone else's reply thread -> not talking to Azia
        if replied and not replied_text:

            in_convo = False

        if in_convo:

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
        # COOLDOWN (groups only)
        # =========================

        if (

            not is_private

            and user_id != OWNER_ID

            and not in_convo

            and not replied_text
        ):

            now = time.time()

            last = GROUP_LAST_REPLY.get(

                chat_id,

                0
            )

            if (

                now - last

                < GROUP_REPLY_COOLDOWN
            ):

                return

            GROUP_LAST_REPLY[
                chat_id
            ] = now

        print(

            "[AZIA REPLYING]"
        )

        # =========================
        # TYPING
        # =========================

        await client.send_chat_action(

            chat_id,

            ChatAction.TYPING
        )

        # =========================
        # AI
        # =========================

        reply = await ask_azia(

            chat_id,

            user_id,

            username,

            text,

            replied_text
        )

        print(

            f"[AZIA] {reply}"
        )

        if not reply:

            return

        # =========================
        # SEND
        # =========================

        await message.reply_text(

            reply,

            quote=True
        )

        ACTIVE_CONVO[(chat_id, user_id)] = time.time()

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

            start_cmd,

            filters.command("start")
        )
    )

    app.add_handler(

        MessageHandler(

            azia_chat,

            filters.text
        )
    )
