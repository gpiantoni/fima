from numpy import min, ptp
import plotly.graph_objects as go

normalize = lambda x: (x - min(x)) / ptp(x)

DASH = {
    'open': 'solid',
    'close': 'dot',
    }
FINGERS = {
    'thumb': 'red',
    'index': 'orange',
    'middle': 'yellow',
    'ring': 'green',
    'little': 'blue',
}

def _plot_dataglove(tsv, events):

    if 'right_thumb' in tsv.dtype.names:
        left_right = 'right'
    elif 'left_thumb' in tsv.dtype.names:
        left_right = 'left'
    else:
        raise ValueError

    traces = []
    i = 0
    for finger, color in FINGERS.items():

        traces.append(
            go.Scatter(
                x=tsv['time'],
                y=normalize(tsv[f'{left_right}_{finger}']) - i,
                name=finger,
                line=dict(
                    color=FINGERS[finger],
                    width=1,
                ),
            ))
        i += 1

    fig = go.Figure(traces)
    fig
    for ev in events:
        tt = ev['trial_type']
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
