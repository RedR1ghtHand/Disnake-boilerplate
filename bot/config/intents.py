"""Discord gateway intents. Privileged flags are read from settings."""

import disnake

from bot.config.settings import get_settings


def build_intents() -> disnake.Intents:
    settings = get_settings()
    intents = disnake.Intents.none()

    intents.guilds = True
    intents.voice_states = True

    intents.members = settings.members_intent
    intents.presences = settings.presences_intent
    intents.message_content = settings.message_content_intent

    return intents
