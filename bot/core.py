"""Bot instance and lifecycle (startup, extension loading)."""

from disnake.ext import commands

from bot.config import build_intents, get_allowed_guilds, settings
from bot.log import get_logger

logger = get_logger(__name__)

intents = build_intents()
allowed_guilds = get_allowed_guilds()

bot = commands.InteractionBot(intents=intents, test_guilds=allowed_guilds)


@bot.event
async def on_ready() -> None:
    logger.info("Logged in as %s (%s)", bot.user, bot.user.id)


def run_bot() -> None:
    logger.info("Starting bot in %s mode", settings.environment)
    bot.run(settings.bot_token)
