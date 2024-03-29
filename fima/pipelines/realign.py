from logging import getLogger
import plotly.graph_objects as go
from numpy import isnan, max, mean, NaN, ones, stack, argmin, argmax

from ..viz import to_div, to_html
from ..read import load
from ..spectrum.compute import compute_timefreq, get_chantime
from ..utils import get_events, create_bool
from ..names import name

lg = getLogger(__name__)


def pipeline_realign(parameters, ieeg_file):

    events = load('events', parameters, ieeg_file, parameters['realign']['read']['event_type'])

    data, names = load('data', parameters, ieeg_file, parameters['realign']['read'])
    tf = compute_timefreq(parameters, data, baseline=True, mean=False)
    tf = get_chantime(parameters, tf, freq_operator='nanmean')

    t = tf.time[0]
    n_time = t.shape[0]
    dur = 200  # this in parameters
    range_min = 0
    range_max = n_time - dur
    offset = range_max // 2

    divs = []
    for event in get_events(names):

        i_events = create_bool(names, event)
        X = tf(trial=0)
        X = X[:, :, i_events]

        max_per_chan = max(mean(X, axis=2), axis=1)

        # channels above threshold
        i_chan = max_per_chan >= 2.5  # this in parameters
        if i_chan.sum() == 0:
            lg.info(f'No channel was significant for {event}. This event will be deleted')
            events['onset'][i_events] = NaN
            continue

        lg.info(f'{i_chan.sum()} channels will be used to realigned {event}')

        X = X[i_chan, :, :]
        n_trl = X.shape[2]

        traces = []
        for i_trl in range(n_trl):
            i_x = slice(offset, offset + dur)
            traces.append(
                go.Scatter(
                    x=t[i_x],
                    y=X[:, i_x, i_trl].mean(axis=0),
                ))
        fig = go.Figure(
            data=traces,
            layout=go.Layout(
                showlegend=False,
                title=dict(
                    text=f'{event} not realigned'),
                ),
            )
        divs.append(to_div(fig))

        i_start = (offset * ones(n_trl)).astype('int')

        for i_trl in range(n_trl):
            X_prime = [X[:, i_start[i]:(i_start[i] + dur), i] for i in range(n_trl) if i != i_trl]
            X_prime_mean = mean(stack(X_prime, axis=2), axis=2)

            r2_to_mean = []
            for shift in range(range_min, range_max):
                X_onetrl = X[:, shift:(shift + dur), i_trl]
                d = X_prime_mean - X_onetrl
                r2_to_mean.append(mean(d ** 2))

            i_start[i_trl] = argmin(r2_to_mean)

        # peak shift is necessary, otherwise each fingers (event) is shifted by an arbitrary amount. Now, the peak is in the middle
        X_prime = [X[:, i_start[i]:(i_start[i] + dur), i] for i in range(n_trl)]
        X_output = mean(X_prime, axis=1)
        peak_shift = argmax(X_output.mean(axis=0))

        traces = []
        for i_trl in range(n_trl):
            i_x = slice(offset, offset + dur)
            i_y = slice(i_start[i_trl], i_start[i_trl] + dur)
            traces.append(
                go.Scatter(
                    x=t[i_x] - t[i_x][peak_shift],
                    y=X[:, i_y, i_trl].mean(axis=0),
                ))
        fig = go.Figure(
            data=traces,
            layout=go.Layout(
                showlegend=False,
                title=dict(
                    text=f'{event} realigned'),
                ),
            )
        divs.append(to_div(fig))

        offset_per_trl = t[i_start] - t[offset] + t[i_x][peak_shift]
        events['onset'][i_events] = events['onset'][i_events] + offset_per_trl

    realigned_html = name(parameters, 'realign_plot', ieeg_file)
    to_html(divs, realigned_html)

    realigned_tsv = name(parameters, 'realign_tsv', ieeg_file)
    with realigned_tsv.open('w') as f:
        f.write('onset\tduration\ttrial_type\n')
        for ev in events:
            if not isnan(ev['onset']):
                f.write(f'{ev["onset"]:.3f}\t{ev["duration"]:.3f}\t{ev["trial_type"]}\n')
