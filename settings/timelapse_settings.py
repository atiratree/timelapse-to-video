from astral import Location
import tempfile
import shutil


class DefaultSettings:
    skip_over_exposed_images = False
    skip_dark_images = False
    skip_images_without_natural_light = False

    output_filename = None
    input_dir = None

    audio_file = None
    audio_start = 0.0

    image_extension = 'jpg'
    output_extension = 'mkv'
    encoder = 'x264'
    encoding_quality = 5

    # encoder = 'x265'
    # encoding_quality = 4

    framerate = 30
    threads = 8

    # coordinates for computing the position of the sun
    latitude = '49.1951'
    longitude = '16.6068'
    elevation = '237'  # meters
    timezone = 'Europe/Prague'
    dawn_dusk_offset = '15'  # minutes

    white_overexposed_threshold_percentage = 50  # not exposed through CLI


class Settings:
    def __init__(self,
                 skip_over_exposed_images=DefaultSettings.skip_over_exposed_images,
                 skip_dark_images=DefaultSettings.skip_dark_images,
                 skip_images_without_natural_light=DefaultSettings.skip_images_without_natural_light,

                 output_filename=DefaultSettings.output_filename,
                 input_dir=DefaultSettings.input_dir,

                 audio_file=DefaultSettings.audio_file,
                 audio_start=DefaultSettings.audio_start,

                 image_extension=DefaultSettings.image_extension,
                 output_extension=DefaultSettings.output_extension,
                 encoder=DefaultSettings.encoder,
                 encoding_quality=DefaultSettings.encoding_quality,

                 framerate=DefaultSettings.framerate,
                 threads=DefaultSettings.threads,

                 latitude=DefaultSettings.latitude,
                 longitude=DefaultSettings.longitude,
                 elevation=DefaultSettings.elevation,
                 timezone=DefaultSettings.timezone,
                 dawn_dusk_offset=DefaultSettings.dawn_dusk_offset,
                 white_overexposed_threshold_percentage=DefaultSettings.white_overexposed_threshold_percentage,
                 ):
        self.skip_over_exposed_images = skip_over_exposed_images
        self.skip_dark_images = skip_dark_images
        self.skip_images_without_natural_light = skip_images_without_natural_light

        self.output_filename = output_filename
        self.input_dir = input_dir

        self.audio_file = audio_file
        self.audio_start = audio_start

        self.image_extension = image_extension
        self.output_extension = output_extension
        self.encoder = encoder
        self.encoding_quality = encoding_quality

        self.framerate = framerate
        self.threads = threads

        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.timezone = timezone
        self.timezone = timezone

        l = Location(())
        l.longitude = self.longitude
        l.latitude = self.latitude
        l.elevation = self.elevation
        l.timezone = self.timezone
        self.location = l

        self.dawn_dusk_offset = dawn_dusk_offset

        self.white_overexposed_threshold_percentage = white_overexposed_threshold_percentage

        self.link_dir = tempfile.mkdtemp()

    def destroy(self):
        shutil.rmtree(self.link_dir)

    def get_output_filename_with_extension(self):
        return f'{self.output_filename}.{self.output_extension}'
