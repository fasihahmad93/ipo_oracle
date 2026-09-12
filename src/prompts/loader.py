"""Prompt loading with validation for YAML prompt definitions."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_prompt_template(prompt_name: str) -> str:
    prompt_path = Path(__file__).with_name(f"{prompt_name}.yaml")
    with prompt_path.open(encoding="utf-8") as prompt_file:
        prompt_definition = yaml.safe_load(prompt_file)

    template = prompt_definition.get("template") if isinstance(prompt_definition, dict) else None
    if not isinstance(template, str) or not template.strip():
        raise ValueError(f"Prompt file {prompt_path} must define a non-empty 'template'.")
    return template
