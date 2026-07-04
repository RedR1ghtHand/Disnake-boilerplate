"""Configuration package. Re-exports settings, intents, and guild helpers."""

from bot.config.guilds import get_allowed_guild_ids, get_allowed_guilds
from bot.config.intents import build_intents
from bot.config.settings import Settings, get_settings, settings

__all__ = [
    "Settings",
    "build_intents",
    "get_allowed_guild_ids",
    "get_allowed_guilds",
    "get_settings",
    "settings",
]
