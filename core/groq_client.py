import asyncio
import re
import time

from openai import (
    AsyncOpenAI,
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)

from config import (
    GROQ_API_KEYS,
    GROQ_BASE_URL,
    MODELS,
    TEMPERATURE,
    MAX_TOKENS,
    REQUEST_TIMEOUT,
)

# =========================
# STATE
# =========================

# one client per key, created once (no per-request TCP handshakes)
CLIENTS = [
    AsyncOpenAI(
        api_key=key,
        base_url=GROQ_BASE_URL,
        max_retries=0,
        timeout=REQUEST_TIMEOUT,
    )
    for key in GROQ_API_KEYS
]

# (key_index, model) -> unix time when usable again
COOLDOWNS = {}

# keys that returned 401/403
DEAD_KEYS = set()

# models Groq says don't exist / are decommissioned
DEAD_MODELS = set()

# models that rejected the reasoning params above
NO_EXTRAS = set()

# round-robin pointer so load spreads over every key
_next_key = 0

_models_checked = False
_check_lock = asyncio.Lock()


def _mask(i):

    key = GROQ_API_KEYS[i]

    return f"key#{i + 1}(...{key[-4:]})"


# =========================
# MODEL DISCOVERY
# =========================

async def refresh_available_models():
    """Drop configured models that Groq no longer serves."""

    global _models_checked

    async with _check_lock:

        if _models_checked:
            return

        for i, client in enumerate(CLIENTS):

            try:

                listed = await client.models.list()

                available = {m.id for m in listed.data}

                for model in MODELS:
                    if model not in available:
                        print(f"[MODEL UNAVAILABLE] {model}")
                        DEAD_MODELS.add(model)

                _models_checked = True

                return

            except (AuthenticationError, PermissionDeniedError):

                print(f"[DEAD KEY] {_mask(i)}")
                DEAD_KEYS.add(i)

            except Exception as e:

                print(f"[MODEL LIST FAILED] {_mask(i)}: {e}")
                return


# =========================
# HELPERS
# =========================

def _retry_after(err, default=60):
    """Seconds to wait, taken from Groq's rate-limit headers."""

    try:

        headers = err.response.headers

        value = headers.get("retry-after")

        if value:
            return max(1.0, float(value))

    except Exception:
        pass

    # "Please try again in 7.66s" / "in 2m3.5s"
    m = re.search(r"try again in (?:(\d+)m)?([\d.]+)s", str(err))

    if m:
        return int(m.group(1) or 0) * 60 + float(m.group(2)) + 1

    return default


def _extra_params(model):
    """Keep reasoning short and out of the visible reply."""

    if model in NO_EXTRAS:
        return {}

    if model.startswith("openai/gpt-oss"):
        return {
            "reasoning_effort": "low",
            "extra_body": {"include_reasoning": False},
        }

    if model.startswith("qwen/"):
        return {"extra_body": {"reasoning_format": "hidden"}}

    return {}


def clean_output(text):

    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)

    # reply got cut off while still "thinking" -> unusable
    if "<think>" in text:
        return ""

    return text.strip()


# =========================
# CHAT
# =========================

async def chat(messages):
    """
    Try every (model, key) pair, best model first.
    Returns (reply, model) or (None, None) when everything failed.
    """

    global _next_key

    if not CLIENTS:
        print("[NO GROQ KEYS] set GROQ_API_KEYS in .env")
        return None, None

    await refresh_available_models()

    start = _next_key

    _next_key = (_next_key + 1) % len(CLIENTS)

    for model in MODELS:

        if model in DEAD_MODELS:
            continue

        for step in range(len(CLIENTS)):

            i = (start + step) % len(CLIENTS)

            if i in DEAD_KEYS:
                continue

            if time.time() < COOLDOWNS.get((i, model), 0):
                continue

            client = CLIENTS[i]

            try:

                try:

                    response = await client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=TEMPERATURE,
                        max_completion_tokens=MAX_TOKENS,
                        **_extra_params(model),
                    )

                except BadRequestError as e:

                    if model in NO_EXTRAS or not _extra_params(model):
                        raise

                    # model doesn't support a reasoning param: retry plain
                    print(f"[NO EXTRAS] {model}: {e}")

                    NO_EXTRAS.add(model)

                    response = await client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=TEMPERATURE,
                        max_completion_tokens=MAX_TOKENS,
                    )

                choice = response.choices[0]

                reply = clean_output(choice.message.content)

                if not reply:
                    print(
                        f"[EMPTY REPLY] {model} {_mask(i)} "
                        f"finish={choice.finish_reason}"
                    )
                    continue

                print(f"[OK] {model} via {_mask(i)}")

                return reply, model

            except RateLimitError as e:

                wait = _retry_after(e)

                print(f"[RATE LIMIT] {model} {_mask(i)} for {wait:.0f}s")

                COOLDOWNS[(i, model)] = time.time() + wait

            except (AuthenticationError, PermissionDeniedError) as e:

                print(f"[DEAD KEY] {_mask(i)}: {e}")

                DEAD_KEYS.add(i)

            except NotFoundError as e:

                print(f"[MODEL GONE] {model}: {e}")

                DEAD_MODELS.add(model)

                break

            except APIStatusError as e:

                msg = str(e).lower()

                if "decommissioned" in msg or "model_not_found" in msg:

                    print(f"[MODEL GONE] {model}")

                    DEAD_MODELS.add(model)

                    break

                # 5xx / overloaded: short cooldown, try next key
                print(f"[API ERROR {e.status_code}] {model} {_mask(i)}")

                COOLDOWNS[(i, model)] = time.time() + 20

            except (APITimeoutError, APIConnectionError) as e:

                print(f"[NETWORK] {model} {_mask(i)}: {e}")

            except Exception as e:

                print(f"[UNKNOWN ERROR] {model} {_mask(i)}: {e}")

    return None, None
