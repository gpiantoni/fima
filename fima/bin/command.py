#!/usr/bin/env python3

from argparse import ArgumentParser, RawTextHelpFormatter
from logging import getLogger, INFO, DEBUG, StreamHandler, Formatter
from json import load, dump, JSONEncoder
from datetime import datetime
from pathlib import Path

from ..pipelines import pipeline_fima

lg = getLogger('fima')
lg.setLevel(DEBUG)


def main():
    """Command line function to compute the analyses"""
    parser = ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description='Analysis finger mapping')

    parser.add_argument(
        'parameters',
        help='point to parameters.json')
    parser.add_argument(
        '-p', '--parallel',
        action='store_true',
        help='Run analysis for all the subjects in parallel')
    parser.add_argument(
        '-s', '--subject', default='*',
        help='Run analysis only on one subject')
    parser.add_argument(
        '-l', '--log',
        default='info',
        help='Logging level: info (default), debug',
        )

    list_pipelines = parser.add_subparsers(title='Pipelines', help='')

    action = list_pipelines.add_parser(
        'brainregions',
        help='Get brain regions for all the electrodes',
        )
    action.set_defaults(function='brainregions')

    action = list_pipelines.add_parser(
        'dataglove',
        help='Plot the time-course of the dataglove',
        )
    action.set_defaults(function='dataglove')

    action = list_pipelines.add_parser(
        'continuous',
        help='Plot the time-course continuously in the high-frequency range',
        )
    action.set_defaults(function='continuous')

    action = list_pipelines.add_parser(
        'spectrum',
        help='Compute Time-Frequency Analysis',
        )
    action.set_defaults(function='spectrum')

    action = list_pipelines.add_parser(
        'timepoints',
        help='Find important timepoints (peak and above threshold)',
        )
    action.set_defaults(function='timepoints')

    action = list_pipelines.add_parser(
        'ols',
        help='Fit Ordinary Least Squares on the continuous data',
        )
    action.set_defaults(function='ols')
    action.add_argument(
        '--skip_ols', action='store_true',
        help='Skip OLS on the data (very time consuming)')
    action.add_argument(
        '--skip_prf', action='store_true',
        help='Skip PRF on parameters (time consuming). Use both options to jump to summary directly')

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

    action = list_pipelines.add_parser(
        'fitting',
        help='Fit a PRF model to the data',
        )
    action.set_defaults(function='fitting')

    args = parser.parse_args()

    parameters = read_parameters(args.parameters)

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

    if args.function == 'ols':
        if 'ols' not in parameters:
            parameters['ols'] = {}
        parameters['ols']['skip_ols'] = args.skip_ols
        parameters['ols']['skip_prf'] = args.skip_prf

    parameters['paths']['output'].mkdir(exist_ok=True, parents=True)
    parameters['timestamp'] = datetime.now().isoformat()
    parameters_json = parameters['paths']['output'] / 'parameters.json'
    with parameters_json.open('w') as f:
        dump(parameters, f, indent=2, cls=JSONEncoder_path)

    pipeline_fima(
        parameters,
        args.function,
        subject_only=args.subject,
        parallel=args.parallel)


def read_parameters(parameters_path):
    parameters_path = Path(parameters_path).resolve()
    with parameters_path.open() as f:
        parameters = load(f)
    for k in parameters['paths']:
        parameters['paths'][k] = Path(parameters['paths'][k]).resolve()

    return parameters


class JSONEncoder_path(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)


if __name__ == '__main__':
    main()
