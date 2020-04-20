from numpy import argmax

from ..spectrum import compute_timefreq, get_chan, get_chantime
from ..viz import plot_tfr, plot_tfr_time, to_div, to_html, plot_surf
from ..viz import plot_tfr, plot_tfr_time, to_div, to_html, plot_surf
from ..viz import plot_tfr, plot_tfr_time, to_div, to_html, plot_surf
from ..parameters import SPECTRUM_DIR, SUBJECTS
from ..read import load


def pipeline_timefreq_all(event_type='cues'):
    for subject, runs in SUBJECTS.items():
        for run in runs:
            pipeline_timefreq(subject, run, event_type)


def pipeline_timefreq(subject, run, event_type='cues'):

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

    print('computing time-frequency')
    tf_m = compute_timefreq(data, mean=True)
    tf_cht = get_chantime(tf_m)
    tf_ch = get_chan(tf_m)

    best_chan = tf_ch.chan[0][argmax(tf_ch.data[0])]
    print('making plots')
    divs = []
    fig = plot_tfr(tf_m, best_chan)
    divs.append(to_div(fig))
    fig = plot_tfr_time(tf_cht)
    divs.append(to_div(fig))

    if elec is not None:
        fig = plot_surf(tf_ch, elec, pial)
        divs.append(to_div(fig))

    html_file = SPECTRUM_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)
