import plotly.graph_objects as go
from numpy import argmin

from ..parameters import MOVEMENT_SYMBOL_DATA, MOVEMENT_LINE
from ..viz.utils import FINGER_COLOR


def plot_dataglove(tsv, events, mov=None):

    traces = []
    i = 0
    for finger, color in FINGER_COLOR.items():

        traces.append(
            go.Scatter(
                x=tsv['time'],
                y=tsv[finger] - i,
                name=finger,
                line=dict(
                    color=color,
                    width=1,
                ),
            ))
        i += 1

    if mov is not None:
        y, circle_color, symbol = _plot_movements(mov, tsv)
        traces.append(
            go.Scatter(
                x=mov['onset'],
                y=y,
                mode='markers',
                marker=dict(
                    color=circle_color,
                    size=10,
                    symbol=symbol,
                    ),
                ))

    fig = go.Figure(
        traces,
        layout=go.Layout(
            showlegend=False,
            xaxis=dict(
                title='time (s)',
            ),
            yaxis=dict(
                tickvals=[.5, -.5, -1.5, -2.5, -3.5],
                ticktext=list(FINGER_COLOR),
            )
        ))

    for ev in events:
        tt = ev['trial_type']
        if tt == 'n/a':
            continue
        finger, movement = tt.split(' ')[:2]
        if finger not in FINGER_COLOR:
            continue

        fig.add_shape(
            dict(
                type="line",
                x0=ev['onset'],
                x1=ev['onset'],
                xref="x",
                yref="paper",
                y0=0,
                y1=1,
                line=dict(
                    color=FINGER_COLOR[finger],
                    width=1,
                    dash=MOVEMENT_LINE[movement],
                )
            ))
    return fig


def _plot_movements(mov, tsv):
    y = []
    circle_color = []
    symbol = []
    for m in mov:
        finger, action = m['trial_type'].split()
        i_min = argmin(abs(m['onset'] - tsv['time']))
        y.append(
            (tsv[finger] - list(FINGER_COLOR).index(finger))[i_min]
        )
        circle_color.append(
            FINGER_COLOR[finger]
        )
        if action == 'flexion':
            symbol.append(MOVEMENT_SYMBOL_DATA['close'])
        else:
            symbol.append(MOVEMENT_SYMBOL_DATA['open'])

    return y, circle_color, symbol
