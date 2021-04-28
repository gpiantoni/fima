import plotly.graph_objs as go
from plotly.subplots import make_subplots
from numpy import where

from ..utils import create_bool, get_events
from ..parameters import FINGER_COLOR, FINGERS, TIMEPOINTS
from .utils import to_div


def plot_singletrial_tf_and_peaks(parameters, tf, indices, names):

    divs = []
    for i_chan in range(tf.number_of('chan')[0]):
        divs.append(to_div(plot_singletrial_tf_and_peaks_per_chan(parameters, tf, indices, names, i_chan)))

    return divs


def plot_singletrial_tf_and_peaks_per_chan(parameters, tf, indices, names, i_chan):

    events = get_events(names)
    t = tf.time[0]
    chan = tf.chan[0][i_chan]
    dat = tf(trial=0, chan=chan)

    fig = make_subplots(
        rows=2, cols=5,
        shared_yaxes=True,
        subplot_titles=events)

    for ev in events:
        finger, action = ev.split()
        if action in ('close', 'flexion'):
            i_row = 1
        elif action in ('open', 'extension'):
            i_row = 2

        trl_in_cond = create_bool(names, ev)

        for i_trl in where(trl_in_cond)[0]:
            fig.add_trace(
                go.Scatter(
                    x=t,
                    y=dat[:, i_trl],
                    name=f'trial {i_trl}',
                    line=dict(
                        color=FINGER_COLOR[finger],
                        )),
                col=FINGERS.index(finger) + 1,
                row=i_row)

        for timepoint in TIMEPOINTS:
            t_grp, y_grp = select_indices(indices[timepoint], t, dat, i_chan, trl_in_cond)
            if len(t_grp) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=t_grp,
                        y=y_grp,
                        name=timepoint,
                        mode='markers',
                        marker=dict(
                            color='black',
                            symbol=TIMEPOINTS[timepoint])),
                    col=FINGERS.index(finger) + 1,
                    row=i_row)

    fig.update_layout(
        showlegend=False,
        title=chan,
        yaxis=dict(
            title=parameters['spectrum']['baseline']['type'],
            range=parameters['viz']['continuous']['yaxis'],
            ),
        yaxis6=dict(
            title=parameters['spectrum']['baseline']['type'],
            range=parameters['viz']['continuous']['yaxis'],
            ),
        )

    return fig


def select_indices(indices, t, dat, i_chan, i):
    t_grp = t[indices[i_chan, i]]
    y_grp = dat[indices[i_chan, i], i]

    t_grp = t_grp[indices[i_chan, i] > 0]
    y_grp = y_grp[indices[i_chan, i] > 0]

    return t_grp, y_grp
