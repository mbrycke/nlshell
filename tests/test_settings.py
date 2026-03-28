import nlshell.settings as settings


def clear_config_cache():
    settings.get_config.cache_clear()


def test_set_config_and_get_config(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_FILE_PATH", str(tmp_path / "settings.ini"))
    clear_config_cache()

    settings.set_config("default", "disable_warning", "True")

    assert settings.get_config("default", "disable_warning") == "True"


def test_get_model_mode_defaults_to_ollama_local(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_FILE_PATH", str(tmp_path / "settings.ini"))
    clear_config_cache()

    assert settings.get_model_mode() == "ollama-local"


def test_get_base_url_uses_model_specific_section(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_FILE_PATH", str(tmp_path / "settings.ini"))
    clear_config_cache()
    settings.set_config("open-router", "base_url", "https://openrouter.example/v1")

    assert settings.get_base_url("open-router") == "https://openrouter.example/v1"


def test_get_base_url_prompts_and_persists_to_selected_section(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_FILE_PATH", str(tmp_path / "settings.ini"))
    clear_config_cache()
    monkeypatch.setattr("builtins.input", lambda _: "https://openrouter.example/v1")

    assert settings.get_base_url("open-router") == "https://openrouter.example/v1"
    clear_config_cache()
    assert (
        settings.get_config("open-router", "base_url")
        == "https://openrouter.example/v1"
    )


def test_get_model_prompts_and_persists_to_selected_section(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "SETTINGS_FILE_PATH", str(tmp_path / "settings.ini"))
    clear_config_cache()
    monkeypatch.setattr("builtins.input", lambda _: "openai/gpt-oss-120b")

    assert settings.get_model("open-router") == "openai/gpt-oss-120b"
    clear_config_cache()
    assert settings.get_config("open-router", "model") == "openai/gpt-oss-120b"


def test_get_api_key_reads_environment(monkeypatch):
    monkeypatch.setenv("NLSHELL_API_KEY", "test-key")

    assert settings.get_api_key() == "test-key"


def test_get_api_key_raises_when_missing(monkeypatch):
    monkeypatch.delenv("NLSHELL_API_KEY", raising=False)

    try:
        settings.get_api_key()
    except ValueError as exc:
        assert "NLSHELL_API_KEY is not set" in str(exc)
    else:
        raise AssertionError("Expected get_api_key to raise ValueError")
