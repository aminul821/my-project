import json
import os
from datetime import datetime

from config import (
    MEMORY_FILE,
    GROUP_MEMORY_FILE,
    CHAT_HISTORY_FILE
)

# =========================
# JSON HELPERS
# =========================

def load_json(path, default):

    if os.path.exists(path):

        try:

            with open(path, "r") as f:
                return json.load(f)

        except:
            return default

    return default


def save_json(path, data):

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=2
        )

# =========================
# PERSONAL MEMORY
# =========================

def save_personal_memory(
    group_id,
    user_id,
    key,
    value
):

    data = load_json(
        MEMORY_FILE,
        {}
    )

    gid = str(group_id)
    uid = str(user_id)

    if gid not in data:
        data[gid] = {}

    if uid not in data[gid]:

        data[gid][uid] = {

            "personal": {},
            "personality": {},
            "inside_jokes": []
        }

    data[gid][uid]["personal"][key] = value

    save_json(MEMORY_FILE, data)

# =========================
# GET PERSONAL MEMORY
# =========================

def get_personal_memory(
    group_id,
    user_id
):

    data = load_json(
        MEMORY_FILE,
        {}
    )

    gid = str(group_id)
    uid = str(user_id)

    if gid not in data:
        return {}

    if uid not in data[gid]:
        return {}

    return data[gid][uid].get(
        "personal",
        {}
    )

# =========================
# PERSONALITY MEMORY
# =========================

def update_personality(
    group_id,
    user_id,
    trait
):

    data = load_json(
        MEMORY_FILE,
        {}
    )

    gid = str(group_id)
    uid = str(user_id)

    if gid not in data:
        data[gid] = {}

    if uid not in data[gid]:

        data[gid][uid] = {

            "personal": {},
            "personality": {},
            "inside_jokes": []
        }

    personality = data[gid][uid][
        "personality"
    ]

    personality[trait] = (
        personality.get(trait, 0) + 1
    )

    save_json(MEMORY_FILE, data)

# =========================
# GET PERSONALITY
# =========================

def get_personality(
    group_id,
    user_id
):

    data = load_json(
        MEMORY_FILE,
        {}
    )

    gid = str(group_id)
    uid = str(user_id)

    if gid not in data:
        return {}

    if uid not in data[gid]:
        return {}

    return data[gid][uid].get(
        "personality",
        {}
    )

# =========================
# INSIDE JOKES
# =========================

def add_inside_joke(
    group_id,
    user_id,
    joke
):

    data = load_json(
        MEMORY_FILE,
        {}
    )

    gid = str(group_id)
    uid = str(user_id)

    if gid not in data:
        data[gid] = {}

    if uid not in data[gid]:

        data[gid][uid] = {

            "personal": {},
            "personality": {},
            "inside_jokes": []
        }

    jokes = data[gid][uid][
        "inside_jokes"
    ]

    if joke not in jokes:

        jokes.append(joke)

    # limit
    jokes = jokes[-20:]

    data[gid][uid][
        "inside_jokes"
    ] = jokes

    save_json(MEMORY_FILE, data)

# =========================
# GET INSIDE JOKES
# =========================

def get_inside_jokes(
    group_id,
    user_id
):

    data = load_json(
        MEMORY_FILE,
        {}
    )

    gid = str(group_id)
    uid = str(user_id)

    if gid not in data:
        return []

    if uid not in data[gid]:
        return []

    return data[gid][uid].get(
        "inside_jokes",
        []
    )

# =========================
# CHAT HISTORY
# =========================

def save_chat_history(
    group_id,
    user_id,
    username,
    message
):

    data = load_json(
        CHAT_HISTORY_FILE,
        {}
    )

    gid = str(group_id)

    if gid not in data:
        data[gid] = []

    data[gid].append({

        "user_id": user_id,
        "username": username,
        "message": message,
        "time": datetime.now().isoformat()

    })

    # keep last 200 msgs
    data[gid] = data[gid][-200:]

    save_json(
        CHAT_HISTORY_FILE,
        data
    )

# =========================
# GET RECENT CHAT
# =========================

def get_recent_chat(
    group_id,
    limit=20
):

    data = load_json(
        CHAT_HISTORY_FILE,
        {}
    )

    gid = str(group_id)

    if gid not in data:
        return []

    return data[gid][-limit:]

# =========================
# SMART MEMORY DETECTION
# =========================

def auto_memory_save(
    group_id,
    user_id,
    text
):

    text_lower = text.lower()

    # birthday
    if (
        "birthday" in text_lower or
        "bday" in text_lower
    ):

        save_personal_memory(
            group_id,
            user_id,
            "birthday",
            text
        )

    # exam
    if (
        "exam" in text_lower or
        "test" in text_lower
    ):

        save_personal_memory(
            group_id,
            user_id,
            "exam",
            text
        )

    # favorite
    if (
        "favorite" in text_lower or
        "favourite" in text_lower
    ):

        save_personal_memory(
            group_id,
            user_id,
            "favorite",
            text
        )

    # remember
    if (
        "yaad rakhna" in text_lower or
        "remember this" in text_lower
    ):

        save_personal_memory(
            group_id,
            user_id,
            "important",
            text
        )

    # study personality
    if (
        "padh" in text_lower or
        "study" in text_lower
    ):

        update_personality(
            group_id,
            user_id,
            "study_person"
        )

    # gym meme 😭
    if (
        "kal se" in text_lower
    ):

        add_inside_joke(
            group_id,
            user_id,
            text
        )
