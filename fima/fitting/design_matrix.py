from numpy import zeros


FINGERS = ['little', 'ring', 'middle', 'index', 'thumb']
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

    if model in ('fingers', 'open_v_close'):
        EVENTS = FINGERS
    elif model == 'movements':
        EVENTS = MOVEMENTS
    elif model == 'cues':
        EVENTS = []
        for m in MOVEMENTS:
            for f in FINGERS:
                EVENTS.append(f'{f} {m}')

    DTYPES = []
    for col_name in EVENTS:
        DTYPES.append((col_name, '<f8'))

    st = zeros((names.shape[0], ), dtype=DTYPES)
    for i, ev in enumerate(names):
        for col_name in EVENTS:
            if col_name in ev:
                if model == 'open_v_close' and 'close' in ev:
                    st[col_name][i] = -1
                else:
                    st[col_name][i] = 1

    return st
