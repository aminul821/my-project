"""
Check every Groq key and model before running the bot.

    python check_groq.py

Shows which models each key can see, then sends one tiny test
prompt per configured model so you know what actually works.
"""

import asyncio
import time

from core.groq_client import CLIENTS, _extra_params, clean_output, _mask
from config import MODELS


async def main():

    if not CLIENTS:
        print("No keys. Set GROQ_API_KEYS in .env")
        return

    for i, client in enumerate(CLIENTS):

        print(f"\n===== {_mask(i)} =====")

        try:
            listed = await client.models.list()
        except Exception as e:
            print(f"  KEY FAILED: {e}")
            continue

        available = sorted(m.id for m in listed.data)

        print("  Available chat models:")
        for m in available:
            if "whisper" in m or "tts" in m or "guard" in m:
                continue
            mark = "*" if m in MODELS else " "
            print(f"   {mark} {m}")

        for model in MODELS:

            if model not in available:
                print(f"  [MISSING] {model}")
                continue

            t = time.time()

            try:
                r = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Reply with just: ok"}],
                    max_completion_tokens=200,
                    **_extra_params(model),
                )
                out = clean_output(r.choices[0].message.content)
                print(f"  [OK {time.time() - t:.1f}s] {model} -> {out!r}")
            except Exception as e:
                print(f"  [FAIL] {model}: {e}")


asyncio.run(main())
