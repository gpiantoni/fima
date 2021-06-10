from numpy import where
from pandas import merge, read_csv, concat, MultiIndex, isnull
from bidso import file_Core

from .regressors import compute_canonical
from ..names import name


COLUMNS = {
    'recording/subject': 'subject',
    'recording/session': 'session',
    'recording/acquisition': 'acquisition',
    'recording/run': 'run',
    'channel/chan': 'chan',
    'channel/a2009s': 'aparc.a2009s',
    'channel/DKTatlas': 'aparc.DKTatlas',
    'channel/BA': 'BA_exvivo.thresh',
    'estimate/rsquared': 'rsquared',
    'estimate/peak': 'loc',
    'estimate/onset': 'onset',
    'estimate/skewness': 'a',
    'estimate/spread': 'scale',
    'estimate/const': 'const',
    'extension/thumb': 'thumb extension',
    'extension/index': 'index extension',
    'extension/middle': 'middle extension',
    'extension/ring': 'ring extension',
    'extension/little': 'little extension',
    'flexion/thumb': 'thumb flexion',
    'flexion/index': 'index flexion',
    'flexion/middle': 'middle flexion',
    'flexion/ring': 'ring flexion',
    'flexion/little': 'little flexion',
    'prf_ext/rsquared': 'extension rsquared',
    'prf_ext/finger': 'extension loc',
    'prf_ext/spread': 'extension scale',
    'prf_flex/rsquared': 'flexion rsquared',
    'prf_flex/finger': 'flexion loc',
    'prf_flex/spread': 'flexion scale',
    'flexext/diff': 'params diff',
    'flexext/corr': 'params corr',
    }


def import_all_ols(parameters):

    df_ols = import_df_ols(parameters)
    df_regions = import_df_regions(parameters)

    df = merge(df_ols, df_regions, how='left', on=['subject', 'session', 'acquisition', 'chan'])

    df = df.sort_values('rsquared', ascending=False).reset_index(drop=True)

    if 'thumb close' in df.columns:
        columns = {k.replace('flexion', 'close'): v.replace('flexion', 'close') for k, v in COLUMNS.items()}
        columns = {k.replace('extension', 'open'): v.replace('extension', 'open') for k, v in columns.items()}
    else:
        columns = COLUMNS

    missing_columns = set(df.columns) - set(columns.values())
    print('These columns will not be included in overview dataset: ' + ', '.join(missing_columns))

    # exclude columns which are in the overview but were not computed
    columns = {k: v for k, v in columns.items() if v in df.columns}
    df1 = df[list(columns.values())]
    df1.columns = MultiIndex.from_tuples([tuple(k.split('/')) for k in columns.keys()])

    df1.loc[isnull(df1['channel']['DKTatlas']), ('channel', 'DKTatlas')] = 'unknown'
    df1.loc[isnull(df1['channel']['a2009s']), ('channel', 'a2009s')] = 'unknown'
    df1.loc[isnull(df1['channel']['BA']), ('channel', 'BA')] = 'unknown'

    return df1


def import_df_ols(parameters):
    """Compute onset as well"""
    TSV_DIR = name(parameters, 'ols_tsv')

    all_ols = []
    for tsv_file in TSV_DIR.glob('*.tsv'):
        bids = file_Core(tsv_file.name)
        ols = read_csv(tsv_file, sep='\t')
        ols['subject'] = bids.subject
        ols['session'] = bids.session
        ols['run'] = bids.run
        ols['acquisition'] = bids.acquisition
        all_ols.append(ols)

    ols = concat(all_ols, sort=False)   # pandas throws a warning when data is not complete

    return ols


def import_df_regions(parameters):
    regions_dir = name(parameters, 'brainregions_dir')

    all_df = []
    for tsv_file in regions_dir.glob('*_brainregions.tsv'):

        bids = file_Core(tsv_file.name)

        temp = read_csv(tsv_file, sep='\t')
        temp['subject'] = bids.subject
        temp['session'] = bids.session
        temp['acquisition'] = bids.acquisition
        all_df.append(temp)

    regions = concat(all_df)
    regions.drop(['x', 'y', 'z'], axis=1, inplace=True)
    return regions


def compute_onset(parameters, row):
    """Compute onset calculating when the estimated function raises above a
    certain threshold (percent of the max)

    Parameters
    ----------
    row : one row of DataFrame

    TODO
    ----
    - tdiff should be in row (new version has it, but older version not)

    """
    if parameters['ols']['window']['method'] == 'gaussian':
        params = [row['loc'], row['scale']]
    else:
        params = [row['loc'], row['scale'], row['a']]

    t, resp = compute_canonical(
        parameters,
        [0, row['tdiff']],
        params
        )
    thresh = resp.max() * parameters['ols']['results']['onset_percent']

    i_onset = where(resp >= thresh)[0][0]
    return t[i_onset]
