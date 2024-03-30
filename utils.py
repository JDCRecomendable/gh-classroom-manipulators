#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# Copyright (c) 2023-2024 Jared Daniel Recomendable.


import requests


def get_github_api_result_page(url, api_key=None, page=None, per_page=None) -> requests.Response:
    headers = {}
    if api_key:
        headers["Authorization"] = f"Token {api_key}"
    if type(page) == int and page > 1:
        url = f"{url}?page={page}"
    if type(per_page) == int and per_page > 1:
        symbol = "&" if "?page=" in url else "?"
        url = f"{url}{symbol}per_page={per_page}"
    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        return result
    else:
        raise Exception(f"Error: {result.status_code}")
