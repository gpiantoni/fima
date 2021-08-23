import plotly.graph_objs as go
from numpy import (
    arctanh,
    corrcoef,
    isnan,
    NaN,
    percentile,
    zeros,
    )

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


def plot_coefs_cc(parameters, df, region, movements):

    region_type = parameters['ols']['results']['atlas']
    i_region = df['channel'][region_type] == region

    cc = zeros((5, 5))
    cc.fill(NaN)
    for i0, f0 in enumerate(FINGERS):
        for i1, f1 in enumerate(FINGERS):
            mov0 = mov1 = movements
            if movements == 'flexion' and i0 >= i1:
                continue
            if movements == 'extension' and i0 <= i1:
                continue
            if movements == 'compare':
                if i0 != i1:
                    continue
                else:
                    mov0 = 'flexion'
                    mov1 = 'extension'
            cc[i0, i1] = fisher_corrcoef(df[mov0][f0][i_region], df[mov1][f1][i_region])

    traces = [
        go.Heatmap(
            z=cc,
            zmin=0,
            zmax=1,
            colorscale=parameters['viz']['colorscale'],
            ),
        ]

    fig = go.Figure(
        data=traces,
        )
    return fig


def fisher_corrcoef(x0, x1):
    x0 = fisher_trans(x0)
    x1 = fisher_trans(x1)
    has_nan = isnan(x0) | isnan(x1)
    return corrcoef(x0[~has_nan], x1[~has_nan])[0, 1]


def fisher_trans(x):
    max0 = percentile(x, 99)
    min0 = percentile(x, 1)
    x = ((x - min0) / (max0 - min0)) * 2 - 1
    x[x <= -1] = NaN
    x[x >= 1] = NaN
    return arctanh(x)
