from plotly.subplots import make_subplots
import plotly.graph_objects as go
from ..parameters import FINGER_COLOR


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
