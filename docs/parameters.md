# PARAMETERS
Information to store in `parameters.json` file.


  - paths:
    - input: str, path to bids folder,
    - freesurfer_subjects_dir: str, path to freesurfer folder,
    - output: str, path to output folder which will contain the results
  - data:
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
      - type: "zscore"

    "select": {
      "freq": [60, 150],
      "time": 0.3
