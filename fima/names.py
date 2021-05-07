from bidso import Task


def name(parameters, what, ieeg_file=None):

    out_dir = parameters['paths']['output']
    if ieeg_file is not None:
        ieeg = Task(ieeg_file)

    if what == 'surface_dir':
        out = out_dir / 'surfaces' / ieeg.subject
        out.mkdir(parents=True, exist_ok=True)

    if what == 'brainregions_dir':
        out = out_dir / 'brainregions' / 'tsv'
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'brainregions_plot':
        out = out_dir / 'brainregions' / 'plots' / f'sub-{ieeg.subject}_ses-{ieeg.session}_acq-{ieeg.acquisition}_brainregions.html'

    elif what == 'brainregions':
        tsv_dir = out_dir / 'brainregions' / 'tsv'
        tsv_dir.mkdir(parents=True, exist_ok=True)
        out = tsv_dir / f'sub-{ieeg.subject}_ses-{ieeg.session}_acq-{ieeg.acquisition}_brainregions.tsv'

    elif what == 'dataglove':
        out = out_dir / 'dataglove'
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'timepoints':
        out = out_dir / 'timepoints' / 'timings' / f'{ieeg_file.stem}.npy'
        out.parent.mkdir(parents=True, exist_ok=True)

    elif what == 'timepoints_plot':
        out = out_dir / 'timepoints' / 'plots' / f'{ieeg_file.stem}.html'
        out.parent.mkdir(parents=True, exist_ok=True)

    elif what == 'continuous':
        out = out_dir / 'continuous' / f'{ieeg_file.stem}.html'

    elif what == 'spectrum':
        out = out_dir / 'spectrum' / 'overview' / f'{ieeg_file.stem}.html'

    elif what == 'ols_chan':
        out = out_dir / 'ols' / ieeg_file.stem
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'ols_tsv':
        out = out_dir / 'ols' / 'tsv'
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'ols_summary':
        out = out_dir / 'ols' / 'summary'
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'ols_plot':
        out = out_dir / 'ols' / 'plots'
        out.mkdir(parents=True, exist_ok=True)

    return out
