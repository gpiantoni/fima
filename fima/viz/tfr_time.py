import plotly.graph_objects as go

from ..parameters import P


def plot_tfr_time(tf_time):
    traces = []
    for chan in tf_time.chan[0]:
        traces.append(
            go.Scatter(
                x=tf_time.time[0],
                y=tf_time(trial=0, chan=chan),
                name=chan,
                line=dict(
                    color='black',
                    width=0.5,
                ),
                showlegend=False,
                hovertemplate="time: %{x:.3f}s<br />dB: %{y:.3f}",
            ))

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            xaxis=dict(
                title='time (s)',
            ),
            yaxis=dict(
                title='change from baseline (dB)',
                range=(
                    -1 * P['viz']['tfr_mean']['max'],
                    P['viz']['tfr_mean']['max'],
                    ),
                )
            )
        )

    return fig
