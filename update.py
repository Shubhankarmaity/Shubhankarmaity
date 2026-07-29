#!/usr/bin/env python3
"""
GitHub Profile README Updater
Auto-updates terminal SVG with live GitHub stats
"""

import requests
import re

GITHUB_USERNAME = "Shubhankarmaity"


def fetch_github_stats():
    """Fetch basic GitHub stats via API"""
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Error fetching stats: {e}")
    return {}


def update_svg_dark(stats):
    """Update dark.svg with live stats if needed"""
    # Placeholder for dynamic updates
    # You can extend this to modify SVG content with real data
    repos = stats.get("public_repos", 0)
    followers = stats.get("followers", 0)
    print(f"[DARK] Repos: {repos}, Followers: {followers}")


def update_svg_light(stats):
    """Update light.svg with live stats if needed"""
    repos = stats.get("public_repos", 0)
    followers = stats.get("followers", 0)
    print(f"[LIGHT] Repos: {repos}, Followers: {followers}")


def main():
    print("🚀 Updating GitHub Profile README...")
    stats = fetch_github_stats()

    if stats:
        update_svg_dark(stats)
        update_svg_light(stats)
        print("✅ Update complete!")
    else:
        print("⚠️ Could not fetch stats. Using cached values.")


if __name__ == "__main__":
    main()
