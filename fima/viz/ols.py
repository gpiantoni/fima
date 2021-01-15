from fima.parameters import FINGER_COLOR
import plotly.graph_objects as go

# this should be in parameters
COLS = [
    'const',
    'thumb extension',
    'index extension',
    'middle extension',
    'ring extension',
    'little extension',
    'thumb flexion',
    'index flexion',
    'middle flexion',
    'ring flexion',
    'little flexion',
    ]


def plot_sigma_delay_mat(MAT, SIGMAS, DELAYS):
    """Not being used at this point, because gamma is 3D so I don't know how to
    plot it"""
    raise NotImplementedError

    fig = go.Figure(data=[
        go.Heatmap(
            x=DELAYS,
            y=SIGMAS,
            z=MAT,
            zmin=0,
            colorscale='Hot',
            ),
        ],
        layout=go.Layout(
            xaxis=dict(
                title='Delay (ms, 0s == movement start)'),
            yaxis=dict(
                title='Kernel size (ms)'),
            ))
    return fig


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
    LOW = results.conf_int()[0]
    HIGH = results.conf_int()[1]

    COLORS = ['grey', ] + list(FINGER_COLOR.values()) + list(FINGER_COLOR.values())

    fig = go.Figure(data=[
        go.Bar(
            x=COLS,
            y=[COEF[col] for col in COLS],
            marker=dict(
                color=COLORS,
            ),
            error_y=dict(
                type='data',
                arrayminus=[COEF[col] - LOW[col] for col in COLS],
                array=[HIGH[col] - COEF[col] for col in COLS],
            ),
        ), ],
        layout=go.Layout(
            yaxis=dict(
                title='Coefficients')
        ))

    return fig
