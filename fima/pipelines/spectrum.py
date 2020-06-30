from numpy import argmax, sum, empty, asanyarray, array, not_equal, nonzero, diff, append

from ..spectrum import compute_timefreq, get_chan, get_chantime
from ..viz import plot_tfr, plot_tfr_time, to_div, to_html, plot_surf, plot_conditions_per_chan
from ..parameters import SPECTRUM_DIR, SUBJECTS, P
from ..read import load
from ..utils import find_max_point

from wonambi.trans import math


DB_THRESHOLD = 3


def pipeline_spectrum_all(event_type='cues', subject_only=None):
    for subject, runs in SUBJECTS.items():
        if subject_only is not None and subject != subject_only:
            continue
        for run in runs:
            print(f'{subject} / {run}')
            try:
                pipeline_spectrum(subject, run, event_type)
            except Exception as err:
                print(err)


def pipeline_spectrum(subject, run, event_type='cues'):

    data, names = load('data', subject, run, event_type=event_type)

    try:
        elec = load('electrodes', subject, run)
    except Exception:
        print(f'No electrodes for {subject}')
        elec = None

    try:
        pial = load('surface', subject, run)
    except Exception:
        print(f'No surfaces for {subject}')
        pial = None

    tf = compute_timefreq(data, mean=False)
    tf_m = math(tf, operator_name='mean', axis='trial_axis')
    tf_cht = get_chantime(tf_m)
    if False:  # this checks only above the threshold, but it fails if there is no point above threshold
        best_chan = find_best_chan(tf_cht)
        best_time = find_timeinterval(tf_cht, best_chan)
    else:
        best_chan, best_time = find_max_point(tf_cht)
    print(f'Best channel {best_chan}, best interval {best_time}s')

    tf_ch = get_chan(tf_m, time=best_time)

    divs = []
    fig = plot_tfr(tf_m, best_chan, time=best_time, freq=P['spectrum']['select']['freq'])
    divs.append(to_div(fig))
    fig = plot_tfr_time(tf_cht, highlight=best_time)
    divs.append(to_div(fig))

    if elec is not None:
        fig = plot_surf(tf_ch, elec, pial)
        divs.append(to_div(fig))

    html_file = SPECTRUM_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)

    html_file = SPECTRUM_DIR / event_type / f'{subject}_run-{run}_{event_type}_allchan.html'

    tf_cht = get_chantime(tf)
    divs = plot_conditions_per_chan(tf_cht, names)
    to_html(divs, html_file)


def find_best_chan(tf_cht):
    """Find best channel which has the most significant time point above
    a threshold.
    """
    values_per_chan = sum(tf_cht.data[0] > DB_THRESHOLD, axis=1)
    i_chan = argmax(values_per_chan)
    best_chan = tf_cht.chan[0][i_chan]
    return best_chan


def find_timeinterval(tf_cht, best_chan):
    """Find time interval with the longest period above threshold
    """
    i_s = tf_cht(trial=0, chan=best_chan) > DB_THRESHOLD
    i_start, i_end = find_max_true(i_s)

    time_start = tf_cht.time[0][i_start]
    time_end = tf_cht.time[0][i_end]

    return time_start, time_end


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