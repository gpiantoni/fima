#!/usr/bin/env python3

from ..pipelines.power_spectrum import pipeline_timefreq_all
from ..pipelines.fingers import pipeline_fingers_all
from ..pipelines.fitting import pipeline_fitting_all


def main():
    pipeline_fitting_all()


if __name__ == '__main__':
    main()
