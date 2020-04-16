from json import load
from numpy import genfromtxt
from bidso.utils import replace_extension
from numpy import percentile


def read_physio(physio_tsv):
    physio_json = replace_extension(physio_tsv, '.json')
    with physio_json.open() as r:
        hdr = load(r)
    tsv = genfromtxt(physio_tsv, delimiter='\t', names=hdr['Columns'])

    # normalize values between 0 and 1
    cols = [x.split('_')[-1] for x in tsv.dtype.names]
    tsv.dtype.names = cols
    for col in tsv.dtype.names[1:]:
        tsv[col] = normalize(tsv[col])
    return tsv


def normalize(x, q=5):
    perc_min = percentile(x, q)
    perc_max = percentile(x, 100 - q)

    return (x - perc_min) / (perc_max - perc_min)
