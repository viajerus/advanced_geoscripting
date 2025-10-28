#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Description"""

from pathlib import Path

import yaml


def load_config(config_file):
    """Load configuration from a YAML file."""

    # Ensure the config_file is a Path object
    if not isinstance(config_file, Path):
        config_file = Path(config_file)

    assert config_file.exists(), (
        f"Configuration file does not exist: {config_file.absolute()}"
    )

    # Check if the file exists
    with open(config_file, "r") as src:
        config = yaml.safe_load(src)

    return config
