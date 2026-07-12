import os
import pytest
from pydantic import ValidationError
from app.core.config import Settings

def test_settings_load_from_env(monkeypatch):
    """Test that environment variables are correctly loaded and typed by Settings."""
    monkeypatch.setenv("GROQ_API_KEY", "test_key")
    monkeypatch.setenv("GROQ_MODEL", "test-model")
    monkeypatch.setenv("PORT", "9999")
    monkeypatch.setenv("HOST", "127.0.0.1")
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "true")
    
    settings = Settings(_env_file=None)
    assert settings.GROQ_API_KEY == "test_key"
    assert settings.GROQ_MODEL == "test-model"
    assert settings.PORT == 9999
    assert settings.HOST == "127.0.0.1"
    assert settings.LANGCHAIN_TRACING_V2 == "true"

def test_settings_defaults(monkeypatch):
    """Test that settings fall back to correct defaults if optional vars are omitted."""
    monkeypatch.setenv("GROQ_API_KEY", "test_key")
    monkeypatch.delenv("GROQ_MODEL", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    
    settings = Settings(_env_file=None)
    assert settings.GROQ_MODEL == "llama3-70b-8192"
    assert settings.PORT == 8000
    assert settings.HOST == "0.0.0.0"

def test_settings_missing_required(monkeypatch):
    """Test that a validation error is raised if required variables are missing."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    
    # We must also bypass reading from local .env if it has the key,
    # SettingsConfigDict points to .env, but we can temporarily mock / clear it
    # by testing with Settings model validation directly or setting env to empty.
    # BaseSettings reads environment variables first, then env file.
    # To force error, we can construct Settings with explicit env_file=None (via SettingsConfigDict or overrides)
    # or we can test that if we mock env_file or clear environment variables it fails.
    # Let's verify by patching config or creating a subclass of Settings without env_file to force validation error.
    
    class TestSettings(Settings):
        model_config = {
            "env_file": None,
            "extra": "ignore"
        }
        
    with pytest.raises(ValidationError):
        TestSettings()
