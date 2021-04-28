from numpy import isnan
from bidso.utils import replace_underscore

from ..read import load
from ..names import name


def pipeline_align(parameters, ieeg_file):

    event_type = 'cues'

    data, names = load('data', parameters, ieeg_file, event_type)

    for critical_point in out.dtype.names:

        realigned = events.copy()

        realigned['onset'] = events['onset'] + out[critical_point]
        good_events = ~isnan(realigned['onset'])
        realigned = realigned[good_events]
        realigned['duration'] = 0

        realigned_dir = name(parameters, 'realigned_dir')
        out_tsv = realigned_dir / replace_underscore(ieeg_file.name, critical_point.replace('_', '') + '.tsv')

        with out_tsv.open('w') as f:
            f.write('onset\tduration\ttrial_type\n')
            for evt in realigned:
                f.write(f'{evt["onset"]:.3f}\t{evt["duration"]:.3f}\t{evt["trial_type"]}\n')


def find_min_max(t, dat, info, index=False):
    i_t = (t >= info['time'][0]) & (t <= info['time'][1])
    t_offset = where(i_t)[0][0]

    x = dat[i_t]
    if isnan(x).any() or (max(x) < info['threshold']['high']):
        return NaN, NaN

    i_max = argmax(dat[i_t])

    if i_max == 0:
        return NaN, NaN

    index_max = t_offset + i_max
    bool_threshold = dat[:index_max] <= info['threshold']['low']

    if bool_threshold.any():  # has to go below first threshold
        index_min = where(bool_threshold)[0][-1] + 1
    else:
        index_min = NaN

    if index:
        return index_min, index_max
    else:
        return t[index_min], t[index_max]
