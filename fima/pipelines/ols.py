from json import dump
from logging import getLogger

from ..read import load
from ..spectrum.continuous import get_continuous_cht
from ..ols.regressors import find_movement_indices
from ..ols.fit import get_max, fit_one_channel, SIGMAS, DELAYS
from ..viz import to_div, to_html
from ..viz.ols import plot_sigma_delay_mat, plot_coefficient, plot_data_prediction
from ..parameters import RESULTS_DIR

lg = getLogger(__name__)


def pipeline_ols(subject, run):

    tf_cht, events, onsets = get_continuous_cht(subject, run, event_type='cues')
    t = tf_cht.time[0]
    t_diff = t[1] - t[0]

    mov = load('movements', subject, run)
    indices = find_movement_indices(mov, tf_cht.time[0])
    for chan in tf_cht.chan[0]:
        lg.info(f'{subject:<10}/ {run} Fitting OLS on {chan}')
        x = tf_cht(trial=0, chan=chan, trial_axis='trial000000')

        MAT = fit_one_channel(x, indices)
        out, result = get_max(MAT, x, indices)
        out['sigma'] *= t_diff
        out['delay'] *= t_diff
        out['chan'] = chan

        divs = []

        fig = plot_sigma_delay_mat(MAT, SIGMAS * t_diff, DELAYS * t_diff)
        divs.append(to_div(fig))

        fig = plot_coefficient(result)
        divs.append(to_div(fig))

        fig = plot_data_prediction(tf_cht.time[0], result)
        divs.append(to_div(fig))

        html_file = RESULTS_DIR / 'ols' / 'movement' / f'{subject}_run-{run}' / f'{subject}_run-{run}_{chan}.html'
        to_html(divs, html_file)

        json_file = html_file.with_suffix('.json')
        with json_file.open('w') as f:
            dump(out, f, indent=2)
