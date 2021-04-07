from numpy import where
from pandas import merge, read_csv, concat, MultiIndex

from .regressors import compute_canonical

COLUMNS = {
    'recording/subject': 'subject',
    'recording/run': 'run',
    'channel/type': 'grid_type',
    'channel/chan': 'chan',
    'channel/brainregion': 'a2009s',
    'channel/BA': 'BA',
    'estimate/rsquared': 'rsquared',
    'estimate/onset': 'onset',
    'estimate/skewness': 'a',
    'estimate/spread': 'scale',
    'estimate/const': 'const',
    'extension/corr': 'extension corr',
    'extension/finger': 'extension loc',
    'extension/spread': 'extension scale',
    'flexion/corr': 'flexion corr',
    'flexion/finger': 'flexion loc',
    'flexion/spread': 'flexion scale',
    'flexext/diff': 'params diff',
    'flexext/corr': 'params corr',
}


def import_all_ols(parameters):

    df_ols = import_df_ols()
    df_regions = import_df_regions()

    df = merge(df_ols, df_regions, how='left', on=['subject', 'chan'])

    df = df.sort_values('rsquared', ascending=False).reset_index(drop=True)

    missing_columns = set(df.columns) - set(COLUMNS.values())
    print('Missing columns: ' + ', '.join(missing_columns))

    df1 = df[list(COLUMNS.values())]
    df1.columns = MultiIndex.from_tuples([tuple(k.split('/')) for k in COLUMNS.keys()])

    return df1


def import_df_ols():
    """Compute onset as well"""
    SUMMARY_DIR = RESULTS_DIR / 'ols' / 'summary'

    all_ols = []
    for tsv_file in SUMMARY_DIR.glob('*.tsv'):
        subject, run = tsv_file.stem.split('_')[2:4]
        ols = read_csv(tsv_file, sep='\t')
        ols['subject'] = subject
        ols['run'] = run[4:]
        all_ols.append(ols)

    ols = concat(all_ols, sort=False)   # pandas throws a warning when data is not complete

    onsets = []
    for row in ols.itertuples():
        onsets.append(compute_onset(row, 0.1))
    ols['onset'] = onsets

    return ols


def import_df_regions():
    regions_dir = RESULTS_DIR / 'brainregions'

    all_df = []
    for tsv_file in regions_dir.glob('*_regions.tsv'):
        subject, run = tsv_file.stem.split('_')[:2]

        temp = read_csv(tsv_file, sep='\t')
        temp['subject'] = subject
        all_df.append(temp)

    regions = concat(all_df)
    regions.drop(['x', 'y', 'z'], axis=1, inplace=True)
    return merge(regions, GRID_TYPES, on=['subject', ])


def compute_onset(row, percent=0.1):
    """Compute onset calculating when the estimated function raises above a
    certain threshold (percent of the max)

    Parameters
    ----------
    row : one row of DataFrame

    TODO
    ----
    - tdiff should be in row (new version has it, but older version not)

    - implement for gaussian
    """
    tdiff = 0.009765625  # this should be row.tdiff

    t, resp = compute_canonical(
        [0, tdiff],
        [row.loc, row.scale, row.a],
        )
    thresh = resp.max() * percent

    i_onset = where(resp >= thresh)[0][0]
    return t[i_onset]
