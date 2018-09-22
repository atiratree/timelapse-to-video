import argparse
from util.utils import realpath, is_dir, is_file, input_exist, filename_and_extension


def proccess_dir(directory, extension):
    directory = realpath(directory)

    if not is_dir(directory):
        raise argparse.ArgumentTypeError(f'{directory} is not an existing directory!')

    if not input_exist(directory, extension):
        raise argparse.ArgumentTypeError(f'No files with {extension} extension exits in {directory}')

    return directory


def proccess_file(file):
    try:
        f = realpath(file)
    except Exception:
        return None

    if not is_file(f):
        raise argparse.ArgumentTypeError(f'{file} is not an existing file!')

    return f


def proccess_filename(filename, default_settings):
    filename, extension = filename_and_extension(filename)

    if extension and extension != default_settings.output_extension:
        print(f'ignoring extension {extension}! Using {default_settings.output_extension}')

    return realpath(filename)


def resolve_encoding(encoding_quality, default_settings):
    if encoding_quality is None:
        return default_settings.encoder, default_settings.encoding_quality
    else:
        return 'x265', encoding_quality


def positive_int(v):
    def fail():
        raise argparse.ArgumentTypeError('Positive Integer value expected.')

    try:
        result = int(v)
        if result < 0:
            fail()
        return result
    except Exception:
        fail()


def positive_float(v):
    def fail():
        raise argparse.ArgumentTypeError('Positive Float value expected.')

    try:
        result = float(v)
        if result < 0:
            fail()
        return result
    except Exception:
        fail()


def x265_preset_int(v):
    def fail():
        raise argparse.ArgumentTypeError('Integer 0-8 expected.')

    try:
        result = int(v)
        if result < 0 or result > 8:
            fail()
        return result
    except Exception:
        fail()
