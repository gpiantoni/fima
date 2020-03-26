from wonambi.trans import apply_baseline, timefrequency

tf = timefrequency(data, 'spectrogram', duration=0.3, overlap=0.9, taper='dpss', halfbandwidth=10)
tf_c = apply_baseline(tf, time=(-0.4, 0), baseline='dB')
