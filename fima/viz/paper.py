from pathlib import Path
from numpy import arange, array
from scipy.stats import norm
import plotly.graph_objects as go

from ..parameters import FINGER_COLOR, FINGERS_OPEN, FINGERS_CLOSED, FINGERS_EXTENSION, FINGERS_FLEXION
from .utils import LAYOUT, merge
from .dataglove import plot_dataglove
from .ols import plot_data_prediction
from ..ols.fit import compute_param_matrix, get_max, fit_one_channel
from ..spectrum import compute_timefreq, get_chantime
from ..names import name
from ..read import load
from ..ols.prf import compute_prf_from_parameters


def plot_papers(parameters):
    plot_dir = name(parameters, 'paper')

    fig = paper_plot_dataglove(parameters)
    fig.write_image(str(plot_dir / 'dataglove.svg'))

    fig, j = paper_plot_data_prediction(parameters)
    fig.write_image(str(plot_dir / 'prediction.svg'))

    fig = paper_plot_coefficients(parameters, j)
    fig.write_image(str(plot_dir / 'coefficients.svg'))


def paper_plot_dataglove(parameters):
    ieeg_file = Path('/Fridge/users/giovanni/projects/finger_mapping/subjects/sub-drouwen/ses-iemu1/ieeg/sub-drouwen_ses-iemu1_task-fingermapping_acq-clinical_run-1_ieeg.eeg')

    events = load('events', parameters, ieeg_file, 'cues')
    tsv = load('dataglove', parameters, ieeg_file)
    mov = load('events', parameters, ieeg_file, 'movements')

    fig = plot_dataglove(tsv, events, mov)

    layout = dict(
        width=300,
        height=200,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zerolinewidth=0.5,
            title=dict(
                text='time (s)',
                standoff=4,
                ),
            range=(
                60,
                130,)
            ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            ),
        )

    return fig.update_layout(merge(LAYOUT, layout))


def paper_plot_data_prediction(parameters):
    ieeg_file = Path('/Fridge/users/giovanni/projects/finger_mapping/subjects/sub-ommen/ses-iemu1/ieeg/sub-ommen_ses-iemu1_task-fingermapping_acq-HDgrid_run-1_ieeg.eeg')

    chan = 'chan40'

    data, names = load('data', parameters, ieeg_file, parameters['ols']['read'])
    tf = compute_timefreq(parameters, data, baseline=True, mean=False)
    tf = get_chantime(parameters, tf, freq_operator='nanmean')

    t = tf.time[0]
    x = tf(trial=0, chan=chan).flatten(order='F')

    t_plot = arange(x.shape[0]) * (t[1] - t[0])
    matrix_values, out_dim = compute_param_matrix(parameters, t)

    MAT = fit_one_channel(parameters, t, x, names)
    result = get_max(parameters, t, x, names, MAT)[1]

    j = dict(result.params)

    if 'index open' in j:
        columns_open = FINGERS_OPEN
        columns_closed = FINGERS_CLOSED
    else:
        columns_open = FINGERS_EXTENSION
        columns_closed = FINGERS_FLEXION

    compute_prf_from_parameters(j, columns_open)
    compute_prf_from_parameters(j, columns_closed)

    fig = plot_data_prediction(t_plot, result, names)

    layout = dict(
        width=300,
        height=200,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zerolinewidth=0.5,
            title=dict(
                text='time (s)',
                standoff=4,
                ),
            range=(54, 108),
            ),
        yaxis=dict(
            title=dict(
                text='z-score',
                standoff=8,
                ),
            showgrid=False,
            showline=False,
            zeroline=False,
            range=(-1, 7.5),
            ),
        )

    return fig.update_layout(merge(LAYOUT, layout)), j


def paper_plot_coefficients(parameters, j):

    COLS = list(j)[:11]

    COLORS = ['grey', ] + list(FINGER_COLOR.values()) + list(FINGER_COLOR.values())

    traces = [
        go.Bar(
            offset=0.5,
            x=arange(len(COLS)),
            y=[j[col] for col in COLS],
            marker=dict(
                color=COLORS,
            ),
        ),
        ]

    movement_types = list(j)[1].split(' ')[1], list(j)[6].split(' ')[1]

    offset = 2
    for movement_type in movement_types:

        y1 = norm.pdf(
            arange(5),
            loc=j[movement_type + ' loc'],
            scale=j[movement_type + ' scale'],
            )

        data = array([j[f'{finger} {movement_type}'] for finger in FINGER_COLOR])
        scaling = min(data / y1)

        x0 = arange(-0, 4, .01)
        y1 = norm.pdf(
            x0,
            loc=j[movement_type + ' loc'],
            scale=j[movement_type + ' scale'],
            ) * scaling

        traces.append(
            go.Scatter(
                x=x0 + offset,
                y=y1,
                mode='lines',
                line=dict(
                    width=3,
                    color='black',
                ),
                )
            )
        offset += 5

    layout = dict(
        showlegend=False,
        width=300,
        height=250,
        xaxis=dict(
            tickmode='array',
            tickvals=arange(len(COLS)) + 0.5,
            ticktext=COLS,
            showgrid=False,
            showline=False,
            tickangle=-45,
            title=dict(
                text='time (s)',
                standoff=4,
                ),
            ),
        yaxis=dict(
            title=dict(
                text='Coefficients',
                standoff=10,
                ),
            dtick=1,
            showgrid=False,
            showline=False,
            zeroline=False,
            ),
        )

    fig = go.Figure(
        data=traces,
        layout=merge(LAYOUT, layout))
    return fig
