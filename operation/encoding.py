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
        return

    # cap on 15 because vlc cannot manage lower fps
    if settings.framerate < 15:
        record_rate = 15
    else:
        record_rate = settings.framerate

    try:
        args = [
            'ffmpeg',
            '-framerate', str(settings.framerate),
            '-pattern_type', 'glob',
            '-i', f'*.{settings.image_extension}',
            '-c:v', f'lib{encoder}',
            '-r', str(record_rate),
            '-pix_fmt', 'yuv420p',
            '-preset', presets[settings.encoding_quality],
            settings.get_output_filename_with_extension()
        ]
        print(f'running ffmpeg in {settings.link_dir}')
        pprint(args)
        subprocess.run(args, cwd=settings.link_dir)
    except OSError as e:
        if e.errno == errno.ENOENT:
            eprint("Please install ffmpeg.")
        else:
            eprint(e)
