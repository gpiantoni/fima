from logging import getLogger
from functools import partial
from multiprocessing import Pool
from os import nice

from .continuous import pipeline_continuous
from ..parameters import SUBJECTS


lg = getLogger(__name__)


def pipeline_fima(pipeline=None, subject_only=None, parallel=False, kwargs=None):
    """Run pipeline to compute power spectrum on all the participants

    Parameters
    ----------
    pipeline : str
        one of the pipelines to run
    event_type : str
        event type used to identify the trials (one of 'cues', 'open', 'close',
        'movements', 'extension', 'flexion')
    subject_only : str
        compute pipeline only for this participant
    """
    func = partial(sub_pipeline, pipeline=pipeline, kwargs=kwargs)
    if parallel:
        args = gen_subject_run()
        with Pool(initializer=be_nice) as p:
            p.starmap(func, args)

    else:
        for subject, runs in SUBJECTS.items():
            if subject_only is not None and subject != subject_only:
                continue

            for run in runs:
                lg.info(f'{subject} / {run}')
                func(subject, run)


def sub_pipeline(subject, run, pipeline, kwargs):

    if pipeline == 'continuous':
        pipeline_continuous(
            subject,
            run,
            baseline=kwargs['baseline'],
            )

    elif pipeline == 'spectrum':
        pipeline_spectrum_all(
            subject_only=args.subject)

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


def gen_subject_run():
    val = []
    for subj, runs in SUBJECTS.items():
        for run in runs:
            val.append((subj, run))

    return val


def be_nice():
    nice(10)

