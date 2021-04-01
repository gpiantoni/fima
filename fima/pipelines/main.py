from logging import getLogger
from functools import partial
from multiprocessing import Pool

from .continuous import pipeline_continuous
from .dataglove import pipeline_dataglove
from .ols import pipeline_ols, pipeline_ols_all
from .brainregions import pipeline_brainregions
from .spectrum import pipeline_spectrum
from ..utils import be_nice


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
    func = partial(sub_pipeline, parameters=parameters, pipeline=pipeline)
    list_ieeg = bids_dir.rglob(f'sub-{subject_only}_ses-*_acq-*_run-*_ieeg.eeg')
    if parallel:
        with Pool(initializer=be_nice) as p:
            p.starmap(func, list_ieeg)

    else:
        for ieeg in list_ieeg:
            lg.info(f'Running {ieeg.stem}')
            func(ieeg)

    if pipeline == 'ols':
        pipeline_ols_all()


def sub_pipeline(ieeg, parameters, pipeline):

    if pipeline == 'continuous':
        pipeline_continuous(parameters, ieeg)

    elif pipeline == 'dataglove':
        pipeline_dataglove(parameters, ieeg)

    elif pipeline == 'brainregions':
        pipeline_brainregions(parameters, ieeg)

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
