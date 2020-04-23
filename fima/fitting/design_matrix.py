from numpy import zeros


FINGERS = ['thumb', 'index', 'middle', 'ring', 'little']
MOVEMENTS = ['close', 'open']


def make_design_matrix(names, model):
    """
    Parameters
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
    """

    if model == 'fingers':
        EVENTS = FINGERS
    elif model == 'movements':
        EVENTS = MOVEMENTS
    elif model == 'cues':
        EVENTS = []
        for m in MOVEMENTS:
            for f in FINGERS:
                EVENTS.append(f'{f} {m}')

    st = zeros((names.shape[0], len(EVENTS)))
    for i, ev in enumerate(names):
        for i_col, col_name in enumerate(EVENTS):
            if col_name in ev:
                st[i, i_col] = 1

    return st
