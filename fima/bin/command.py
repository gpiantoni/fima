#!/usr/bin/env python3

from ..pipelines.power_spectrum import pipeline_timefreq_all


def main():
    for ev in ('flexion', 'extension', 'open', 'close', 'cues'):
        pipeline_timefreq_all(ev)


if __name__ == '__main__':
    main()
