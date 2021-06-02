from shutil import rmtree
from json import dump
from json import load as json_load
from logging import getLogger
from wonambi import Data
from pandas import DataFrame
from numpy import nanmin, nanmax, array, arange

from ..read import load
from ..spectrum.compute import compute_timefreq, get_chantime
from ..ols.fit import get_max, fit_one_channel
from ..ols.prf import add_prf_estimates
from ..ols.summary import import_all_ols
from ..viz import to_div, to_html
from ..viz.surf import plot_surf
from ..viz.ols import plot_coefficient, plot_data_prediction
from ..viz.ols_summary import plot_ols_rsquared, plot_ols_params, plot_ols_flexext, plot_ols_prf, plot_fingerfriends
from ..names import name

lg = getLogger(__name__)


def pipeline_ols(parameters, ieeg_file):
    """
    Parameters
    ----------
    """
    if not parameters['ols']['skip_ols']:
        pipeline_ols_allchan(parameters, ieeg_file)
    if not parameters['ols']['skip_prf']:
        pipeline_ols_prf(parameters, ieeg_file)

    pipeline_ols_summary(parameters, ieeg_file)


def pipeline_ols_all(parameters):

    summary_dir = name(parameters, 'ols_plot')

    df = import_all_ols(parameters)

    REGIONS = ['DKTatlas']
    divs = []
    for region in REGIONS:
        fig = plot_ols_rsquared(df, region)
        divs.append(to_div(fig))
    to_html(divs, summary_dir / 'ols_movement_all_rsquared_bars.html')

    PARAMS = (
        ('estimate', 'onset', 'Onset time (ms, movement onset = 0)'),
        ('estimate', 'peak', 'Peak time (ms, movement onset = 0)'),
        ('estimate', 'spread', 'Temporal Spread (ms, wider -> more spread over time)'),
        ('flexext', 'corr', 'Correlation between extension and flexion estimates'),
        ('flexext', 'diff', 'Extension estimates - flexion estimates'),
        ('prf_ext', 'spread', 'PRF spatial spread (extension)'),
        ('prf_flex', 'spread', 'PRF spatial spread (extension)'),
        ('prf_ext', 'finger', 'PRF favorite finger (extension)'),
        ('prf_flex', 'finger', 'PRF favorite finger (extension)'),
        )

    divs = []
    for param in PARAMS:
        for region in REGIONS:
            fig = plot_ols_params(
                df[df['estimate']['rsquared'] > 0.1],
                param[:2],
                region,
                param[2],
                )
            divs.append(to_div(fig))
    to_html(divs, summary_dir / 'ols_movement_all_summary.html')

    region_type = parameters['ols']['results']['atlas']

    divs = plot_fingerfriends(df, region_type)
    to_html(divs, summary_dir / 'ols_movement_all_fingerfriends.html')

    divs = plot_ols_flexext(df, region_type)
    to_html(divs, summary_dir / 'ols_movement_all_flexext.html')

    divs = plot_ols_prf(df, region_type, 'finger')
    to_html(divs, summary_dir / 'ols_movement_all_prf_finger.html')

    divs = plot_ols_prf(df, region_type, 'spread')
    to_html(divs, summary_dir / 'ols_movement_all_prf_spread.html')

    df.to_csv(
        name(parameters, 'ols_summary') / 'overview.tsv',
        sep='\t', index=False)


def pipeline_ols_allchan(parameters, ieeg_file):

    out_dir = name(parameters, 'ols_chan', ieeg_file)
    rmtree(out_dir, ignore_errors=True)

    try:
        data, names = load('data', parameters, ieeg_file, parameters['ols']['read'])
    except (FileNotFoundError, IndexError):
        return
    tf = compute_timefreq(parameters, data, baseline=True, mean=False)
    tf = get_chantime(parameters, tf, freq_operator='nanmean')

    t = tf.time[0]

    for chan in tf.chan[0][::-1]:
        lg.info(f'{ieeg_file.stem} Fitting OLS on {chan}')
        x = tf(trial=0, chan=chan).flatten(order='F')

        MAT = fit_one_channel(parameters, t, x, names)
        out, result = get_max(parameters, t, x, names, MAT)
        out['chan'] = chan

        divs = []

        t_plot = arange(x.shape[0]) * out['tdiff']
        fig = plot_data_prediction(t_plot, result, names)
        divs.append(to_div(fig))

        fig = plot_coefficient(result)
        divs.append(to_div(fig))

        html_file = out_dir / f'{chan}.html'
        to_html(divs, html_file)

        json_file = html_file.with_suffix('.json')
        with json_file.open('w') as f:
            dump(out, f, indent=2)


def pipeline_ols_summary(parameters, ieeg_file):
    df = import_ols(parameters, ieeg_file)
    if df is None:
        return

    df.to_csv(
        name(parameters, 'ols_tsv') / f'{ieeg_file.stem}.tsv',
        sep='\t', index=False)

    try:
        elec = load('electrodes', parameters, ieeg_file)
    except FileNotFoundError:
        return

    try:
        pial = load('surface', parameters, ieeg_file)
    except FileNotFoundError:
        pial = None

    dat = Data(array(df['rsquared']), chan=array(df['chan']))
    fig = plot_surf(parameters, dat, elec, pial=pial, clim=(0, 0.55), colorscale='Hot')

    plots_dir = name(parameters, 'ols_plot') / ieeg_file.stem
    to_html([to_div(fig), ], plots_dir / 'rsquared.html')

    df = df[df['rsquared'] >= parameters['ols']['threshold']]
    if len(df) == 0:
        lg.warning(f'No channels had a fit better than threshold {parameters["ols"]["threshold"]}')
        return

    params = set(df) - {'rsquared', 'chan'}
    for param in params:
        dat = Data(array(df[param]), chan=array(df['chan']))
        fig = plot_surf(parameters, dat, elec, pial=pial, clim=(nanmin(df[param]), nanmax(df[param])), colorscale='Hot')
        to_html([to_div(fig), ], plots_dir / f'{param.replace(" ", "_")}.html')


def import_ols(parameters, ieeg_file):

    out_dir = name(parameters, 'ols_chan', ieeg_file)

    df = []
    for json_file in out_dir.glob('*.json'):
        with json_file.open() as f:
            df.append(json_load(f))

    if len(df) == 0:
        return

    df = DataFrame(df).sort_values('rsquared', ascending=False).reset_index(drop=True)

    return df


def pipeline_ols_prf(parameters, ieeg_file):

    out_dir = name(parameters, 'ols_chan', ieeg_file)

    for json_file in out_dir.glob('*.json'):
        add_prf_estimates(json_file)
