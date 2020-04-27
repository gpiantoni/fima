from ..fitting.general import fit_data, get_trialdata
from ..fitting.trialbased import MODELS
from ..fitting.viz import estimate_and_plot, plot_prf_results
from ..spectrum.compute import compute_timefreq, get_chantime
from ..read import load
from ..viz import to_div, to_html, to_png
from ..parameters import FITTING_DIR, SUBJECTS


def pipeline_fitting_all(model_name=None):

    if model_name is None:
        model_names = MODELS
    else:
        model_names = [model_name, ]
    event_type = 'cues'

    values = []
    for model_name in model_names:
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


def pipeline_fitting(subject, run, model_name, event_type='cues'):

    data, names = load('data', subject, run, event_type=event_type)
    electrodes = load('electrodes', subject, run)
    surf = load('surface', subject, run)

    tf_m = compute_timefreq(data, baseline=True, mean=False)
    tf_cht = get_chantime(tf_m)

    model = MODELS[model_name]

    result = fit_data(model, tf_cht, names)

    divs = []

    fig = estimate_and_plot(get_trialdata(tf_cht), model, names, result, data.chan[0])
    divs.append(to_div(fig))

    for param in (list(model['parameters']) + ['rsquared', ]):
        if param == 'rsquared' or model['parameters'][param]['to_plot']:
            png_name = f'img/{subject}_run-{run}_{event_type}_{param}.png'
            png_file = FITTING_DIR / model_name / png_name
            fig = plot_prf_results(result, param, data.chan[0], electrodes, surf)
            to_png(fig, png_file)
            divs.append(f"<div><img src='{png_name}'></div>")

    html_file = FITTING_DIR / model_name / f'{subject}_run-{run}_{event_type}.html'
    to_html(divs, html_file)

    output = [
        f"{result['rsquared'].max():0.3f}",
        f"{(result['rsquared'] >= 0.10).sum():d} / {len(result):d}",
        ]
    return output
