#!/usr/bin/env python3

from argparse import ArgumentParser, RawTextHelpFormatter
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter

from ..pipelines import pipeline_fima
from ..parameters import P

lg = getLogger('fima')
lg.setLevel(DEBUG)


def main():
    """Command line function to compute the analyzses"""
    parser = ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description='Analysis finger mapping')

    parser.add_argument(
        '-p', '--parallel',
        action='store_true',
        help='Run analysis for all the subjects in parallel')
    parser.add_argument(
        '-s', '--subject', default=None,
        help='Run analysis only on one subject')
    parser.add_argument(
        '-l', '--log',
        default='info',
        help='Logging level: info (default), debug',
        )

    list_pipelines = parser.add_subparsers(title='Pipelines', help='')

    action = list_pipelines.add_parser(
        'continuous',
        help='Plot the time-course continuously in the high-frequency range',
        )
    action.set_defaults(function='continuous')
    action.add_argument(
        '--baseline', action='store_true',
        help='Baseline correction with ' + P['spectrum']['baseline']['type'])

    action = list_pipelines.add_parser(
        'dataglove',
        help='Plot the time-course of the dataglove',
        )
    action.set_defaults(function='dataglove')

    action = list_pipelines.add_parser(
        'ols',
        help='Fit Ordinary Least Squares on the continuous data',
        )
    action.set_defaults(function='ols')

    action = list_pipelines.add_parser(
        'spectrum',
        help='Compute Time-Frequency Analysis',
        )
    action.set_defaults(function='spectrum')

    action = list_pipelines.add_parser(
        'flex_ext',
        help='',
        )
    action.set_defaults(function='flex_ext')

    action = list_pipelines.add_parser(
        'fingers',
        help='Analyze each finger individually',
        )
    action.set_defaults(function='fingers')
    action.add_argument(
        '--bars', action='store_true',
        help='Plot bars with t-statistics')
    action.add_argument(
        '--corr', action='store_true',
        help='Correlation across fingers')
    action.add_argument(
        '--each', action='store_true',
        help='Correlation across fingers based on each finger')

    action = list_pipelines.add_parser(
        'fitting',
        help='Fit a PRF model to the data',
        )
    action.set_defaults(function='fitting')
    action.add_argument(
        '--model', default='linear_separate_gaussians_per_finger',
        help='Specify which model to run')
    action.add_argument(
        '--response', default=None,
        help='If specify, use all the datapoints (options: "mean")')

    args = parser.parse_args()

    if args.log[:1].lower() == 'i':
        LEVEL = INFO
        FORMAT = '{asctime:<10}{message}'

    elif args.log[:1].lower() == 'd':
        LEVEL = DEBUG
        FORMAT = '{asctime:<10}{levelname:<8}{filename:<20} (l.{lineno: 4d}): {message}'

    lg.setLevel(LEVEL)
    DATE_FORMAT = '%H:%M:%S'
    handler = StreamHandler()
    handler.setLevel(LEVEL)
    formatter = Formatter(fmt=FORMAT, datefmt=DATE_FORMAT, style='{')
    handler.setFormatter(formatter)
    lg.addHandler(handler)

    kwargs = {}
    if args.function == 'continuous':
        kwargs['baseline'] = args.baseline

    pipeline_fima(
        args.function,
        subject_only=args.subject,
        parallel=args.parallel,
        kwargs=kwargs)


if __name__ == '__main__':
    main()
