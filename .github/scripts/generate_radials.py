import matplotlib.pyplot as plt
import numpy as np

# Example data (replace with real analysis later)
languages = {
    "C": 45,
    "C++": 35,
    "Rust": 15,
    "Other": 5,
}

# Colors (neon style)
colors = ["#00f7ff", "#ff2e63", "#f7ff00", "#9b59b6"]

# Create figure
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
fig.patch.set_facecolor("#0d1117")  # GitHub dark background
ax.set_facecolor("#0d1117")
ax.set_xticks([])
ax.set_yticks([])
ax.spines.clear()

# Draw arcs
start_angle = 0
for (lang, value), color in zip(languages.items(), colors):
    end_angle = start_angle + (value / 100) * 2 * np.pi
    ax.barh(
        y=1, width=end_angle - start_angle,
        left=start_angle, height=0.3,
        color=color, edgecolor="white", linewidth=2
    )
    start_angle = end_angle

# Add numeric total in the center
total = sum(languages.values())
ax.text(0, 0, f"{total}%", ha="center", va="center",
        fontsize=28, fontweight="bold", color="white")

# Save SVG
plt.savefig("radial-all.svg", format="svg", bbox_inches="tight", transparent=True)
