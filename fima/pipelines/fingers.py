from ..fingers.max_activity import find_activity_per_finger, find_tstat_per_finger
from ..viz.finger_channels import plot_finger_chan
from ..fingers.viz import plot_fingerbars
from ..viz import to_div, to_html, plot_surf
from ..fingers.correlation import plot_heatmap, plot_finger_chan_2
from ..read import load

from numpy import corrcoef, empty, save, NaN
from scipy.stats import norm as normdist
from wonambi import Data


def pipeline_fingers(subject, run, event_type='cues'):
    v, chans = find_activity_per_finger(subject, run)
    fig = plot_finger_chan(v, chans)

    divs = [to_div(fig), ]

    html_file = FINGERS_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)


def pipeline_fingerbars(subject, run, event_type='cues'):
    t, events = find_tstat_per_finger(subject, run, event_type)
    fig = plot_fingerbars(t, events)
    divs = [to_div(fig), ]

    html_file = FINGERBARS_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)


def pipeline_finger_correlations(subject, run, event_type, threshold=5):
    t, events = find_tstat_per_finger(subject, run, event_type)
    X = t.data[0]
    i_active = (X > threshold).any(axis=1)
    X1 = X[i_active]

    dat = corrcoef(X1.T)

    fig = plot_heatmap(dat, events)
    divs = [to_div(fig), ]

    html_file = FINGERCORR_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)


def pipeline_finger_correlations_each(subject, run, event_type, pvalue=0.05):
    t, events = find_tstat_per_finger(subject, run, event_type)
    X = t.data[0]
    threshold = normdist.ppf(1 - (pvalue / 2))
    elec = load('electrodes', subject, run)

    C = empty((t.number_of('event')[0], t.number_of('event')[0]))
    divs = []
    A = X.copy()
    i_active = abs(A) < threshold
    A[i_active] = NaN
    fig1 = plot_finger_chan_2(A, events, t.chan[0])

    for i in range(t.number_of('event')[0]):
        i_active = abs(X[:, i]) > threshold
        X1 = X[i_active, :]

        d = t(event=t.event[0][i], trial=0).copy()
        d[~i_active] = NaN
        t_1 = Data(d, s_freq=1, chan=t.chan[0])
        fig = plot_surf(t_1, elec, info='tstat')
        fig = fig.update_layout(title=t.event[0][i])
        divs.append(to_div(fig))
        dat = corrcoef(X1.T)
        C[:, i] = dat[:, i]

    divs.append(to_div(fig1))
    fig = plot_heatmap(C, events)
    divs.append(to_div(fig))

    html_file = FINGERCORREACH_DIR / event_type / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)
    npy_file = html_file.with_suffix('.npy')
    save(str(npy_file), C)
