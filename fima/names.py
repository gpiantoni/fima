from bidso import Task


def name(parameters, what, ieeg_file=None):

    out_dir = parameters['paths']['output']
    if ieeg_file is not None:
        ieeg = Task(ieeg_file)

    if what == 'brainregions_dir':
        out = out_dir / 'brainregions'

    elif what == 'brainregions':
        out = out_dir / 'brainregions' / f'sub-{ieeg.subject}_ses-{ieeg.session}_acq-{ieeg.acquisition}_brainregions.tsv'

    elif what == 'continuous':
        out = out_dir / 'continuous' / f'{ieeg_file.stem}.html'

    elif what == 'spectrum':
        out = out_dir / 'spectrum' / 'overview' / f'{ieeg_file.stem}.html'

    elif what == 'spectrum_all':
        out = out_dir / 'spectrum' / 'channels' / f'{ieeg_file.stem}.html'

    elif what == 'ols_chan':
        out = out_dir / 'ols' / ieeg_file.stem

    elif what == 'ols_summary':
        out = out_dir / 'ols' / 'summary'
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'ols_plot':
        out = out_dir / 'ols' / 'plots'
        out.mkdir(parents=True, exist_ok=True)

    return out
