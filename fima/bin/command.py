#!/usr/bin/env python3

from argparse import ArgumentParser
from ..pipelines import (
    pipeline_continuous_all,
    pipeline_spectrum_all,
    pipeline_fitting_all,
    pipeline_fingers_all,
    pipeline_flexext_all,
    )

from ..parameters import P


def main():
    """Command line function to compute the analyzses"""
    parser = ArgumentParser(description='Analysis finger mapping')

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
        'spectrum',
        help='Compute Time-Frequency Analysis',
        )
    action.set_defaults(function='spectrum')
    action.add_argument(
        '-S', '--subject', default=None,
        help='Run analysis only on one subject')

    action = list_pipelines.add_parser(
        'flex_ext',
        help='',
        )
    action.set_defaults(function='flex_ext')
    action.add_argument(
        '-S', '--subject', default=None,
        help='Run analysis only on one subject')

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
    action.add_argument(
        '-S', '--subject', default=None,
        help='Run analysis only on one subject')

    args = parser.parse_args()
    print(args)

    if args.function == 'continuous':
        pipeline_continuous_all(
            baseline=args.baseline,
            )

    elif args.function == 'spectrum':
        pipeline_spectrum_all(
            subject_only=args.subject)

    elif args.function == 'flex_ext':
        pipeline_flexext_all(
            subject_only=args.subject)

    elif args.function == 'fingers':
        pipeline_fingers_all(bars=args.bars, corr=args.corr, each=args.each)

    elif args.function == 'fitting':
        pipeline_fitting_all(
            model_name=args.model,
            response=args.response,
            subject_only=args.subject)


if __name__ == '__main__':
    main()
