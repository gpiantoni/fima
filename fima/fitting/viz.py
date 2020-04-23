import plotly.graph_objects as go

from ..parameters import FINGER_COLOR, MOVEMENT_SYMBOL_DATA, MOVEMENT_SYMBOL_MODEL


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
                title='trials / time',
                ),
            yaxis=dict(
                title='values (dB / zvalues)',
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
