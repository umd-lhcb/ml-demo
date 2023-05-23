#!/usr/bin/env python3

import sys

import hist
import numpy as np

from termcolor import cprint
from scipy.optimize import leastsq
from matplotlib.figure import Figure


def fit_gauss(xi, yi, verbose=False):
    fitfunc = lambda p, x: p[0] * np.exp(-0.5 * ((x - p[1]) / p[2]) ** 2) + p[3]
    errfunc = lambda p, x, y: (y - fitfunc(p, x))

    init = [yi.max(), xi[yi.argmax()], 30, 0.01]
    fit_result, fit_cov = leastsq(errfunc, init, args=(xi, yi))
    if verbose:
        print(
            "Init values 1: coeff = %.2f, mean = %.2f, sigma = %.2f, offset = %.2f"
            % tuple(init)
        )
        print(
            "Fit results 1: coeff = %.2f, mean = %.2f, sigma = %.2f, offset = %.2f"
            % tuple(fit_result)
        )

    # redo fit just taking 2*sigma around the peak
    mask = np.logical_and(
        xi > (fit_result[1] - 1.5 * abs(fit_result[2])),
        xi < (fit_result[1] + 1.5 * abs(fit_result[2])),
    )
    xi2, yi2 = xi[mask], yi[mask]
    fit_result, fit_cov = leastsq(errfunc, fit_result, args=(xi2, yi2))
    # print("Fit results: coeff = %.2f, mean = %.2f, sigma = %.2f, offset = %.2f" % tuple(fit_result))
    return fit_result, fitfunc(fit_result, xi2), mask


def plot_resolution(tag, y_pred, y_true, y_ref=None):
    sigma_dnn = y_pred - y_true

    xmin, xmax, xlabel = -100, 350, "True - Predicted"
    if y_true.sum() == 0:
        xmin, xmax, xlabel = 50, 250, "Higgs mass [GeV]"

    hsigma = hist.Hist(
        "Events",
        hist.Cat("method", "Reco method"),
        hist.Bin("sigma", xlabel, 100, xmin, xmax),
    )
    hsigma.fill(method="DNN", sigma=sigma_dnn)

    if y_ref is not None:
        sigma_cb = y_ref - y_true
        hsigma.fill(method="CB", sigma=sigma_cb)

    fig = Figure()
    ax = hist.plot1d(hsigma, overlay="method", stack=False)
    fit_result, gauss, mask = fit_gauss(
        hsigma.axes["sigma"].centers(), hsigma.values()[("DNN",)]
    )
    print("DNN mean = %.2f, std = %.2f" % tuple(fit_result[1:3]))

    ax.plot(
        hsigma.axes["sigma"].centers()[mask],
        gauss,
        color="maroon",
        linewidth=1,
        label=r"Fitted function",
    )
    if y_ref is not None:
        fit_result, gauss, mask = fit_gauss(
            hsigma.axes["sigma"].centers(), hsigma.values()[("CB",)]
        )
        print("Ref. mean = %.2f,x std = %.2f" % tuple(fit_result[1:3]))
        ax.plot(
            hsigma.axes["sigma"].centers()[mask],
            gauss,
            color="navy",
            linewidth=1,
            label=r"Fitted function",
        )
    filename = "sigma_" + tag + ".pdf"
    fig.savefig(filename)
    cprint("imgcat " + filename, "green")
    return


def plot_mhiggs(tag, y1, label1, y2, label2, title=""):
    fig = Figure()
    hmh = hist.Hist(
        "Events",
        hist.Cat("process", title),
        hist.Bin("mhiggs", "Higgs mass [GeV]", 60, 0, 300),
    )
    hmh.fill(process=label1, mhiggs=y1)
    hmh.fill(process=label2, mhiggs=y2)
    ax = hist.plot1d(hmh, overlay="process", stack=False)
    filename = tag + ".pdf"
    fig.savefig(filename)
    cprint("imgcat " + filename, "green")
    return


def find_max_eff(tag, y_pred, y_true, mass_window_width=40):
    sigma_dnn = y_pred - y_true

    nevents = sigma_dnn.size
    xmin, xmax, bin_width = (-100, 100, 1) if y_true.sum() != 0 else (50, 250, 1)
    if mass_window_width % bin_width > 0:
        sys.exit("eval_dnn::find_max_eff() Mass window must be divisible by bin width")
    counts, edges = np.histogram(
        sigma_dnn, bins=int((xmax - xmin) / bin_width), range=(xmin, xmax)
    )

    # find window that would contain the most events
    isum = counts[0:mass_window_width].sum()
    max_sum = isum
    mass_window_pos = xmin + mass_window_width / 2.0
    for i in range(len(counts)):
        prev_bin, next_bin = i, i + int(mass_window_width / bin_width)
        if next_bin >= len(counts):
            break
        isum += counts[next_bin] - counts[prev_bin]
        if isum > max_sum:
            max_sum = isum
            mass_window_pos = xmin + i * bin_width + mass_window_width / 2.0

    sig_eff = float(max_sum) / nevents * 100.0
    print(
        "--> Max. eff.: {:>10s}, sig. eff = {:.0f}%, peak pos = {:.0f} (width = {:.0f})".format(
            tag, sig_eff, mass_window_pos, mass_window_width
        )
    )
    return sig_eff, mass_window_pos
