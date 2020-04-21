#!/usr/bin/env python3

from ..pipelines.power_spectrum import pipeline_timefreq_all
from ..pipelines.fingers import pipeline_fingers_all


def main():
    pipeline_fingers_all()


if __name__ == '__main__':
    main()
