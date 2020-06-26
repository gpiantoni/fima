Module fima.fitting.design_matrix
=================================

Functions
---------

    
`make_design_matrix(names, model)`
:   Parameters
    ----------
    names : list of str
        list of events
    model : str
        'fingers' (5 columns, open and close are together)
        'movements' (2 columns, fingers are together)
        'cues' (10 columns, all fingers, open and close)
        'open_v_close' (5 columns, open is +1, close is -1)
    
    Returns
    -------
    ndarray
        design matrix (n rows is the number of events, n col depends on "model")