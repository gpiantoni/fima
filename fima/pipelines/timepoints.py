from numpy import (
    argmax,
    isnan,
    NaN,
    save,
    where,
    zeros,
    )

from ..spectrum.compute import compute_timefreq, get_chantime
from ..read import load
from ..names import name
from ..viz.timepoints import plot_singletrial_tf_and_peaks
from ..viz.utils import to_html


def pipeline_timepoints(parameters, ieeg_file):

    data, names = load('data', parameters, ieeg_file)
    tf = compute_timefreq(parameters, data, baseline=True, mean=False)
    tf = get_chantime(parameters, tf, freq_operator='nanmean')

    t = tf.time[0]
    n_chan, _, n_trl = tf.data[0].shape
    indices = zeros((n_chan, n_trl), dtype=[('crossthresh', 'int'), ('peak', 'int')])

    for i_chan in range(n_chan):
        for i_trl in range(n_trl):
            indices['crossthresh'][i_chan, i_trl], indices['peak'][i_chan, i_trl] = find_threshold_points(t, tf.data[0][i_chan, :, i_trl], parameters['timepoints'])

    timepoints = zeros((n_chan, n_trl), dtype=[('crossthresh', 'float64'), ('peak', 'float64')])
    for timepoint in indices.dtype.names:
        timepoints[timepoint] = t[indices[timepoint]]
        timepoints[timepoint][indices[timepoint] == 0] = NaN

    timepoint_file = name(parameters, 'timepoints', ieeg_file)
    save(timepoint_file, timepoints)

    timepoint_file = name(parameters, 'timepoints_plot', ieeg_file)
    divs = plot_singletrial_tf_and_peaks(parameters, tf, indices, names)
    to_html(divs, timepoint_file)


def find_threshold_points(t, dat, info):
    """
    0 means that it does not exist
    """
    i_t = (t >= info['time'][0]) & (t <= info['time'][1])
    t_offset = where(i_t)[0][0]

    x = dat[i_t]
    if isnan(x).any() or (max(x) < info['threshold']['high']):
        return 0, 0

    i_max = argmax(dat[i_t])

    if i_max == 0:
        return 0, 0

    index_max = t_offset + i_max
    bool_threshold = dat[:index_max] <= info['threshold']['low']

    if bool_threshold.any():  # has to go below first threshold
        index_min = where(bool_threshold)[0][-1] + 1
    else:
        index_min = 0

    return index_min, index_max
