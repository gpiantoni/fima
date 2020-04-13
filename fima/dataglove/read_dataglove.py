from json import load
from numpy import genfromtxt
from bidso.utils import replace_extension


def _read_physio(physio_tsv):
    physio_json = replace_extension(physio_tsv, '.json')
    with physio_json.open() as r:
        hdr = load(r)
    print(hdr['StartTime'])
    tsv = genfromtxt(physio_tsv, delimiter='\t', names=hdr['Columns'])
    return tsv


def _read_events(physio_tsv):
    print('only run-1!!!!')
    events_tsv = physio_tsv.parent / (physio_tsv.name[:-34] + '_run-1_events.tsv')
    dtypes = [
        ('onset', 'float'),
        ('duration', 'float'),
        ('trial_type', 'U4096'),
        ('response_time', 'float'),
        ('value', 'int')
    ]
    events = genfromtxt(events_tsv, delimiter='\t', skip_header=1, dtype=dtypes)
    return events
