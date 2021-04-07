import plotly.graph_objs as go

from ..fingers.max_activity import FINGERS


def plot_finger_chan(v, chans):
    fig = go.Figure(
        go.Heatmap(
            x=chans,
            y=FINGERS,
            z=v.T,
            zmax=v.max(),
            zmin=v.max() * -1,
            colorscale=P['viz']['colorscale'],
        ),
        layout=go.Layout(
            xaxis=dict(
                title='Channels',
            ),
            yaxis=dict(
                title='Fingers',
                autorange='reversed',
            ))
    )
    return fig
