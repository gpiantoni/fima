import plotly.graph_objects as go

from ..parameters import P


def plot_tfr_time(tf_time, highlight=None):
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

    if highlight is not None:
        fig.add_shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=highlight[0],
            y0=0,
            x1=highlight[1],
            y1=1,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
            )

    return fig
