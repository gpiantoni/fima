from ..parameters import (
    FINGER_COLOR,
    FINGERS_EXTENSION,
    FINGERS_FLEXION,
    FINGERS_OPEN,
    FINGERS_CLOSED,
    MOVEMENT_LINE,
    )
import plotly.graph_objects as go


def plot_data_prediction(t, results, names):

    n_trl = len(names)
    n_time = results.fittedvalues.shape[0] // n_trl

    traces = [
        go.Scatter(
            x=t,
            y=results.model.data.endog,
            name='data',
            line=dict(
                color='black',
                width=1,
            ),
        ),
        ]

    for i_trl in range(n_trl):
        finger, action = names[i_trl].split()

        i_x = slice(
            i_trl * n_time,
            (i_trl + 1) * n_time)
        traces.append(
            go.Scatter(
                x=t[i_x],
                y=results.fittedvalues[i_x],
                name='prediction',
                line=dict(
                    color=FINGER_COLOR[finger],
                    dash=MOVEMENT_LINE[action],
                    width=2,
                ),
            ),
            )
    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            showlegend=False))

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
