import plotly.graph_objs as go

from ..fitting.viz import get_color_symbol
from ..utils import group_per_condition
from .utils import to_div


def plot_conditions_per_chan(tf_cht, names):
    data_m, events = group_per_condition(tf_cht, names, 'mean')
    data_sd, events = group_per_condition(tf_cht, names, 'std')  # you can also use sem

    divs = []

    for chan in tf_cht.chan[0]:
        y = data_m(trial=0, chan=chan)
        s = data_sd(trial=0, chan=chan)
        fig = plot_per_chan(y, s, chan, names)
        divs.append(to_div(fig))

    return divs


def plot_per_chan(y, s, chan, names):

    LINE = {
        'circle-open': 1,
        'circle': 2,
    }

    finger_color, symbol_data, symbol_model = get_color_symbol(names)

    traces = []
    for i in range(y.shape[1]):
        traces.append(
            go.Scatter(
                x0=i,
                dx=1 / y.shape[0],
                y=y[:, i] + s[:, i],
                name='data',
                mode='lines',
                line=dict(width=0,),
                fillcolor='rgba(68, 68, 68, 0.3)',
                )
            )
        traces.append(
            go.Scatter(
                x0=i,
                dx=1 / y.shape[0],
                y=y[:, i] - s[:, i],
                name='data',
                mode='lines',
                line=dict(width=0,),
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty'
                )
            )

        traces.append(
            go.Scatter(
                x0=i,
                dx=1 / y.shape[0],
                y=y[:, i],
                name='data',
                mode='lines',
                line=dict(
                    width=LINE[symbol_data[i]],
                    color=finger_color[i],
                    dash='solid',
                    ),
                )
            )

    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            title=chan,
            showlegend=False,
            xaxis=dict(
                title='time and conditions',
                ),
            yaxis=dict(
                title='change from baseline',
                range=(-6, 6),
                ),
            ),
    )
    return fig
