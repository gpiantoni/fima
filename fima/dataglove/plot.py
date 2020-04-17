import plotly.graph_objects as go
from numpy import argmin


DASH = {
    'open': 'dot',
    'close': 'solid',
    }
FINGERS = {
    'thumb': 'red',
    'index': 'orange',
    'middle': 'black',
    'ring': 'green',
    'little': 'blue',
}

def plot_dataglove(tsv, events, mov=None):

    traces = []
    i = 0
    for finger, color in FINGERS.items():

        traces.append(
            go.Scatter(
                x=tsv['time'],
                y=tsv[finger] - i,
                name=finger,
                line=dict(
                    color=FINGERS[finger],
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
                ticktext=list(FINGERS),
            )
        ))

    for ev in events:
        tt = ev['trial_type']
        if tt == 'n/a':
            continue
        finger, movement = tt.split(' ')[:2]
        if finger not in FINGERS:
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
                    color=FINGERS[finger],
                    width=1,
                    dash=DASH[movement],
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
            (tsv[finger] - list(FINGERS).index(finger))[i_min]
        )
        circle_color.append(
            FINGERS[finger]
        )
        if action == 'flexion':
            symbol.append('circle')
        else:
            symbol.append('circle-open')

    return y, circle_color, symbol
