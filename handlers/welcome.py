from pyrogram import filters
from pyrogram.types import Message

import random

from main import app

# =========================
# WELCOME MESSAGES
# =========================

WELCOME_MESSAGES = [

    "Welcome 😭 ab group ki average IQ aur girne wali hai",

    "Aagaye boss 😈 attendance lag gayi",

    "Ek aur insaan internet barbaad karne aagaya 😭",

    "Welcome 😭 yaha logic optional hai",

    "Aaj ka new character enter ho gaya 😭",

    "Lo aa gaya fresh content 💀",

    "Ab maza ayega ya aur chaos hoga 😭",

    "Welcome 😎 ab bakchodi officially shuru",

    "Ek aur overthinker join kar gaya 😔",

    "Group ne ek aur victim recruit kar liya 😭",

    "Yaha sab normal hote toh tum join nahi karte 😭",

    "Welcome 😈 ab tum bhi suffer karoge",

    "Achievement unlocked: random group joined 💀",

    "Ab yaha productivity aur kam hogi 😭",

    "Chalo kisi ne toh invite accept kiya 😔",

    "Welcome 😭 therapist ki zarurat sabko padegi",

    "Aur batao 😭 life ne idhar kaise phek diya",

    "Fresh banda detected 😎 scan complete",

    "Ab dekhna 😭 yaha sleep schedule barbaad hota hai",

    "Welcome 😈 ab tumhara bhi brainrot start"
]

# =========================
# MEMBER JOIN
# =========================

@app.on_message(filters.new_chat_members)

async def welcome_handler(
    client,
    message: Message
):

    try:

        for member in message.new_chat_members:

            # skip bot itself
            if member.is_bot:

                continue

            first_name = member.first_name

            welcome_text = random.choice(
                WELCOME_MESSAGES
            )

            final_message = (

                f"**{first_name}**\n\n"
                f"{welcome_text}"
            )

            await message.reply_text(
                final_message
            )

    except Exception as e:

        print(
            "\n[WELCOME ERROR]"
        )

        print(e)
