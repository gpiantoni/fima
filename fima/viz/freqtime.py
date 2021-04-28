import plotly.graph_objs as go

from wonambi.attr import Channels
from wonambi.attr.chan import assign_region_to_channels
from numpy import c_

from ..viz.fitting import get_color_symbol
from ..utils import group_per_condition
from .utils import to_div


def plot_conditions_per_chan(parameters, tf_cht, names, statistics='sem', fs=None, elec=None):
    assert NotImplementedError
    """Plot all the conditions for each channel

    Parameters
    ----------
    tf_cht : wonambi.Data
        time-channel data
    names : list of str
        list of all the events
    statistics : str
        'sem' or 'std'

    Returns
    -------
    list of dict
        plotly images
    """
    data_m, events = group_per_condition(tf_cht, names, 'mean')
    data_sd, events = group_per_condition(tf_cht, names, statistics)  # you can also use sem

    if False and elec is not None and fs is not None:
        regions = _compute_regions(fs, elec)

    divs = []

    for chan in tf_cht.chan[0]:
        y = data_m(trial=0, chan=chan)
        s = data_sd(trial=0, chan=chan)
        fig = plot_per_chan(parameters, y, s, chan, names)

        if False and elec is not None and fs is not None:
            region = _get_region(regions, chan)
            fig.update_layout(title=f'{chan} ({region})')

        divs.append(to_div(fig))

    return divs


def plot_per_chan(parameters, y, s, chan, names):

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
                range=(-1 * parameters['viz']['tfr']['max'], parameters['viz']['tfr']['max'])
                ),
            ),
    )
    return fig
