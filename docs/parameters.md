# PARAMETERS
Information to store in `parameters.json` file.


  - paths:
    - input: str, path to bids folder,
    - movements: str, path to movements (should have the same prefix as `_events.tsv` but ends with `_dataglove.tsv`)
    - freesurfer_subjects_dir: str, path to freesurfer folder,
    - output: str, path to output folder which will contain the results
  - read:
    - event_type : str, one of 'cues', 'open', 'close', 'movements', 'extension', 'flexion'
    - pre: float, time in s to include before the events
    - post: float, time in s to include after the event
  - spectrum:
    - method: str, "spectrogram" or "morlet" or "hilbert"
    - window_size: float
    - taper: "dpss" or "hann"
    - baseline:
      - apply: bool
      - time: list of two values (start and end time of the baseline)
      - common: bool, use the same baseline for all the trials
      - type: "zscore", "dB"
    - select:
      - freq: [float, float], frequency range to include
      - timeinterval: float, center of the time window
  - ols:
    - threshold: float
    - window:
      - method: str, 'gaussian' or 'gamma'
      - onset_percent: float, value between 0 and 1 to calculate onset of the gaussian or gamma window
  - viz:
    - colorscale: str, 'Jet'
    - continuous:
      - yaxis: [float, float], amplitude range
    - tfr:
      - max: float
    - tfr_mean:
      - max: float
