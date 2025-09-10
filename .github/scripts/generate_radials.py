#!/usr/bin/env python3
# .github/scripts/generate_radials.py
"""
Generate two professional radial gauge SVGs (radial-c.svg, radial-cpp.svg)
based on the user's GitHub language stats (C and C++) across all repos.
Language name is printed inside the ring above the percentage.
"""

import os
import sys
import requests
import math
import matplotlib.pyplot as plt

GITHUB_USER = "MohamedShabanElwa3er"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    print("Warning: GITHUB_TOKEN not found in environment. Script will still run but GitHub API calls may fail.")
    # We continue: the script will return zeros if API fails.

def fetch_all_repos(username, token):
    """Fetch all public repos for username with pagination."""
    headers = {"Authorization": f"token {token}"} if token else {}
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Failed to fetch repos (status {resp.status_code}): {resp.text}")
            break
        page_repos = resp.json()
        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1
    return repos

def aggregate_language_counts(repos, token):
    """Aggregate language bytes for C and C++ across repos."""
    totals = {"C": 0, "C++": 0}
    headers = {"Authorization": f"token {token}"} if token else {}
    for r in repos:
        try:
            url = r.get("languages_url")
            if not url:
                continue
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                # skip this repo on error
                continue
            langs = resp.json()
            totals["C"] += langs.get("C", 0)
            totals["C++"] += langs.get("C++", 0)
        except Exception as e:
            # continue on any repo error
            print(f"Warning: repo languages fetch error: {e}", file=sys.stderr)
            continue
    return totals

def compute_percentages(totals):
    c = totals.get("C", 0)
    cpp = totals.get("C++", 0)
    total = c + cpp
    if total <= 0:
        return {"C": 0.0, "C++": 0.0}
    return {"C": (c / total) * 100.0, "C++": (cpp / total) * 100.0}

def create_radial_svg(value, lang_name, filename, color_hex):
    """
    Draw a professional radial gauge (SVG) with:
      - thick dark background ring,
      - colored progress arc,
      - language name inside (top),
      - percentage centered below the name.
    """
    # Figure setup
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': 'polar'})
    # Start at the top and go clockwise
    ax.set_theta_offset(math.pi/2)
    ax.set_theta_direction(-1)

    # Hide grid/labels
    ax.set_axis_off()

    # Draw background ring (full circle)
    full_circle = 2 * math.pi
    ax.barh(1.0, full_circle, left=0.0, height=0.35, color="#16181A", alpha=1.0, edgecolor='none')

    # Draw the progress arc proportional to value
    arc_angle = (value / 100.0) * full_circle
    ax.barh(1.0, arc_angle, left=0.0, height=0.35, color=color_hex, edgecolor='none')

    # Add inner circle (to create donut "hole")
    # Use a white/transparent center by plotting a filled circle on top
    circle = plt.Circle((0, 0), 0.45, transform=ax.transData._b, color="#0d1117", zorder=10)
    ax.add_artist(circle)

    # Put text inside using figure coordinates (reliable positioning)
    # Language name (top), percentage (center)
    # Use fig.text with 0.5,0.56 (slightly above center) and 0.5,0.44 (center)
    lang_label = lang_name
    percent_text = f"{value:.1f}%"

    fig.text(0.5, 0.56, lang_label, ha="center", va="center",
             fontsize=16, fontweight='600', color="#FFFFFF")

    fig.text(0.5, 0.43, percent_text, ha="center", va="center",
             fontsize=30, fontweight='700', color=color_hex)

    # Save as SVG with transparent background
    plt.savefig(filename, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)
    print(f"Saved {filename}")

def main():
    repos = fetch_all_repos(GITHUB_USER, TOKEN)
    totals = aggregate_language_counts(repos, TOKEN)
    perc = compute_percentages(totals)

    # choose colors (feel free to change hex colors)
    create_radial_svg(perc["C"], "C", ".github/radial-c.svg", "#00b4d8")     # cyan
    create_radial_svg(perc["C++"], "C++", ".github/radial-cpp.svg", "#ff006e") # pink

if __name__ == "__main__":
    main()
