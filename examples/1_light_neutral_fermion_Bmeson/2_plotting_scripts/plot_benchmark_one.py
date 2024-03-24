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

    data_dir = pathlib.Path("../3_plots/data_points/")
    plot_file = pathlib.Path("../3_plots/benchmark_one.pdf")
    plot_style = "one"

    data_dict = func.load_data(data_dir)

    func.draw_plot(data_dict, plot_style)
    plot_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_file, format="pdf", bbox_inches="tight", dpi=200)
