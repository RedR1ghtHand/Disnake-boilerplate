# Discord Bot Boilerplate

A cake base for Discord bots with [Disnake](https://docs.disnake.dev/), MongoDB, and a layered architecture. With a pinch of colored logging, Docker support, and pytest scaffolding.

## Tech Stack

- **Discord** - Disnake
- **Database** - MongoDB (PyMongo)
- **Config** - pydantic-settings + `.env`
- **Package manager** - [UV](https://docs.astral.sh/uv/)
- **Testing** - Pytest

## Project Structure

```
discord-bot-boilerplate/
├── main.py                     # Entry point
├── Dockerfile
├── docker-compose.yml          # Bot only (Atlas / external MongoDB)
├── docker-compose.local.yml    # Optional local MongoDB overlay
├── tests/
│   ├── conftest.py
│   ├── integration/
│   └── factories/
└── bot/
    ├── core.py                 # Bot instance + lifecycle
    ├── log.py                  # Colored category logging
    ├── config/                 # Settings, intents, guilds
    ├── commands/               # Slash commands, listeners, cogs
    ├── services/               # Business logic
    ├── ui/                     # Embeds, views, modals
    └── db/
        ├── session.py          # MongoDB connection
        ├── models/
        ├── repositories/
        └── migrations/         # Index setup, data scripts
```

## Architecture

```
Discord interaction
  → commands/       parse input, check permissions
  → services/       business rules
  → db/repositories/  read/write data
  → ui/             build embed/view response
```

| Layer | Responsibility |
|-------|----------------|
| `commands/` | Handle Discord interactions |
| `services/` | Business logic, orchestration |
| `db/repositories/` | CRUD and queries only |
| `ui/` | Embeds, views, message templates |
| `config/` | Static deployment settings from `.env` |

## Quick Start

### Prerequisites

- Python 3.11+
- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- A [Discord bot token](https://discord.com/developers/applications)

### Setup

```bash
git clone <your-repo-url>
cd discord-bot-boilerplate

cp .env.example .env
# Edit .env - set BOT_TOKEN at minimum

uv sync
uv run python main.py
```

### Logging demo

Preview all log levels, category colors, and decorators without connecting to Discord:

```bash
uv run python main.py --demo-only
```

Demo logging, then start the bot:

```bash
uv run python main.py --demo-logging
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | Yes | Discord bot token |
| `ALLOWED_GUILDS` | No | Comma-separated guild IDs for fast slash-command sync during dev |
| `ENVIRONMENT` | No | `development` / `production` (default: `development`) |
| `LOG_LEVEL` | No | `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`) |
| `MEMBERS_INTENT` | No | Privileged intent - also enable in Developer Portal |
| `PRESENCES_INTENT` | No | Privileged intent - also enable in Developer Portal |
| `MESSAGE_CONTENT_INTENT` | No | Privileged intent (default: `true`) |
| `MONGODB_URI` | No | MongoDB connection string |
| `MONGODB_DATABASE` | No | Database name (default: `bot`) |

### MongoDB connection examples

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/

# Local MongoDB
MONGODB_URI=mongodb://localhost:27017

# Docker local mongo overlay (set automatically by compose.local.yml)
MONGODB_URI=mongodb://mongo:27017
```

## Docker

### Atlas / external MongoDB

Set `MONGODB_URI` in `.env` to your Atlas or remote connection string, then:

```bash
docker compose up --build
docker compose up -d
docker compose logs -f bot
docker compose down
```

### Local MongoDB in Docker

Adds a `mongo` service and overrides `MONGODB_URI` to `mongodb://mongo:27017`:

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
docker compose -f docker-compose.yml -f docker-compose.local.yml down
docker compose -f docker-compose.yml -f docker-compose.local.yml down -v   # + wipe volume
```

## Logging

Colored logs per layer - category is auto-detected from the module path:

| Category | Color | Module prefix |
|----------|-------|---------------|
| `commands` | cyan | `bot.commands.*` |
| `services` | green | `bot.services.*` |
| `db` | yellow | `bot.db.*` |
| `ui` | magenta | `bot.ui.*` |
| `core` | blue | `bot.core` |

```python
from bot.log import get_logger, log_command, log_service, log_db, log_ui

logger = get_logger(__name__)
logger.info("Something happened")

@log_ui("help embed sent")
async def send_help_embed(inter, embed):
    await inter.response.send_message(embed=embed)
```

## Testing

```bash
uv sync --group dev
uv run pytest
```

Add tests as `tests/test_<feature>.py`. Integration tests that need MongoDB go in `tests/integration/`.

## Adding Features

| Task | Location |
|------|----------|
| Slash command | `bot/commands/` |
| Business logic | `bot/services/` |
| Embed / view | `bot/ui/` |
| MongoDB model | `bot/db/models/` |
| Database query | `bot/db/repositories/` |
| Env variable | `bot/config/settings.py` + `.env.example` |
| Discord intents | `bot/config/intents.py` |

## MongoDB Migrations

MongoDB is schemaless - you don't need SQL-style migrations. Use `bot/db/migrations/` for:

- Index creation
- One-off data transformations

## License

MIT
