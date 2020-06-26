Module fima.read
================

Functions
---------

    
`load(what, subject, run=None, acq=None, event_type=None)`
:   WHAT:
      - 'data' returns: ChanTime, event_names
      - 'events' returns: ndarray
      - 'dataglove' returns: ndarray
      - 'movements' returns: ndarray
      - 'electrodes'
      - 'surface'
    
    EVENT_TYPE
      - cues : all cues (to open and close)
      - open : cues to open fingers
      - close : cues to close fingers
      - movements : all actual movements (from dataglove)
      - extension : actual extension of all fingers
      - flexion : actual flexion of all fingers

    
`select_events(subject, run, t)`
: