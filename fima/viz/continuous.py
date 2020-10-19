import plotly.graph_objs as go

from ..viz import to_div
from ..parameters import FINGER_COLOR, MOVEMENT_LINE


def plot_continuous(tf_cht, onsets, events):

    divs = []
    for chan in tf_cht.chan[0]:
        fig = plot_continuous_per_chan(tf_cht, onsets, events, chan)
        if fig is None:
            continue
        divs.append(to_div(fig))

    return divs


def plot_continuous_per_chan(tf_cht, onsets, events, chan):
    dat = tf_cht(trial=0, trial_axis='trial000000', chan=chan)
    if max(abs(dat)) < 20:
        return None

    fig = go.Figure(data=[
        go.Scatter(
            x=tf_cht.time[0],
            y=dat,
            line=dict(
                color='black',
                width=1,
                )
            ),
        ],
        layout=go.Layout(
            title=dict(
                text=chan,
                ),
            xaxis=dict(
                title='absolute time (s) from start of the task',
                ),
            yaxis=dict(
                title='power spectral density (μV²)',
                range=(-1, 30),
                ),
            ))

    for i in range(len(onsets)):
        finger, movement = events[i].split(' ')

        fig.add_annotation(
            x=onsets[i],
            y=1,
            xref='x',
            yref='paper',
            text=events[i],
            textangle=300,
            font=dict(
                color=FINGER_COLOR[finger],
                )
            )

        fig.add_shape(
            type="line",
            x0=onsets[i],
            x1=onsets[i],
            y0=0,
            y1=1,
            xref='x',
            yref="paper",
            line=dict(
                color=FINGER_COLOR[finger],
                dash=MOVEMENT_LINE[movement],
                ),
            )

    return fig
