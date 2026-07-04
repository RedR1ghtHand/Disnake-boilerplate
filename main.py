"""Application entry point. Starts the Discord bot."""

from __future__ import annotations

import argparse

from bot.core import run_bot
from bot.log import setup_logging
from bot.log_demo import run_log_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Discord bot boilerplate")
    parser.add_argument(
        "--demo-logging",
        action="store_true",
        help="Print all log levels, categories, and decorators before starting",
    )
    parser.add_argument(
        "--demo-only",
        action="store_true",
        help="Run logging demo and exit (no bot connection)",
    )
    args = parser.parse_args()

    setup_logging()

    if args.demo_logging or args.demo_only:
        run_log_demo()

    if args.demo_only:
        return

    run_bot()


if __name__ == "__main__":
    main()
