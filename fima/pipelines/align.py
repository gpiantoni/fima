from numpy import isnan
from bidso.utils import replace_underscore

from ..read import load
from ..align.maxmin import main_func
from ..names import name


def pipeline_align(parameters, ieeg_file):

    event_type = 'cues'

    data, names = load('data', parameters, ieeg_file, event_type)
    out = main_func(parameters, data, names)

    events = load('events', parameters, ieeg_file, event_type)

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
