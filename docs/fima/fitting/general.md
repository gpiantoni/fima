Module fima.fitting.general
===========================

Functions
---------

    
`estimate(model, names, x0, n_points=None)`
:   

    
`fit_data(model, data, names, parallel=True)`
:   

    
`fitting(y, model, names)`
:   

    
`get_trialdata(data)`
:   

    
`to_minimize(x0, fun, X, response, y, to_optimize='rms')`
:   Function to minimize
    
    Parameters
    ----------
    fun : function
        function to minimize
    X : (n_trials, n_betas) array
        design matrix
    response : (n_timepoints, ) array
        vector with value at each time point, for all the trials
    y : (n_trials, ) or (n_timepoints, n_trials, ) array
        raw data
    to_optimize : str
        'rms' or 'r2'
    
    Returns
    -------
    float
        value to minimize