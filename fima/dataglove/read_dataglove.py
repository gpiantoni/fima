from json import load
from numpy import genfromtxt
from bidso.utils import replace_extension


def read_physio(physio_tsv):
    physio_json = replace_extension(physio_tsv, '.json')
    with physio_json.open() as r:
        hdr = load(r)
    tsv = genfromtxt(physio_tsv, delimiter='\t', names=hdr['Columns'])
    return tsv
