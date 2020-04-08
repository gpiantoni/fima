from bidso.utils import read_tsv
from xelo2.io.tsv import save_tsv
from numpy import empty
from shutil import copytree

from ..parameters import NYU_DIR, BIDS_DIR


def add_nyu_subjects():
    """

    TODO
    ----
    add line to participants.tsv
    """
    for nyu_sub in NYU_DIR.glob('sub-*'):
        out_dir = copytree(nyu_sub, BIDS_DIR / nyu_sub.name)

    for event_file in out_dir.rglob('*_events.tsv'):
        fix_nyu_events(event_file)

    for channel_file in out_dir.rglob('*_channels.tsv'):
        fix_nyu_channels(channel_file)


def fix_nyu_events(event_file):
    tsv = read_tsv(event_file)
    dtypes = [
        ('onset', '<f8'),
        ('duration', '<f8'),
        ('trial_type', '<U4096'),
        ]

    events = empty(tsv.shape[0], dtype=dtypes)
    events['onset'] = tsv['onset']
    events['duration'] = tsv['duration']
    events['trial_type'] = tsv['trial_name']
    save_tsv(event_file, events)


def fix_nyu_channels(channel_file):
    tsv = read_tsv(channel_file)
    tsv['type'] = [x.upper() for x in tsv['type']]
    save_tsv(channel_file, tsv)
