"""Data-plane helpers exposed by the AdaOS SDK."""

from __future__ import annotations

from contextlib import contextmanager

from .bus import BusNotAvailable, emit, get_meta, on
from .context import clear_current_skill, get_current_skill, set_current_skill
from .env import get_audio_out_backend, get_stt_backend, get_tts_backend
from .events import publish
from .fs import open as open  # noqa: A001 - re-export for convenience
from .fs import save_bytes, tmp_path
from .i18n import I18n, _
from .memory import delete, get, list, put
from .secrets import read, write
from .skill_memory import get as skill_memory_get
from .skill_memory import set as skill_memory_set


@contextmanager
def ctx_subnet(_: str):
    """Backwards-compatible no-op subnet context helper.

    Older skills imported :func:`ctx_subnet` but newer SDK versions moved away
    from this API.  Keeping a dummy context manager here prevents import-time
    failures for skills that still reference the symbol while preserving
    runtime behavior (the helper never mutates global state).
    """

    yield


__all__ = [
    "BusNotAvailable",
    "emit",
    "on",
    "get_meta",
    "clear_current_skill",
    "set_current_skill",
    "get_current_skill",
    "publish",
    "tmp_path",
    "save_bytes",
    "open",
    "get",
    "put",
    "delete",
    "list",
    "read",
    "write",
    "I18n",
    "_",
    "skill_memory_get",
    "skill_memory_set",
    "get_tts_backend",
    "get_stt_backend",
    "get_audio_out_backend",
    "ctx_subnet",
]
