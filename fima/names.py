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

    elif what == 'realign_tsv':
        out = out_dir / 'realigned' / 'tsv' / f'{ieeg_file.stem}.tsv'
        out.parent.mkdir(parents=True, exist_ok=True)

    elif what == 'realign_plot':
        out = out_dir / 'realigned' / 'plots' / f'{ieeg_file.stem}.html'
        out.parent.mkdir(parents=True, exist_ok=True)

    elif what == 'timepoints':
        event_type = parameters['timepoints']['read']['event_type']
        out = out_dir / 'timepoints' / event_type / 'timings' / f'{ieeg_file.stem}.npy'
        out.parent.mkdir(parents=True, exist_ok=True)

    elif what == 'timepoints_plot':
        event_type = parameters['timepoints']['read']['event_type']
        out = out_dir / 'timepoints' / event_type / 'plots' / f'{ieeg_file.stem}.html'
        out.parent.mkdir(parents=True, exist_ok=True)

    elif what == 'continuous':
        out = out_dir / 'continuous' / f'{ieeg_file.stem}.html'

    elif what == 'spectrum':
        event_type = parameters['spectrum']['read']['event_type']
        out = out_dir / 'spectrum' / event_type / 'overview' / f'{ieeg_file.stem}.html'

    elif what == 'ols_chan':
        event_type = parameters['ols']['read']['event_type']
        out = out_dir / 'ols' / event_type / ieeg_file.stem
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'ols_tsv':
        event_type = parameters['ols']['read']['event_type']
        out = out_dir / 'ols' / event_type / 'tsv'
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'ols_summary':
        event_type = parameters['ols']['read']['event_type']
        out = out_dir / 'ols' / event_type / 'summary'
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'ols_plot':
        event_type = parameters['ols']['read']['event_type']
        out = out_dir / 'ols' / event_type / 'plots'
        out.mkdir(parents=True, exist_ok=True)

    elif what == 'paper':
        out = out_dir / 'paper'
        out.mkdir(parents=True, exist_ok=True)

    return out
