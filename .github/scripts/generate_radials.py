import requests
import os
import matplotlib.pyplot as plt

GITHUB_USER = "MohamedShabanElwa3er"
TOKEN = os.getenv("GITHUB_TOKEN")

def get_language_stats():
    headers = {"Authorization": f"token {TOKEN}"}
    repos = requests.get(
        f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100",
        headers=headers
    ).json()

    totals = {"C": 0, "C++": 0}
    for repo in repos:
        langs = requests.get(repo["languages_url"], headers=headers).json()
        for lang, count in langs.items():
            if lang in totals:
                totals[lang] += count

    total_all = sum(totals.values())
    if total_all == 0:
        return {"C": 0, "C++": 0}
    return {lang: round((count / total_all) * 100, 2) for lang, count in totals.items()}

def create_radial_chart(value, label, filename, color):
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(1.57)
    ax.set_theta_direction(-1)

    # Background circle
    ax.barh(1, 2 * 3.1416, left=0, height=0.3, color="#2b2d42", alpha=0.2)

    # Progress arc
    ax.barh(1, (value / 100) * 2 * 3.1416, left=0, height=0.3, color=color)

    # Remove axis
    ax.set_axis_off()

    # Center text
    plt.text(0, 0, f"{value:.1f}%", ha="center", va="center",
             fontsize=20, fontweight="bold", color=color)
    plt.text(0, -0.5, label, ha="center", va="center",
             fontsize=12, color="white")

    plt.savefig(filename, transparent=True)
    plt.close()

if __name__ == "__main__":
    stats = get_language_stats()
    create_radial_chart(stats["C"], "C Projects", "radial-c.svg", "#00b4d8")
    create_radial_chart(stats["C++"], "C++ Projects", "radial-cpp.svg", "#ff006e")
