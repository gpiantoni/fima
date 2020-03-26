import plotly.graph_objects as go

from ..parameters import P


def plot_tfr(tf_m, chan):
    """Plot time frequency representation for one channel

    """

    V = tf_m(trial=0, chan=chan)

    fig = go.Figure(
        go.Heatmap(
            x=tf_m.time[0],
            y=tf_m.freq[0],
            z=V.T,
            colorscale=P['colorscale'],
            zmax=5,
            zmin=-5,
        ),
        layout=go.Layout(
            title=chan,
            xaxis=dict(
                title='time (s)',
            ),
            yaxis=dict(
                title='frequency (Hz)',
                range=(0, 200),
            )
            )
        )
    return fig
