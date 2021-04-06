from bidso import Task


def name(parameters, ieeg_file, what):

    out_dir = parameters['paths']['output']
    ieeg = Task(ieeg_file)

    if what == 'brainregions':
        out = out_dir / 'brainregions' / f'sub-{ieeg.subject}_ses-{ieeg.session}_acq-{ieeg.acquisition}_brainregions.tsv'

    elif what == 'continuous':
        out = out_dir / 'continuous' / f'{ieeg_file.stem}.html'

    elif what == 'spectrum':
        out = out_dir / 'spectrum' / 'overview' / f'{ieeg_file.stem}.html'

    elif what == 'spectrum_all':
        out = out_dir / 'spectrum' / 'channels' / f'{ieeg_file.stem}.html'

    elif what == 'ols_chan':
        out = out_dir / 'ols' / ieeg_file.stem

    return out
