"""Compute the power spectrum"""
from logging import getLogger
from numpy import argmax, empty, asanyarray, array, not_equal, nonzero, diff, append

from ..spectrum import compute_timefreq, get_chan, get_chantime
from ..viz import plot_tfr, plot_tfr_time, to_div, to_html, plot_surf
from ..read import load
from ..utils import find_max_point
from ..names import name

from wonambi.trans import math

lg = getLogger(__name__)


def pipeline_spectrum(parameters, ieeg_file):
    """Run pipeline to compute power spectrum on one participant, one run

    Parameters
    ----------
    """
    data, names = load('data', parameters, ieeg_file, parameters['spectrum']['read'])

    try:
        elec = load('electrodes', parameters, ieeg_file)
    except Exception:
        lg.warning(f'No electrodes for {ieeg_file.stem}')
        elec = None

    try:
        pial = load('surface', parameters, ieeg_file)
    except Exception:
        lg.warning(f'No surfaces for {ieeg_file.stem}')
        pial = None

    tf = compute_timefreq(parameters, data, mean=False)
    tf_m = math(tf, operator_name='nanmean', axis='trial_axis')
    tf_cht = get_chantime(parameters, tf_m)
    best_chan, best_time = find_max_point(parameters, tf_cht)
    lg.info(f'Best channel {best_chan}, best interval [{best_time[0]: .3f}-{best_time[1]: .3f}]s')

    tf_ch = get_chan(parameters, tf_m, time=best_time)

    divs = []
    fig = plot_tfr(parameters, tf_m, best_chan, time=best_time)
    divs.append(to_div(fig))
    fig = plot_tfr_time(parameters, tf_cht, highlight=best_time)
    divs.append(to_div(fig))

    if elec is not None:
        fig = plot_surf(parameters, tf_ch, elec, pial)
        divs.append(to_div(fig))

    to_html(divs, name(parameters, 'spectrum', ieeg_file))


def find_max_true(x):
    i_values, i_start, i_dur = find_runs(x)
    i_start = i_start[i_values]
    i_dur = i_dur[i_values]
    i_best = argmax(i_dur)
    return i_start[i_best], i_start[i_best] + i_dur[i_best]


def find_runs(x):
    """Find runs of consecutive items in an array.
    https://gist.github.com/alimanfoo/c5977e87111abe8127453b21204c1065
    """

    # ensure array
    x = asanyarray(x)
    if x.ndim != 1:
        raise ValueError('only 1D array supported')
    n = x.shape[0]

    # handle empty array
    if n == 0:
        return array([]), array([]), array([])

    else:
        # find run starts
        loc_run_start = empty(n, dtype=bool)
        loc_run_start[0] = True
        not_equal(x[:-1], x[1:], out=loc_run_start[1:])
        run_starts = nonzero(loc_run_start)[0]

        # find run values
        run_values = x[loc_run_start]

        # find run lengths
        run_lengths = diff(append(run_starts, n))

        return run_values, run_starts, run_lengths
