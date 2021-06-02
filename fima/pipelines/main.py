from logging import getLogger
from functools import partial
from multiprocessing import Pool

try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = None

from .continuous import pipeline_continuous
from .dataglove import pipeline_dataglove
from .ols import pipeline_ols, pipeline_ols_all
from .brainregions import pipeline_brainregions
from .spectrum import pipeline_spectrum
from .timepoints import pipeline_timepoints
from .realign import pipeline_realign
from ..utils import be_nice
from ..viz.paper import plot_papers


lg = getLogger(__name__)


def pipeline_fima(parameters, pipeline, subject_only='*', parallel=False):
    """Run pipeline to compute power spectrum on all the participants

    Parameters
    ----------
    parameters : dict
        analysis specific parameters
    pipeline : str
        one of the pipelines to run
    subject_only : str
        compute pipeline only for this participant
    parallel : bool
        where to run it with multiprocessing
    """
    if pipeline != 'paper':
        func = partial(sub_pipeline, parameters=parameters, pipeline=pipeline)
        bids_dir = parameters['paths']['input']
        list_ieeg = bids_dir.rglob(f'sub-{subject_only}_ses-*_acq-*_run-*_ieeg.eeg')
        if parallel:
            with Pool(initializer=be_nice) as p:
                p.map(func, list_ieeg)

        else:
            for ieeg in list_ieeg:
                lg.info(f'Running {ieeg.stem}')
                func(ieeg)

    if pipeline == 'ols':
        pipeline_ols_all(parameters)

    if pipeline == 'paper':
        plot_papers(parameters)


def sub_pipeline(ieeg, parameters, pipeline):
    if setproctitle is not None:
        setproctitle(f'fima {pipeline} {ieeg.stem}')

    if pipeline == 'continuous':
        pipeline_continuous(parameters, ieeg)

    elif pipeline == 'dataglove':
        pipeline_dataglove(parameters, ieeg)

    elif pipeline == 'brainregions':
        pipeline_brainregions(parameters, ieeg)

    elif pipeline == 'timepoints':
        pipeline_timepoints(parameters, ieeg)

    elif pipeline == 'realign':
        pipeline_realign(parameters, ieeg)

    elif pipeline == 'ols':
        pipeline_ols(parameters, ieeg)

    elif pipeline == 'spectrum':
        pipeline_spectrum(parameters, ieeg)

    elif pipeline == 'flex_ext':
        pipeline_flexext_all(
            subject_only=args.subject)

    elif pipeline == 'fingers':
        pipeline_fingers_all(bars=args.bars, corr=args.corr, each=args.each)

    elif pipeline == 'fitting':
        pipeline_fitting_all(
            model_name=args.model,
            response=args.response,
            subject_only=args.subject)
