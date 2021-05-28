from ..parameters import (
    FINGER_COLOR,
    FINGERS_EXTENSION,
    FINGERS_FLEXION,
    FINGERS_OPEN,
    FINGERS_CLOSED,
    )
import plotly.graph_objects as go


def plot_data_prediction(t, results):
    fig = go.Figure(data=[
        go.Scatter(
            x=t,
            y=results.model.data.endog,
            name='data',
            line=dict(
                color='blue',
                width=1,
            ),
        ),
        go.Scatter(
            x=t,
            y=results.fittedvalues,
            name='prediction',
            line=dict(
                color='red',
                width=1,
            ),
        ),
    ])
    return fig


def plot_coefficient(results):

    COEF = results.params

    if 'index open' in COEF.index.values:
        COLS = ['const', ] + FINGERS_OPEN + FINGERS_CLOSED
    else:
        COLS = ['const', ] + FINGERS_EXTENSION + FINGERS_FLEXION

    COLORS = ['grey', ] + list(FINGER_COLOR.values()) + list(FINGER_COLOR.values())

    fig = go.Figure(data=[
        go.Bar(
            x=COLS,
            y=[COEF[col] for col in COLS],
            marker=dict(
                color=COLORS,
            ),
        ), ],
        layout=go.Layout(
            yaxis=dict(
                title='Coefficients')
        ))

    return fig
