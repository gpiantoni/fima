from ..fitting.general import fit_data, get_trialdata
from ..fitting.trialbased import MODELS
from ..fitting.viz import estimate_and_plot, plot_prf_results
from ..spectrum.compute import compute_timefreq, get_chantime
from ..read import load
from ..viz import to_div, to_html
from ..parameters import FITTING_DIR, SUBJECTS

from wonambi.trans import math


def pipeline_fitting_all(model_name=None):

    if model_name is None:
        model_names = MODELS
    else:
        model_names = [model_name, ]
    event_type = 'cues'

    for model_name in model_names:
        values = []
        for subject, runs in SUBJECTS.items():

            for run in runs:
                print(f'{subject} / {run}')
                try:
                    vals = pipeline_fitting(subject, run, model_name, event_type)
                    values.append(vals)
                except Exception as err:
                    print(err)
                    values.append([])

        csv_file = FITTING_DIR / model_name / f'recap_{event_type}.csv'
        with csv_file.open('w') as f:
            for l in values:
                f.write('\t'.join(l) + '\n')


def pipeline_fitting(subject, run, model_name, response=None, event_type='cues'):
    """
    response : str
        if None, it's trial-based
        'mean' : take the mean for that channel
    """
    data, names = load('data', subject, run, event_type=event_type)
    electrodes = load('electrodes', subject, run)
    surf = load('surface', subject, run)

    tf_m = compute_timefreq(data, baseline=True, mean=False)
    data = get_chantime(tf_m)
    if response is None:
        data = math(data, operator_name='mean', axis='time')
        parallel = True
    else:
        parallel = False

    model = MODELS[model_name]
    model['response'] = response

    result = fit_data(model, data, names, parallel=parallel)

    divs = []

    fig = estimate_and_plot(get_trialdata(data), model, names, result, data.chan[0])
    divs.append(to_div(fig))

    for param in (['rsquared', ] + list(model['parameters'])):
        if param == 'rsquared' or model['parameters'][param]['to_plot']:
            fig = plot_prf_results(result, param, data.chan[0], electrodes, surf)
            divs.append(to_div(fig))

    html_file = FITTING_DIR / model_name / str(model['response']) / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)

    output = [
        f"{result['rsquared'].max():0.3f}",
        f"{(result['rsquared'] >= 0.10).sum():d} / {len(result):d}",
        ]
    return output
