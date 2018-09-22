#!/usr/bin/env python3

from argparse import ArgumentTypeError
from util.utils import eprint
from arg_parses.audio_parser import ArgParser
from operation.audio import add_audio


def run(settings):
    add_audio(settings)


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
