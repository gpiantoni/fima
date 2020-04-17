from pathlib import Path
from numpy import argmax

from ..preproc import read_data, read_surf
from ..spectrum import compute_timefreq, get_chan, get_chantime
from ..viz import plot_tfr, plot_tfr_time, to_div, to_html, plot_surf
from ..parameters import SPECTRUM_DIR
from ..utils import make_name


def pipeline_timefreq(subject, run, event_type='all'):

    filename = Path(filename).resolve()

    print(f'reading {filename.stem}')

    try:
        elec = read_elec(filename)
    except:
        print(f'No electrodes for {filename.stem}')
        elec = None

    try:
        pial = read_surf(filename)
    except:
        print(f'No surfaces for {filename.stem}')
        pial = None
    data, events = read_data(filename, event_type)

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

    to_html(divs, SPECTRUM_DIR / make_name(filename, event_type))
    print('done')
