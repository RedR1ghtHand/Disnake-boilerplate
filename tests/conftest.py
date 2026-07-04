"""Shared pytest fixtures and test configuration."""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("BOT_TOKEN", "test-token")
os.environ.setdefault("ALLOWED_GUILDS", "")

from bot.config.settings import get_settings


@pytest.fixture(autouse=True)
def reset_settings_cache() -> None:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def bot_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("ALLOWED_GUILDS", "")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
