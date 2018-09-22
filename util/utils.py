import os
import sys
import re


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def realpath(path):
    return os.path.realpath(path)


def is_dir(directory):
    return os.path.isdir(directory) and os.path.exists(directory)


def is_file(file):
    return os.path.isfile(file) and os.path.exists(file)


def input_exist(directory, extension):
    for file in os.listdir(directory):
        if file.endswith(extension):
            return True

    return False


def filename_and_extension(file):
    return os.path.splitext(file)


def file_in_dir(directory, file):
    return os.path.join(directory, file)


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]


def natural_sorted(l):
    return sorted(l, key=natural_sort_key)


def hex_code(rgb):
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    return '#%02x%02x%02x' % (r, g, b)


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()
