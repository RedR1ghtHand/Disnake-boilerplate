"""Allowed guild IDs from env. Passed to Disnake as test_guilds for fast slash-command sync."""

from bot.config.settings import get_settings


def get_allowed_guild_ids() -> list[int]:
    return get_settings().allowed_guilds


def get_allowed_guilds() -> list[int] | None:
    guild_ids = get_allowed_guild_ids()
    return guild_ids or None
