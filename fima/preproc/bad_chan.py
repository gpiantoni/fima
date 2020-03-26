from wonambi.trans import montage, concatenate, math


def find_good_channels(data):
    data = montage(data, ref_chan=list(data.chan[0][:1]))  # reference to first channel
    data = concatenate(data, axis='time')

    data = math(data, operator_name='std', axis='time')
    chans = data.chan[0][data(trial=0) < 300]

    return chans
