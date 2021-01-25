from json import dump
from json import load as json_load
from logging import getLogger
from wonambi import Data
from pandas import DataFrame
from numpy import nanmin, nanmax, array, corrcoef

from ..read import load
from ..spectrum.continuous import get_continuous_cht
from ..ols.regressors import find_movement_indices
from ..ols.fit import get_max, fit_one_channel
from ..viz import to_div, to_html
from ..viz.surf import plot_surf
from ..viz.ols import plot_coefficient, plot_data_prediction
from ..parameters import RESULTS_DIR, P, FINGERS_FLEXION, FINGERS_EXTENSION

lg = getLogger(__name__)

OLS_DIR = RESULTS_DIR / 'ols' / 'movement'
SUMMARY_DIR = RESULTS_DIR / 'ols' / 'summary'
PLOTS_DIR = RESULTS_DIR / 'ols' / 'plots'


def pipeline_ols(subject, run, summary):
    """
    Parameters
    ----------
    summary : bool
        if True, skip time-consuming computation of OLS for each channel
    """
    if not summary:
        pipeline_ols_allchan(subject, run)

    pipeline_ols_summary(subject, run)


def pipeline_ols_allchan(subject, run):

    tf_cht, events, onsets = get_continuous_cht(subject, run, event_type='cues')
    t = tf_cht.time[0]

    try:
        mov = load('movements', subject, run)
    except FileNotFoundError:
        return

    indices = find_movement_indices(mov, tf_cht.time[0])
    for chan in tf_cht.chan[0]:
        lg.info(f'{subject:<10}/ {run} Fitting OLS on {chan}')
        x = tf_cht(trial=0, chan=chan, trial_axis='trial000000')

        MAT = fit_one_channel(t, x, indices)
        out, result = get_max(t, x, indices, MAT)
        out['chan'] = chan

        divs = []

        # fig = plot_sigma_delay_mat(MAT, SIGMAS * t_diff, DELAYS * t_diff)
        # divs.append(to_div(fig))

        fig = plot_coefficient(result)
        divs.append(to_div(fig))

        fig = plot_data_prediction(tf_cht.time[0], result)
        divs.append(to_div(fig))

        html_file = OLS_DIR / f'{subject}_run-{run}' / f'{subject}_run-{run}_{chan}.html'
        to_html(divs, html_file)

        json_file = html_file.with_suffix('.json')
        with json_file.open('w') as f:
            dump(out, f, indent=2)


def pipeline_ols_summary(subject, run):
    df = import_ols(subject, run)
    if df is None:
        return

    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(
        SUMMARY_DIR / f'ols_movement_{subject}_run-{run}_summary.tsv',
        sep='\t', index=False)

    elec = load('electrodes', subject, run)
    try:
        pial = load('surface', subject, run)
    except FileNotFoundError:
        pial = None

    dat = Data(array(df['rsquared']), chan=array(df['chan']))
    fig = plot_surf(dat, elec, pial=pial, clim=(0, nanmax(df['rsquared'])), colorscale='Hot')
    to_html([to_div(fig), ], PLOTS_DIR / f'ols_movement_{subject}_run-{run}_rsquared.html')

    df = df[df['rsquared'] >= P['ols']['threshold']]
    if len(df) == 0:
        lg.warning(f'No channels had a fit better than threshold {P["ols"]["threshold"]}')
        return

    params = set(df) - {'rsquared', 'chan'}
    for param in params:
        dat = Data(array(df[param]), chan=array(df['chan']))
        fig = plot_surf(dat, elec, pial=pial, clim=(nanmin(df[param]), nanmax(df[param])), colorscale='Hot')
        to_html([to_div(fig), ], PLOTS_DIR / f'ols_movement_{subject}_run-{run}_{param.replace(" ", "")}.html')


def import_ols(subject, run):

    out_dir = OLS_DIR / f'{subject}_run-{run}'

    df = []
    for json_file in out_dir.glob('*.json'):
        with json_file.open() as f:
            df.append(json_load(f))

    if len(df) == 0:
        return

    df = DataFrame(df).sort_values('rsquared', ascending=False).reset_index(drop=True)

    i_corr = []
    for i, row in df.iterrows():
        i_corr.append(
            corrcoef(
                row[FINGERS_FLEXION].astype(float),
                row[FINGERS_EXTENSION].astype(float))[0, 1])
    df['corrparams'] = i_corr

    return df


