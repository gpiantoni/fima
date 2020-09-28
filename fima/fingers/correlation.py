from plotly.subplots import make_subplots
import plotly.graph_objects as go

from ..parameters import FINGER_COLOR, P


def plot_correlation(dat, events):
    """To be merged with .viz/plot_fingerbars"""
    n_rows = dat.shape[0]
    range = (-1, 1)

    fig = make_subplots(rows=n_rows, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.1 / n_rows)

    i = 1
    for y in dat:
        fig.add_trace(
            go.Bar(
                x=events,
                y=y,
                marker=dict(
                    color=list(FINGER_COLOR.values()) + list(FINGER_COLOR.values()),
                ),
            ), col=1, row=i)

        yaxis_name = 'yaxis'
        if i > 1:
            yaxis_name += str(i)
        fig.update_layout({yaxis_name: dict(range=range, title=events[i - 1])})

        if i == n_rows:
            break
        i += 1

    fig.update_layout(
        height=100 * n_rows,
        width=600,
        showlegend=False,
    )

    return fig


def plot_heatmap(v, events):
    fig = go.Figure(
        go.Heatmap(
            x=events,
            y=events,
            z=v.T,
            zmax=1,
            zmin=-1,
            colorscale=P['viz']['colorscale'],
        ),
        layout=go.Layout(
            xaxis=dict(
                title='Fingers',
            ),
            yaxis=dict(
                title='Fingers (used for electrode selection)',
                autorange='reversed',
            ))
    )
    return fig


def plot_finger_chan_2(v, events, chans):
    fig = go.Figure(
        go.Heatmap(
            x=events,
            y=chans,
            z=v,
            zmax=10,
            zmin=-10,
            colorscale=P['viz']['colorscale'],
        ),
        layout=go.Layout(
            width=600,
            height=50 * len(chans),
            xaxis=dict(
                title='Channels',
            ),
            yaxis=dict(
                title='Fingers',
                autorange='reversed',
            ))
    )

    return fig
