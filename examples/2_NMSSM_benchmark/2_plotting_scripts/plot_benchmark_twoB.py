#!env python

import os
import pathlib
import sys  # Basic functions

import functions as func
import matplotlib as mpl  # Plotting module
import matplotlib.pyplot as plt  # Plotting module

if __name__ == "__main__":
    # Setting Matplotlib backend as non-interactive, necessary for use in Linus
    mpl.use("Agg")

    data_dir = pathlib.Path("../3_plots/data_pointsB/")
    plot_file = pathlib.Path("../3_plots/benchmark_twoB.pdf")
    plot_style = "twoB"

    data_dict = func.load_data(data_dir)
    # skip detectors with very low sensitivity for certain benchmarks
    data_dict.pop("FASER", None)

    func.draw_plot(data_dict, plot_style)
    plot_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_file, format="pdf", bbox_inches="tight", dpi=200)
