from plotly.subplots import make_subplots
import plotly.graph_objects as go
from ..parameters import FINGER_COLOR


def plot_fingerbars(t, events, range=(-20, 20)):
    """Plot bars for each value of the fingers.

    Parameters
    ----------
    t : instance of ChanTime
        with channels X values per event
    events : list of str
        list of events

    Returns
    -------
    instance of Plotly Figure

    TODO
    -----
    Note that the function is not very flexible now
    """
    n_rows = t.data[0].shape[0]

    fig = make_subplots(rows=n_rows, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.1 / n_rows)

    i = 1
    for y in t.data[0]:
        fig.add_trace(
            go.Bar(
                x=events,
                y=y,
                marker=dict(
                    color=list(FINGER_COLOR.values()) + list(FINGER_COLOR.values()),
                    line=dict(
                        color='black',
                        width=0,
                    ),
                ),
            ), col=1, row=i)

        yaxis_name = 'yaxis'
        if i > 1:
            yaxis_name += str(i)
        fig.update_layout({yaxis_name: dict(range=range, title=t.chan[0][i - 1])})

        if i == n_rows:
            break
        i += 1

    fig.update_layout(
        height=100 * n_rows,
        width=600,
        showlegend=False,
    )

    return fig
