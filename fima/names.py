from bidso import Task


def name(parameters, ieeg_file, what):

    out_dir = parameters['paths']['output']
    ieeg = Task(ieeg_file)

    if what == 'brainregions':
        out = out_dir / 'brainregions' / f'sub-{ieeg.subject}_ses-{ieeg.session}_acq-{ieeg.acquisition}_brainregions.tsv'

    elif what == 'continuous':
        out = out_dir / 'continuous' / f'{ieeg_file.stem}.html'

    return out
