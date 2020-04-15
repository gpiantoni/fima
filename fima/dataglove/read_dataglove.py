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
    stem = '_'.join([x for x in physio_tsv.stem[:-10].split('_') if not x.startswith('rec-')]) + 'events.tsv'
    events_tsv = physio_tsv.parent / stem
    dtypes = [
        ('onset', 'float'),
        ('duration', 'float'),
        ('trial_type', 'U4096'),
        ('response_time', 'float'),
        ('value', 'int')
    ]
    events = genfromtxt(events_tsv, delimiter='\t', skip_header=1, dtype=dtypes)
    return events
