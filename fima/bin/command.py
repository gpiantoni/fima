#!/usr/bin/env python3

from argparse import ArgumentParser
from ..pipelines import (
    pipeline_spectrum_all,
    pipeline_fitting_all,
    )


def main():
    parser = ArgumentParser(description='Analysis finger mapping')

    list_pipelines = parser.add_subparsers(title='Pipelines', help='')

    action = list_pipelines.add_parser(
        'spectrum',
        help='Compute Time-Frequency Analysis',
        )
    action.set_defaults(function='spectrum')
    action.add_argument(
        '-S', '--subject', default=None,
        help='Run analysis only on one subject')

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

    if args.function == 'spectrum':
        pipeline_spectrum_all(
            subject_only=args.subject)

    elif args.function == 'fitting':
        pipeline_fitting_all(
            model_name=args.model,
            response=args.response,
            subject_only=args.subject)


if __name__ == '__main__':
    main()
