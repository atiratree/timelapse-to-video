import subprocess
import errno
from pprint import pprint

from util.utils import eprint

presets = [
    'ultrafast',
    'superfast',
    'veryfast',
    'faster',
    'fast',
    'medium',
    'slow',
    'slower',
    'veryslow'
]


def encode_video(settings):
    encoder = settings.encoder

    if encoder != 'x264' and encoder != 'x265':
        eprint(f'invalid encoder {encoder}')

    options = build_options(settings)
    print(f'running ffmpeg in {settings.link_dir}')
    pprint(options)

    try:
        subprocess.run(options, cwd=settings.link_dir)
    except OSError as e:
        if e.errno == errno.ENOENT:
            eprint("Please install ffmpeg.")
        else:
            eprint(e)


def build_options(settings):
    inputs = []
    options = []

    if settings.framerate < 15:
        # lower bound on 15 because vlc cannot manage lower fps
        record_rate = 15
    elif settings.framerate > 120:
        # upper bound on 120 for performance reasons
        record_rate = 120
    else:
        record_rate = settings.framerate

    # add video options
    inputs.extend([
        '-pattern_type', 'glob',
        '-i', f'*.{settings.image_extension}',
    ])

    options.extend([
        '-c:v', f'lib{settings.encoder}',
        '-r', str(record_rate),
        '-framerate', str(settings.framerate),
        '-pix_fmt', 'yuv420p',
        '-preset', presets[settings.encoding_quality],
    ])

    # add audio options
    if settings.audio_file:
        if settings.audio_start > 0:
            inputs.extend([
                '-ss', str(settings.audio_start)
            ])
        inputs.extend([
            '-i', settings.audio_file,
        ])

        options.extend([
            '-c:a', 'aac',
            '-b:a', '320k',
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
