from numpy import (
    argmax,
    empty,
    isnan,
    max,
    NaN,
    where,
    )
from wonambi.trans import select

from ..utils import create_bool
from ..parameters import EVENTS, P


def main_func(data):
    data = select(data, time=P['align']['time'])


def find_max_min(data, names):

    t = data.time[0]
    dat_cond = data(trial=0)

    all_offsets = empty((data.number_of('trial_axis')[0]), [('t_inflection', '<f8'), ('t_midpoint', '<f8'), ('t_peak', '<f8')])

    for ev in EVENTS:
        select_trl = create_bool(names, ev)
        dat_allchan = dat_cond[:, :, select_trl]

        dat_mean = dat_allchan.mean(axis=2)
        bool_chan = max(dat_mean, axis=1) >= P['align']['threshold']['high']
        dat = dat_allchan[bool_chan, :, :]

        n_chan = bool_chan.sum()
        n_trl = select_trl.sum()

        timings = empty((n_chan, n_trl), dtype=([('peak', '<f8'), ('t_inflection', '<f8'), ('t_midpoint', '<f8'), ('t_peak', '<f8')]))

        indices_max = argmax(dat, axis=1)
        values_max = max(dat, axis=1)

        indices_min = empty((n_chan, n_trl), dtype='int')
        for i_chan in range(n_chan):
            for i_trl in range(n_trl):
                i_max = indices_max[i_chan, i_trl]
                bool_threshold = dat[i_chan, :i_max, i_trl] <= P['align']['threshold']['low']
                if i_max == 0 or bool_threshold.all() is False:
                    timings['peak'][i_chan, i_trl] = NaN
                    indices_min[i_chan, i_trl] = 0
                else:
                    indices_min[i_chan, i_trl] = where(bool_threshold)[0][-1]

        timings['peak'] = values_max
        timings['t_peak'] = t[indices_max]
        timings['t_inflection'] = t[indices_min]
        timings['t_midpoint'] = (timings['t_inflection'] + timings['t_peak']) / 2

        for param in all_offsets.dtype.names:
            timings[param][isnan(timings['peak'])] = NaN

        for param in all_offsets.dtype.names:
            offset = empty(n_trl, dtype='<f8')
            for i_trl in range(n_trl):
                # offset[i_trl] = timings[param][timings['peak'][:, i_trl] >= P['align']['threshold']['high'], i_trl].mean()
                offset[i_trl] = timings[param][:, i_trl].mean()
            all_offsets[param][select_trl] = offset

    return all_offsets
