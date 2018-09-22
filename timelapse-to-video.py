#!/usr/bin/env python3

from argparse import ArgumentTypeError
from util.utils import eprint
from arg_parses.timelapse_parser import ArgParser
from operation.file import process_input_files
from operation.encoding import encode_video


def run(settings):
    process_input_files(settings)
    encode_video(settings)


if __name__ == "__main__":
    settings = None
    try:
        settings = ArgParser.require_args()
        run(settings)
    except ArgumentTypeError as e:
        eprint(e)
    finally:
        if settings:
            settings.destroy()
