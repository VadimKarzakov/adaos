from __future__ import annotations

import sys
from pathlib import Path
from typing import Mapping
import sys
import types
import importlib

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
SRC_DIR = REPO_ROOT / "src"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(SRC_DIR))

# Provide a lightweight YAML stub to satisfy imports in environments without PyYAML.
if "yaml" not in sys.modules:
    yaml_stub = types.SimpleNamespace(
        safe_load=lambda data: {},
        dump=lambda obj: "",
    )
    sys.modules["yaml"] = yaml_stub

if "y_py" not in sys.modules:
    class _DummyYDoc:
        def __init__(self, *_, **__):
            pass

    sys.modules["y_py"] = types.SimpleNamespace(YDoc=_DummyYDoc)

if "adaos.sdk.manage" not in sys.modules:
    sys.modules["adaos.sdk.manage"] = types.ModuleType("adaos.sdk.manage")

if "jsonschema" not in sys.modules:
    class _DummyValidationError(Exception):
        pass

    class _DummyValidator:
        def __init__(self, *_, **__):
            pass

        def validate(self, *_args, **_kwargs):
            return None

    jsonschema_stub = types.SimpleNamespace(
        Draft202012Validator=_DummyValidator,
        ValidationError=_DummyValidationError,
    )
    sys.modules["jsonschema"] = jsonschema_stub

if "anyio" not in sys.modules:
    class _DummyLock:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_, **__):
            return None

    class _DummyEvent:
        def __init__(self):
            pass

        def set(self):
            return None

    anyio_stub = types.ModuleType("anyio")
    anyio_stub.Event = _DummyEvent
    anyio_stub.Lock = _DummyLock
    anyio_stub.TASK_STATUS_IGNORED = object()
    sys.modules["anyio"] = anyio_stub
    sys.modules["anyio.abc"] = types.SimpleNamespace(TaskStatus=object)

if "ypy_websocket.ystore" not in sys.modules:
    class _DummyBaseYStore:
        def __init__(self, *_, **__):
            pass

    class _DummyYDocNotFound(Exception):
        pass

    sys.modules["ypy_websocket.ystore"] = types.SimpleNamespace(
        BaseYStore=_DummyBaseYStore,
        YDocNotFound=_DummyYDocNotFound,
    )

from adaos.sdk.scenarios.runtime import ScenarioRuntime, ScenarioModel, ensure_runtime_context

SCENARIO_DIR = Path(__file__).resolve().parents[1]
BASE_DIR = REPO_ROOT / ".adaos"

try:
    import yaml  # type: ignore

    SCENARIO_PAYLOAD = yaml.safe_load((SCENARIO_DIR / "scenario.yaml").read_text(encoding="utf-8"))
except Exception:
    SCENARIO_PAYLOAD = {
        "id": "morning_routine",
        "version": "0.1.0",
        "name": "Утренний сценарий",
        "description": "Последовательно озвучивает текущее время и погоду.",
        "trigger": "manual",
        "vars": {"greeting": "Доброе утро!"},
        "steps": [
            {
                "name": "get_time",
                "call": "skills.run",
                "args": {"skill": "time_skill", "topic": "nlp.intent.time.get", "payload": {}},
                "save_as": "time",
            },
            {"name": "format_time", "when": "${time.result.ok}", "set": {"time_text": "${time.result.message}"}},
            {"name": "fallback_time", "when": "${not time.result.ok}", "set": {"time_text": "Время недоступно"}},
            {
                "name": "get_weather",
                "call": "skills.run",
                "args": {"skill": "weather_skill", "topic": "nlp.intent.weather.get", "payload": {}},
                "save_as": "weather",
            },
            {
                "name": "format_weather",
                "when": "${weather.result.ok}",
                "set": {
                    "weather_text": "Погода: ${weather.result.description} (${weather.result.temp}°C) в ${weather.result.city}",
                },
            },
            {"name": "fallback_weather", "when": "${not weather.result.ok}", "set": {"weather_text": "${weather.result.error}"}},
            {
                "name": "compose_message",
                "set": {"msg": "Утреннее напоминание:\n${vars.greeting}\n${time_text}\n${weather_text}"},
            },
            {"name": "out_console", "call": "io.console.print", "args": {"text": "${msg}"}},
            {"name": "out_voice", "call": "io.voice.tts.speak", "args": {"text": "${msg}"}},
        ],
    }

if not isinstance(SCENARIO_PAYLOAD, dict) or not SCENARIO_PAYLOAD.get("steps"):
    SCENARIO_PAYLOAD = {
        "id": "morning_routine",
        "version": "0.1.0",
        "name": "Утренний сценарий",
        "description": "Последовательно озвучивает текущее время и погоду.",
        "trigger": "manual",
        "vars": {"greeting": "Доброе утро!"},
        "steps": [
            {
                "name": "get_time",
                "call": "skills.run",
                "args": {"skill": "time_skill", "topic": "nlp.intent.time.get", "payload": {}},
                "save_as": "time",
            },
            {"name": "format_time", "when": "${time.result.ok}", "set": {"time_text": "${time.result.message}"}},
            {"name": "fallback_time", "when": "${not time.result.ok}", "set": {"time_text": "Время недоступно"}},
            {
                "name": "get_weather",
                "call": "skills.run",
                "args": {"skill": "weather_skill", "topic": "nlp.intent.weather.get", "payload": {}},
                "save_as": "weather",
            },
            {
                "name": "format_weather",
                "when": "${weather.result.ok}",
                "set": {
                    "weather_text": "Погода: ${weather.result.description} (${weather.result.temp}°C) в ${weather.result.city}",
                },
            },
            {"name": "fallback_weather", "when": "${not weather.result.ok}", "set": {"weather_text": "${weather.result.error}"}},
            {
                "name": "compose_message",
                "set": {"msg": "Утреннее напоминание:\n${vars.greeting}\n${time_text}\n${weather_text}"},
            },
            {"name": "out_console", "call": "io.console.print", "args": {"text": "${msg}"}},
            {"name": "out_voice", "call": "io.voice.tts.speak", "args": {"text": "${msg}"}},
        ],
    }


def stub_skill_handler(skill: str, topic: str, payload: Mapping[str, object]):
    if skill == "time_skill":
        print("Сейчас 09:00")
        return {"ok": True, "time": "09:00", "message": "Сейчас 09:00"}

    if skill == "weather_skill":
        print("В Москве ясно, 18°C")
        return {
            "ok": True,
            "city": payload.get("city", "Москва"),
            "temp": 18,
            "description": "ясно",
            "message": "В Москве ясно, 18°C",
        }

    raise RuntimeError(f"unexpected skill call: {skill} / {topic}")


@pytest.fixture(autouse=True)
def _setup_runtime(monkeypatch):
    ensure_runtime_context(BASE_DIR)
    monkeypatch.setenv("ADAOS_BASE_DIR", str(BASE_DIR))
    monkeypatch.setenv("ADAOS_SKILL_RUNTIME_ENV", "dev")

    target_module = importlib.import_module("adaos.services.skill.runtime")
    monkeypatch.setattr(target_module, "run_skill_handler_sync", stub_skill_handler)


def test_morning_routine_generates_message():
    runtime = ScenarioRuntime()
    scenario = ScenarioModel.from_payload(SCENARIO_PAYLOAD, fallback_id="morning_routine")

    result = runtime.run(scenario)

    assert "Доброе утро!" in result.get("msg", "")
    assert "Сейчас 09:00" in result.get("msg", "")
    assert "Погода: ясно" in result.get("msg", "")


def test_scenario_records_step_results():
    runtime = ScenarioRuntime()
    scenario = ScenarioModel.from_payload(SCENARIO_PAYLOAD, fallback_id="morning_routine")

    result = runtime.run(scenario)

    steps = result.get("steps", {})
    assert "get_time" in steps
    assert "get_weather" in steps
    assert result.get("time_text") == "Сейчас 09:00"
    assert result.get("weather_text") == "Погода: ясно (18°C) в Москва"

