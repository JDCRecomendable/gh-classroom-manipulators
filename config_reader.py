#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.

import json
import os
import sys


def load_config() -> dict:
    final_config = {}
    if not os.path.isfile("config.json"):
        print("config.json or config.json.DEFAULT not found!", file=sys.stderr)
        print("Please copy config.json from config.json.DEFAULT and fill in the values to proceed.", file=sys.stderr)
        sys.exit(1)
    with open("config.json.DEFAULT", "r") as default_config_file:
        with open("config.json", "r") as config_file:
            default_config = json.load(default_config_file)
            custom_config = json.load(default_config_file)
            final_config = default_config | custom_config
    return final_config
