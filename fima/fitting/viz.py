import plotly.graph_objects as go
from numpy import NaN, nanargmax, outer
from wonambi import Data

from .general import estimate
from ..viz.surf import plot_surf
from ..parameters import MOVEMENT_SYMBOL_DATA, MOVEMENT_SYMBOL_MODEL
from .utils import get_response
from ..viz.utils import FINGER_COLOR


def estimate_and_plot(y, model, names, result, channels, chan=None):

    if chan is None:
        i_chan = nanargmax(result['rsquared'])
    else:
        i_chan = list(channels).index(i_chan)

    seed = result[i_chan:i_chan + 1].view('<f8')[:-1]

    if y[0].ndim == 1:
        n_timepoints = None
    else:
        n_timepoints = y[0].shape[0]
    est = estimate(model, names, seed, n_timepoints)

    response = get_response(model.get('response', None), y[i_chan])
    if response is not None:
        est = outer(response, est)

    if response is None and model['type'] == 'trial-based':
        fig = plot_fitted_trial(names, y[i_chan], est)
        response_str = ' (trials)'
    else:
        fig = plot_fitted_time(names, y[i_chan], est)
        response_str = ' (' + str(model.get('response', '')) + ')'

    title = model['doc'] + response_str + '<br />' + _parse_subtitle(channels[i_chan], result[i_chan:i_chan + 1])
    fig = fig.update_layout(
        title=dict(
            text=title))
    return fig


def _parse_subtitle(chan, v):
    t = [f'channel: {chan}']
    for name in v.dtype.names:
        t.append(f'{name}: {v[name][0]:0.3f}')

    if len(t) > 6:
        return '<br />'.join([
            '\t'.join(t[:5]),
            '\t'.join(t[5:]),
            ])

    else:
        return '\t'.join(t)


def plot_prf_results(result, param, channels, electrodes, surf=None, rsquared_threshold=0.05):

    val = result[param].copy()
    if param == 'rsquared':
        info = 'rsquared'
        pial = surf
    elif param == 'open_v_close':
        info = 'open_v_close'
        pial = surf
    else:
        val[result['rsquared'] < rsquared_threshold] = NaN
        info = 'finger'
        pial = None
    dat = Data(val, s_freq=1, chan=channels)

    fig = plot_surf(dat, electrodes, pial=pial, info=info)
    fig.update_layout(
        title=dict(
            text=param,
            ))

    return fig


def plot_fitted_trial(names, y, estimate):

    finger_color, symbol_data, symbol_model = get_color_symbol(names)
    fig = go.Figure(
        data=[
            go.Scatter(
                y=estimate.ravel('F'),
                name='estimate',
                mode='lines+markers',
                line=dict(
                    width=0.5,
                    ),
                marker=dict(
                    color=finger_color,
                    symbol=symbol_model,
                    size=8,
                    ),
                ),
            go.Scatter(
                y=y.ravel('F'),
                name='data',
                mode='lines+markers',
                line=dict(
                    width=0.5,
                    ),
                marker=dict(
                    color=finger_color,
                    symbol=symbol_data,
                    size=8,
                    ),
                ),
            ],
        layout=go.Layout(
            xaxis=dict(
                title='trials',
                ),
            yaxis=dict(
                title='values',
                ),
            ),
        )

    return fig


def plot_fitted_time(names, y, estimate):

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
                y=y[:, i],
                name='data',
                mode='lines',
                line=dict(
                    width=LINE[symbol_data[i]],
                    color=finger_color[i],
                    dash='dash',
                    ),
            )
        )
        traces.append(
            go.Scatter(
                x0=i,
                dx=1 / y.shape[0],
                y=estimate[:, i],
                name='estimate',
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
            showlegend=False,
            xaxis=dict(
                title='time',
                ),
            yaxis=dict(
                title='values',
                ),
            ),
    )
    return fig


def get_color_symbol(names):
    color = []
    symbol_data = []
    symbol_model = []

    for m in names:
        finger, action = m.split()
        color.append(FINGER_COLOR[finger])
        symbol_data.append(MOVEMENT_SYMBOL_DATA[action])
        symbol_model.append(MOVEMENT_SYMBOL_MODEL[action])

    return color, symbol_data, symbol_model
