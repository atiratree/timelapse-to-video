import argparse
from settings.audio_settings import Settings, DefaultSettings
from arg_parses.utils import positive_float, positive_int, proccess_file, proccess_filename


class ArgParser:
    @staticmethod
    def require_args():
        parser = argparse.ArgumentParser(usage='add-audio-to-video.py [OPTIONS] VIDEO_INPUT AUDIO_INPUT OUTPUT\n'
                                               '\n'
                                               ' - adds audio from AUDIO_INPUT to VIDEO_INPUT')
        parser.add_argument('VIDEO_INPUT', help=f'video file')
        parser.add_argument('AUDIO_INPUT', help=f'audio file')
        parser.add_argument('OUTPUT', help=f'output file which will be saved in mkv format')

        parser.add_argument('-s', '--audio_start', type=positive_float, nargs='?',
                            dest='audio_start',
                            required=False, const=True, default=DefaultSettings.audio_start,
                            help=f'where should the audio start (default {DefaultSettings.audio_start})')

        parser.add_argument('-j', '--jobs', type=positive_int, nargs='?',
                            dest='threads',
                            required=False, const=True, default=DefaultSettings.threads,
                            help=f'default {DefaultSettings.threads}.')

        args = parser.parse_args()

        return ArgParser._as_settings(args)

    @staticmethod
    def _as_settings(args):
        output_file = proccess_filename(args.OUTPUT, DefaultSettings)

        video_file = proccess_file(args.VIDEO_INPUT)
        audio_file = proccess_file(args.AUDIO_INPUT)

        return Settings(
            video_file=video_file,
            output_filename=output_file,
            audio_file=audio_file,
            audio_start=args.audio_start,
            threads=args.threads,
        )
