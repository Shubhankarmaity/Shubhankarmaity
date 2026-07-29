#!/usr/bin/env python3
"""
update.py
Refreshes the public repo/follower counts inside README.md between
the markers below, so the profile stays current. Meant to be run on
a schedule via GitHub Actions (see .github/workflows/update-readme.yml).

Add these markers anywhere in README.md where you want live numbers:
    <!--STATS:START--> ... <!--STATS:END-->
"""

import re
import requests

USERNAME = "Shubhankarmaity"
README_PATH = "README.md"
START, END = "<!--STATS:START-->", "<!--STATS:END-->"


def fetch_profile():
    r = requests.get(f"https://api.github.com/users/{USERNAME}", timeout=10)
    r.raise_for_status()
    return r.json()


def build_block(data):
    return (
        f"{START}\n"
        f"**Public repos:** {data['public_repos']} &nbsp;|&nbsp; "
        f"**Followers:** {data['followers']} &nbsp;|&nbsp; "
        f"**Following:** {data['following']}\n"
        f"{END}"
    )


def main():
    data = fetch_profile()
    block = build_block(data)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(block, content)
    else:
        content += "\n\n" + block + "\n"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("README.md stats updated.")


if __name__ == "__main__":
    main()
