def test_handle_prints_current_time(monkeypatch, capsys):
    import skills.time_skill.handlers.main as time_main

    monkeypatch.setattr(time_main, "_now_text", lambda: "12:34")

    time_main.handle("nlp.intent.time.get", {})

    captured = capsys.readouterr()
    assert "Сейчас 12:34" in captured.out
