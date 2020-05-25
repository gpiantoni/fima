from ..fitting.general import fit_data, get_trialdata
from ..fitting.timebased import MODELS
from ..fitting.viz import estimate_and_plot, plot_prf_results
from ..fitting.utils import group_per_condition
from ..spectrum.compute import compute_timefreq, get_chantime
from ..read import load
from ..viz import to_div, to_html
from ..parameters import FITTING_DIR, SUBJECTS, P

from numpy import nanmax
from wonambi.trans import math


FOLDER_NAME = '400ms'


def pipeline_fitting_all(model_name=None, response=None, subject_only=None):

    if model_name is None:
        model_names = MODELS
    else:
        model_names = [model_name, ]
    event_type = 'cues'

    for model_name in model_names:
        values = []
        for subject, runs in SUBJECTS.items():
            if subject_only is not None and subject != subject_only:
                continue

            for run in runs:
                print(f'{subject} / {run}')
                try:
                    vals = pipeline_fitting(subject, run, model_name, response=response, event_type=event_type)
                    print(vals)
                    values.append(vals)
                except Exception as err:
                    print(err)
                    values.append([])

        if subject_only is not None:
            csv_file = FITTING_DIR / model_name / FOLDER_NAME / f'recap_{event_type}.csv'
            with csv_file.open('w') as f:
                for line in values:
                    f.write('\t'.join(line) + '\n')


def pipeline_fitting(subject, run, model_name, response=None, event_type='cues'):
    """
    response : str
        if None, it's trial-based
        'mean' : take the mean for that channel
    """

    data, names = load('data', subject, run, event_type=event_type)
    electrodes = load('electrodes', subject, run)
    surf = load('surface', subject, run)

    tf_m = compute_timefreq(data, baseline=P['spectrum']['baseline']['type'], mean=False)
    data = get_chantime(tf_m)

    model = MODELS[model_name]
    if model['type'] == 'trial-based' and response is None:
        data = math(data, operator_name='mean', axis='time')
    elif model['type'] == 'time-based' and response is not None:
        raise ValueError('You cannot use a time-based model and use an empirical response')

    if model.get('grouped', False):
        data, names = group_per_condition(data, names)

    if response is None:
        parallel = True
    else:
        parallel = False

    model['response'] = response

    result = fit_data(model, data, names, parallel=parallel)

    divs = []

    fig = estimate_and_plot(get_trialdata(data), model, names, result, data.chan[0])
    divs.append(to_div(fig))

    for param in (['rsquared', ] + list(model['parameters'])):
        if param == 'rsquared' or model['parameters'][param]['to_plot']:
            fig = plot_prf_results(result, param, data.chan[0], electrodes, surf)
            divs.append(to_div(fig))

    html_file = FITTING_DIR / model_name / FOLDER_NAME / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)

    output = [
        f"{nanmax(result['rsquared']):0.3f}",
        f"{(result['rsquared'] >= 0.10).sum():d} / {len(result):d}",
        ]
    csv_file = html_file.with_suffix('.csv')
    export_results(result, data, csv_file)

    return output


def export_results(result, data, out_file):
    with out_file.open('w') as f:
        f.write('chan\t' + '\t'.join(result.dtype.names) + '\n')
        for chan, r in zip(data.chan[0], result):
            f.write(chan + '\t' + '\t'.join(f'{x:0.3f}' for x in r) + '\n')
