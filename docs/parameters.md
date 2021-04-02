# PARAMETERS
Information to store in `parameters.json` file.


  - paths:
    - input: str, path to bids folder,
    - freesurfer_subjects_dir: str, path to freesurfer folder,
    - output: str, path to output folder which will contain the results
  - data:
    - event_type : str, "cues" etc
    - pre: float, time in s to include before the events
    - post: float, time in s to include after the event

  "spectrum": {
    "method": "spectrogram",
    "window_size": 0.3,
    "taper": "dpss",
    "baseline": {
      "apply": true,
      "time": [-1, -0.5],
      "common": true,
      "type": "zscore"
    },
    "select": {
      "freq": [60, 150],
      "time": 0.3
```
