"""Environment-backed runtime settings for IPO Oracle."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().casefold() in {"1", "true", "yes", "on"}


def get_int_env(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def get_float_env(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)))
