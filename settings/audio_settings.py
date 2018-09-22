class DefaultSettings:
    output_filename = None
    video_file = None

    audio_file = None
    audio_start = 0.0

    output_extension = 'mkv'

    threads = 8


class Settings:
    def __init__(self,
                 output_filename=DefaultSettings.output_filename,
                 video_file=DefaultSettings.video_file,

                 audio_file=DefaultSettings.audio_file,
                 audio_start=DefaultSettings.audio_start,

                 output_extension=DefaultSettings.output_extension,
                 threads=DefaultSettings.threads,
                 ):
        self.output_filename = output_filename
        self.video_file = video_file

        self.audio_file = audio_file
        self.audio_start = audio_start

        self.output_extension = output_extension
        self.threads = threads

    def destroy(self):
        pass

    def get_output_filename_with_extension(self):
        return f'{self.output_filename}.{self.output_extension}'
