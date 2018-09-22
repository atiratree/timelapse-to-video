import subprocess
import errno
from pprint import pprint

from util.utils import eprint


def add_audio(settings):
    options = _build_options(settings)
    print('running ffmpeg')
    pprint(options)

    try:
        subprocess.run(options)
    except OSError as e:
        if e.errno == errno.ENOENT:
            eprint("Please install ffmpeg.")
        else:
            eprint(e)


def _build_options(settings):
    inputs = []
    options = []

    # add video options
    inputs.extend([
        '-i', settings.video_file,
    ])

    options.extend([
        '-c:v', 'copy',
        '-map', '0:v'
    ])

    if settings.audio_start > 0:
        inputs.extend([
            '-ss', str(settings.audio_start)
        ])
    inputs.extend([
        '-i', settings.audio_file,
    ])

    options.extend([
        '-c:a', 'aac',
        '-map', '1:a',
        '-b:a', '320k',
        '-filter_complex', ' [1:0] apad ',  # pad with silence when audio input is too short
        '-shortest'
    ])

    result = [
        'ffmpeg',
        '-loglevel', 'level+fatal',
        '-stats'
    ]
    result.extend(inputs)
    result.extend(options)
    result.append(settings.get_output_filename_with_extension())

    return result
