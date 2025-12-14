"""Simple time skill for local development scenarios."""

from __future__ import annotations

from datetime import datetime
from typing import Dict

from adaos.sdk.core.decorators import subscribe, tool
from adaos.sdk.data.bus import emit


def _now_text() -> str:
    return datetime.now().strftime("%H:%M")


@tool("get_time")
def get_time() -> Dict:
    current = _now_text()
    message = f"Сейчас {current}"
    print(message)
    return {"ok": True, "time": current, "message": message}


@subscribe("nlp.intent.time.get")
async def on_time_intent(evt) -> None:
    payload = get_time()
    await emit(
        "ui.notify",
        {"text": payload["message"]},
        actor=evt.actor,
        source="time_skill",
        trace_id=evt.trace_id,
    )
