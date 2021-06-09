from pathlib import Path
from shutil import rmtree
from numpy import arange, array, ceil, floor, histogram, max, sqrt
from scipy.stats import norm
from subprocess import run
import plotly.graph_objects as go

from ..parameters import FINGER_COLOR, FINGERS_OPEN, FINGERS_CLOSED, FINGERS_EXTENSION, FINGERS_FLEXION, FINGERS
from .utils import LAYOUT, merge
from .dataglove import plot_dataglove
from .ols import plot_data_prediction
from .ols_summary import plot_ols_rsquared
from ..ols.fit import compute_param_matrix, get_max, fit_one_channel
from ..spectrum import compute_timefreq, get_chantime
from ..names import name
from ..read import load
from ..ols.prf import compute_prf_from_parameters
from ..ols.summary import import_all_ols


REGIONS = 'precentral', 'postcentral'


def plot_papers(parameters):

    plot_dir = name(parameters, 'paper')
    try:
        rmtree(plot_dir)
    except OSError:
        pass
    plot_dir.mkdir(exist_ok=True, parents=True)

    fig = paper_plot_dataglove(parameters)
    fig.write_image(str(plot_dir / 'dataglove.svg'))

    fig = paper_plot_rsquared(parameters)
    fig.write_image(str(plot_dir / 'rsquared.svg'))

    df = import_all_ols(parameters)
    fig = paper_plot_df_time(df, 'spread')
    fig.write_image(str(plot_dir / 'time_spread.svg'))
    fig = paper_plot_df_time(df, 'onset')
    fig.write_image(str(plot_dir / 'time_onset.svg'))
    fig = paper_plot_df_time(df, 'peak')
    fig.write_image(str(plot_dir / 'time_peak.svg'))

    figs = paper_plot_prf(df)
    for region, fig in zip(REGIONS, figs):
        fig.write_image(str(plot_dir / f'prf_{region}.svg'))

    fig = paper_plot_surf()
    fig_name = str(plot_dir / 'surf_rsquared.png')
    fig.write_image(fig_name)
    run(['convert', fig_name, '-trim', fig_name])

    # takes time
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


def paper_plot_rsquared(parameters):
    df = import_all_ols(parameters)

    fig = plot_ols_rsquared(df, 'DKTatlas')
    layout = dict(
        showlegend=True,
        width=400,
        height=300,
        title=dict(
            text='',
            ),
        xaxis=dict(
            title=dict(
                text='',
                ),
            showgrid=False,
            tickangle=-45,
            ),
        yaxis=dict(
            title=dict(
                text='# channels',
                standoff=10,
                ),
            dtick=100,
            showgrid=False,
            ),
        )

    fig.update_layout(merge(LAYOUT, layout))

    return fig


def paper_plot_df_time(df, param):
    width = 0.05

    markers = dict(
        color='white',
        line=dict(
            width=2,
            color='black',
            ),
        )

    i_rsquared = df['estimate']['rsquared'] > 0.1
    i_region = df['channel']['DKTatlas'].isin(REGIONS)
    y = df[i_rsquared & i_region]['estimate'][param]

    min_val = floor(y.min() / 0.05) * 0.05
    max_val = ceil(y.max() / 0.05) * 0.05
    t_plot = arange(min_val, max_val, width)

    traces = []
    h_all = []

    for region in REGIONS:
        i_region = df['channel']['DKTatlas'] == region
        y = df[i_rsquared & i_region]['estimate'][param]
        h0 = histogram(y, t_plot)[0]
        h_all.append(h0)

        if region == 'precentral':
            scale = 1
        else:
            scale = -1

        traces.append(
            go.Bar(
                x=t_plot,
                y=h0 * scale,
                name=region,
                marker=markers,
                width=width,
                )
            )

    m = max(h_all) + 5
    layout = dict(
        showlegend=False,
        width=400,
        height=200,
        barmode='relative',
        yaxis=dict(
            range=[-m, m],
            title=dict(
                text=''
                ),
            ),
        )

    fig = go.Figure(
        data=traces,
        layout=merge(LAYOUT, layout),
        )

    return fig


def paper_plot_prf(df):

    pick_finger = lambda v: int(floor(v + 0.5))
    figs = []
    i_rsquared = df['estimate']['rsquared'] >= 0.1  # TODO: in parameters

    for region in REGIONS:
        i_region = df['channel']['DKTatlas'] == region

        m = {}
        s = {}
        traces = []
        for movement_type in ('ext', 'flex'):
            df_prf = df['prf_' + movement_type]

            i_prf = df_prf['rsquared'] >= 0.9  # TODO: in parameters
            main_finger = df_prf['finger'].apply(pick_finger)

            i_row = i_region & i_rsquared & i_prf & main_finger.isin(range(5))
            m[movement_type] = df_prf[i_row].groupby(main_finger).mean()['spread']
            s[movement_type] = df_prf[i_row].groupby(main_finger).std()['spread'] / sqrt(i_row.sum())

            traces.append(
                go.Scatter(
                    x=arange(5) + 1,
                    y=m[movement_type],
                    mode='markers',
                    error_y=dict(
                        type='data',
                        array=s[movement_type],
                        ),
                    ),
            )

        layout = dict(
            showlegend=False,
            width=300,
            height=250,
            xaxis=dict(
                tickmode='array',
                tickvals=arange(len(FINGERS)) + 1,
                ticktext=FINGERS,
                showgrid=False,
                tickangle=-45,
                ),
            yaxis=dict(
                title=dict(
                    text='Spread',
                    standoff=10,
                    ),
                dtick=1,
                range=(0, 4),
                showgrid=False,
                ),
            )

        figs.append(
            go.Figure(
                data=traces,
                layout=merge(LAYOUT, layout))
            )
    return figs


def paper_plot_surf():
    pass
