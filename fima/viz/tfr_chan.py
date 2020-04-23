import plotly.graph_objects as go

from ..parameters import P


def plot_tfr(tf_m, chan, time=None, freq=None):
    """Plot time frequency representation for one channel

    """

    V = tf_m(trial=0, chan=chan)

    fig = go.Figure(
        go.Heatmap(
            x=tf_m.time[0],
            y=tf_m.freq[0],
            z=V.T,
            colorscale=P['viz']['colorscale'],
            zmax=P['viz']['tfr']['max'],
            zmin=P['viz']['tfr']['max'] * -1,
            hovertemplate="time: %{x:.3f}s<br />freq: %{y:.0f}Hz<br />dB: %{z:.3f}<extra></extra>",
            colorbar=dict(
                title=dict(
                    text='change from baseline (dB)',
                    side='right',
                    ),
                ),
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

    if freq is not None and time is not None:
        fig.add_shape(
            type="rect",
            xref="x",
            yref="y",
            x0=time[0],
            y0=freq[0],
            x1=time[1],
            y1=freq[1],
            opacity=1,
            layer="above",
            line=dict(
                color="Black",
                width=5,
                ),
            )

    return fig
