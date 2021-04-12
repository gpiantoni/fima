from numpy import isnan

from ..read import load
from ..align.maxmin import main_func
from ..names import name


def pipeline_align(parameters, ieeg_file):

    data, names = load('data', parameters, ieeg_file)
    out = main_func(parameters, data, names)

    events = load('events', parameters, ieeg_file)

    for critical_point in out.dtype.names:

        realigned = events.copy()

        realigned['onset'] = events['onset'] + out[critical_point]
        good_events = ~isnan(realigned['onset'])
        realigned = realigned[good_events]
        realigned['duration'] = 0

        realigned_dir = names('realigned_dir', parameters)
        out_tsv = realigned_dir / replace_underscore(ieeg_file.name, critical_point.replace('_', '') + '.tsv')


