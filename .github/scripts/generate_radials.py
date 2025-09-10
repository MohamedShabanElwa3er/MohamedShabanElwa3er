import subprocess
import json
import matplotlib.pyplot as plt

def get_language_stats():
    """Run cloc to get language breakdown as JSON"""
    result = subprocess.run(
        ["cloc", "--json", "--quiet", "."],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    stats = {}
    total = 0

    for lang, info in data.items():
        if isinstance(info, dict) and "code" in info:
            stats[lang] = info["code"]
            total += info["code"]

    # Convert to %
    percentages = {lang: round((count / total) * 100, 2) for lang, count in stats.items()}
    return percentages

def create_radial_chart(value, label, filename, color):
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': 'polar'})
    ax.set_theta_offset(1.57)
    ax.set_theta_direction(-1)

    # Background circle
    ax.barh(1, 2 * 3.1416, left=0, height=0.3, color="#2b2d42", alpha=0.2)

    # Progress arc
    ax.barh(1, (value/100) * 2 * 3.1416, left=0, height=0.3, color=color)

    # Remove axis
    ax.set_axis_off()

    # Add % number in center
    plt.text(0, 0, f"{value:.0f}%", ha="center", va="center", fontsize=20, fontweight="bold", color=color)
    plt.text(0, -0.5, label, ha="center", va="center", fontsize=12, color="white")

    plt.savefig(filename, transparent=True)
    plt.close()

if __name__ == "__main__":
    stats = get_language_stats()

    c_value = stats.get("C", 0)
    cpp_value = stats.get("C++", 0)

    create_radial_chart(c_value, "C Projects", "radial-c.svg", "#00b4d8")
    create_radial_chart(cpp_value, "C++ Projects", "radial-cpp.svg", "#ff006e")
