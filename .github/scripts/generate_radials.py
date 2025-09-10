import matplotlib.pyplot as plt

def make_radial(filename, data, title):
    labels, sizes = zip(*data)
    colors = plt.cm.Set3(range(len(data)))

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(aspect="equal"))

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%1.0f%%",
        pctdistance=0.8,
        startangle=90,
        colors=colors,
        wedgeprops=dict(width=0.35, edgecolor="w")
    )

    plt.setp(autotexts, size=12, weight="bold", color="black")
    ax.set_title(title, fontsize=14, weight="bold")
    plt.savefig(filename, format="svg", bbox_inches="tight")
    plt.close()

# Example data (replace with real stats later)
c_data = [("Project A", 40), ("Project B", 30), ("Project C", 30)]
cpp_data = [("Proj X", 50), ("Proj Y", 25), ("Proj Z", 25)]
all_data = [("C", 45), ("C++", 35), ("Other", 20)]

make_radial("radial-c.svg", c_data, "C Projects")
make_radial("radial-cpp.svg", cpp_data, "C++ Projects")
make_radial("radial-all.svg", all_data, "Overall Projects")
