import plotly.graph_objects as go
from numpy import NaN, argmax
from wonambi import Data

from .general import estimate
from ..viz.surf import plot_surf
from ..parameters import FINGER_COLOR, MOVEMENT_SYMBOL_DATA, MOVEMENT_SYMBOL_MODEL


def estimate_and_plot(y, model, names, result, channels, chan=None):

    if chan is None:
        i_chan = argmax(result['rsquared'])
    else:
        i_chan = list(channels).index(i_chan)

    seed = result[i_chan:i_chan + 1].view('<f8')[:-1]
    est = estimate(model, names, seed)

    fig = plot_fitted(names, y[i_chan], est)

    title = model['doc'] + '<br /> ' + _parse_subtitle(channels[i_chan], result)
    fig = fig.update_layout(
        title=dict(
            text=title))
    return fig


def _parse_subtitle(chan, v):
    t = [f'channel: {chan}']
    for name in v.dtype.names:
        t.append(f'{name}: {v[name][0]:0.3f}')

    return '\t'.join(t)


def plot_prf_results(result, param, channels, electrodes, surf, rsquared_threshold=0.05):
    val = result[param].copy()
    val[result['rsquared'] < rsquared_threshold] = NaN
    dat = Data(val, s_freq=1, chan=channels)

    return plot_surf(dat, electrodes, pial=surf, info='finger')


def plot_fitted(names, y, estimate):

    finger_color, symbol_data, symbol_model = get_color_symbol(names)
    fig = go.Figure(
        data=[
            go.Scatter(
                y=estimate,
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
                y=y,
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
