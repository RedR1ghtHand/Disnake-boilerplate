"""Colored logging with per-layer categories and decorator support."""

from __future__ import annotations

import asyncio
import logging
import sys
from collections.abc import Callable
from enum import StrEnum
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from colorama import Fore, Style, init as colorama_init

from bot.config import settings

P = ParamSpec("P")
R = TypeVar("R")

RESET = Style.RESET_ALL
DIM = Style.DIM


class LogCategory(StrEnum):
    COMMANDS = "commands"
    SERVICES = "services"
    DB = "db"
    UI = "ui"
    CORE = "core"
    CONFIG = "config"
    APP = "app"


CATEGORY_COLORS: dict[LogCategory, str] = {
    LogCategory.COMMANDS: Fore.CYAN,
    LogCategory.SERVICES: Fore.GREEN,
    LogCategory.DB: Fore.YELLOW,
    LogCategory.UI: Fore.MAGENTA,
    LogCategory.CORE: Fore.BLUE,
    LogCategory.CONFIG: Fore.WHITE,
    LogCategory.APP: Fore.LIGHTBLACK_EX,
}

LEVEL_COLORS: dict[str, str] = {
    "DEBUG": Fore.LIGHTBLACK_EX,
    "INFO": Fore.WHITE,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.LIGHTRED_EX,
}

MODULE_CATEGORY_PREFIXES: tuple[tuple[str, LogCategory], ...] = (
    ("bot.commands", LogCategory.COMMANDS),
    ("bot.services", LogCategory.SERVICES),
    ("bot.db", LogCategory.DB),
    ("bot.ui", LogCategory.UI),
    ("bot.core", LogCategory.CORE),
    ("bot.config", LogCategory.CONFIG),
)


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        category = LogCategory(getattr(record, "category", LogCategory.APP))
        category_color = CATEGORY_COLORS.get(category, Fore.WHITE)
        level_color = LEVEL_COLORS.get(record.levelname, Fore.WHITE)

        timestamp = f"{DIM}{self.formatTime(record, '%H:%M:%S')}{RESET}"
        level = f"{level_color}{record.levelname:<8}{RESET}"
        tag = f"{category_color}{category.value:<10}{RESET}"
        name = f"{DIM}{record.name}{RESET}"
        message = record.getMessage()

        return f"{timestamp} {level} {tag} {name} | {message}"


class CategoryLogger(logging.LoggerAdapter[logging.Logger]):
    def process(
        self,
        msg: str,
        kwargs: dict[str, Any],
    ) -> tuple[str, dict[str, Any]]:
        extra = kwargs.setdefault("extra", {})
        extra["category"] = self.extra["category"]
        return msg, kwargs

    def event(self, message: str, *args: object, **kwargs: Any) -> None:
        self.info(message, *args, **kwargs)


def resolve_category(name: str) -> LogCategory:
    for prefix, category in MODULE_CATEGORY_PREFIXES:
        if name.startswith(prefix):
            return category
    return LogCategory.APP


def get_logger(
    name: str,
    *,
    category: LogCategory | str | None = None,
) -> CategoryLogger:
    resolved = LogCategory(category) if category else resolve_category(name)
    base = logging.getLogger(name)
    return CategoryLogger(base, {"category": resolved.value})


def setup_logging() -> None:
    colorama_init()

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    logging.getLogger("disnake").setLevel(logging.WARNING)
    logging.getLogger("disnake.http").setLevel(logging.WARNING)


def logged(
    *,
    category: LogCategory | str | None = None,
    action: str | None = None,
    level: int = logging.DEBUG,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Log function entry and exit. Use ``action`` for UI-style messages."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        logger = get_logger(func.__module__, category=category)
        enter_message = f"> {func.__qualname__}" if action is None else f"> {action}"
        exit_message = f"< {func.__qualname__}" if action is None else f"done: {action}"

        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                logger.log(level, enter_message)
                try:
                    result = await func(*args, **kwargs)
                except Exception:
                    logger.exception("! %s failed", func.__qualname__)
                    raise
                logger.log(level, exit_message)
                return result

            return async_wrapper  # type: ignore[return-value]

        @wraps(func)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            logger.log(level, enter_message)
            try:
                result = func(*args, **kwargs)
            except Exception:
                logger.exception("! %s failed", func.__qualname__)
                raise
            logger.log(level, exit_message)
            return result

        return sync_wrapper

    return decorator


def _category_logger(
    category: LogCategory,
    func_or_action: Callable[P, R] | str | None = None,
    *,
    action: str | None = None,
    level: int = logging.DEBUG,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    def wrap(func: Callable[P, R]) -> Callable[P, R]:
        resolved_action = func_or_action if isinstance(func_or_action, str) else action
        return logged(category=category, action=resolved_action, level=level)(func)

    if callable(func_or_action):
        return wrap(func_or_action)

    return wrap


def log_command(
    func_or_action: Callable[P, R] | str | None = None,
    *,
    action: str | None = None,
    level: int = logging.DEBUG,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    return _category_logger(LogCategory.COMMANDS, func_or_action, action=action, level=level)


def log_service(
    func_or_action: Callable[P, R] | str | None = None,
    *,
    action: str | None = None,
    level: int = logging.DEBUG,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    return _category_logger(LogCategory.SERVICES, func_or_action, action=action, level=level)


def log_db(
    func_or_action: Callable[P, R] | str | None = None,
    *,
    action: str | None = None,
    level: int = logging.DEBUG,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    return _category_logger(LogCategory.DB, func_or_action, action=action, level=level)


def log_ui(
    func_or_action: Callable[P, R] | str | None = None,
    *,
    action: str | None = None,
    level: int = logging.DEBUG,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    return _category_logger(LogCategory.UI, func_or_action, action=action, level=level)
