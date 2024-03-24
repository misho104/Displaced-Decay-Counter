#!/usr/bin/env python
import matplotlib as mpl  # Plotting module
import matplotlib.pyplot as plt  # Plotting module

default_font = {
    "family": "serif",
    "style": "normal",
    "variant": "normal",
    "weight": "light",
    "size": 16,
}

_detector_styles = {
    "ANUBIS0": ("#005AC8", "--", r"ANUBIS0, 3 ab$^{-1}$"),  # blue
    "ANUBIS1": ("#005AC8", "-", r"ANUBIS, 3 ab$^{-1}$"),  # blue
    "AL3X": ("#00A0FA", "-", r"AL3X, 250 fb$^{-1}$"),  # pink
    "CODEXB0": ("#AA0A3C", "--", r"CODEX-b0, 300 fb$^{-1}$"),  # orange
    "CODEXB1": ("#AA0A3C", "-", r"CODEX-b, 300 fb$^{-1}$"),  # orange
    "FACET": ("#000000", "-", r"FACET, 3 ab$^{-1}$"),  # brown
    "FASER": ("#FA78FA", "-", r"FASER, 150 fb$^{-1}$"),  # green
    "FASER2": ("#ff0505", "-", r"FASER2, 3 ab$^{-1}$"),  # green
    "MAPP1": ("#0A9B4B", "-", r"MAPP1, 30 fb$^{-1}$"),  # red
    "MAPP2": ("#FF825F", "-", r"MAPP2, 300 fb$^{-1}$"),  # red
    "MATHUSLA0": ("#a39103", "--", r"MATHUSLA0, 3 ab$^{-1}$"),  # yellow
    "MATHUSLA1": ("#a39103", "-", r"MATHUSLA, 3 ab$^{-1}$"),  # yellow
    "MATHUSLA2": ("#a39103", "-.", r"MATHUSLA2, 3 ab$^{-1}$"),  # yellow
}


def detector_styles(detector):
    # Returns plot styles for detectors: hex color,  line style, and LaTeX legend-label
    color, linestyle, label = _detector_styles.get(detector, ("", "", ""))
    return {"color": color, "linestyle": linestyle, "label": label}


def load_data(data_dir):
    data = {}
    if not data_dir.is_dir():
        raise RuntimeError("data_dir is not directory", data_dir)
    for child in data_dir.iterdir():
        if not child.is_file():
            continue
        if not child.suffix == ".dat":  # Skip it, if it is the wrong file
            continue
        detector_name = child.stem
        print(f"\tReading {child}\t> {detector_name}")

        content_text = child.read_text()
        content = {"ctau": [], "value": []}
        for line in content_text.splitlines():
            tokens = line.split("\t")
            if len(tokens) == 1:
                continue
            content["ctau"].append(float(tokens[0]))
            content["value"].append(float(tokens[1]))
        # skip if the file is empty
        if len(content["ctau"]) == 0:
            continue
        content.update(detector_styles(detector_name))
        data[detector_name] = content
    return data


def draw_plot(data_dict, plot_style, font=default_font):
    # Setting regarding the typewriting of axis and label
    plt.rc("text", usetex=True)
    plt.rc("font", **font)
    mpl.rc("font", **font)

    # Setting plots
    fig = plt.figure(num=None, figsize=(5, 4), dpi=300, facecolor="w", edgecolor="k")
    ax = fig.add_subplot(1, 1, 1)

    # Plotting each detector
    for name in sorted(data_dict.keys()):
        print("Plotting " + name)
        value = data_dict[name]
        plt.loglog(
            value["ctau"],
            value["value"],
            color=value["color"],
            linestyle=value["linestyle"],
            linewidth=1,
            label=value["label"],
        )

    # make up and filename
    plot_make_up(ax, plot_style)


def plot_make_up(ax, plot_style):
    print(f"decorating with plot style {plot_style}")
    major = mpl.ticker.LogLocator(subs=(0.1, 1.0), numticks=100)
    minor = mpl.ticker.LogLocator(subs=[i / 10 for i in range(1, 10)], numticks=100)
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(major)
    ax.xaxis.set_minor_locator(minor)
    ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())

    major = mpl.ticker.LogLocator(subs=(0.1, 1.0), numticks=100)
    minor = mpl.ticker.LogLocator(subs=[i / 10 for i in range(1, 10)], numticks=100)
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(major)
    ax.yaxis.set_minor_locator(minor)
    ax.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())

    # Labels
    if plot_style == "one":
        plt.xlabel(r"c$\tau_{N}$ [m]")
        plt.ylabel(r"Br$(B^+/B^0 \to e^+/\bar{\nu}_e   N)$")
        plt.title(r"$m_N=1$~GeV")
        plt.axis([1e-2, 1e7, 1e-13, 1e-5])
        plt.legend(loc="lower right", prop={"size": 7})
    elif plot_style in ["twoA", "twoB"]:
        if plot_style == "twoA":
            bound_y = 4.08 / 0.06
            title = r"$M_{A}=410$~GeV,\,\,$M_{A_S}=70$~GeV"
        else:
            bound_y = 1.26 / 0.06 / 0.66
            title = r"$M_{A}=500$~GeV,\,\,$M_{A_S}=200$~GeV"
        plt.xlabel(r"c$\tau_{A_S}$ [m]")
        plt.ylabel(r"$\sigma (pp\rightarrow A\rightarrow A_S\,h_{\mathrm{SM}})$ [fb]")
        # ($ggF\rightarrow A\rightarrow h+A_s$)
        plt.axhline(bound_y, color="black", linestyle="--", linewidth=1.75)
        plt.title(title)
        plt.axis([1e-2, 1e7, 1e-1, 1e7])
        plt.legend(loc="lower right", prop={"size": 7})
    elif plot_style == "three":
        plt.axhline(3.0, color="black", linestyle="--", linewidth=2.25)
        plt.xlabel(r"c$\tau_{\tilde{\chi}^0_1}$ [m]")
        plt.ylabel(r"Signal Events")  # ($ggF\rightarrow A\rightarrow h+A_s$)
        # plt.ylabel(r'Br($\tilde{l}_L \rightarrow e^+\tilde{\chi}^0_1$)')
        plt.title(r"$m_{\tilde{e}_R}=500$~GeV,\,\,$m_{\tilde{\chi}^0_1}=1$~GeV")
        plt.axis([1e-4, 1e4, 1e-4, 1e4])
        plt.legend(loc="upper right", prop={"size": 7})

    # Plot a grid
    plt.grid(
        color="black", which="major", axis="x", alpha=0.5, linestyle="--", linewidth=0.5
    )
    # plt.grid(color='black',which='minor',axis='x',alpha=0.25,linestyle=':',linewidth=0.25)
    plt.grid(
        color="black", which="major", axis="y", alpha=0.5, linestyle="--", linewidth=0.5
    )
    # plt.grid(color='black',which='minor',axis='y',alpha=0.25,linestyle=':',linewidth=0.25)
