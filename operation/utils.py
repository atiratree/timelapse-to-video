import datetime

import pytz
import re
from PIL import Image

from util.utils import hex_code, filename_and_extension

_FILENAME_REGEX = re.compile(r'([^\d]*)(\d+)$')


def is_file_processable(file, settings):
    img = Image.open(file)
    exif_data = img._getexif()
    str_image_date = exif_data[36867]
    image_date = datetime.datetime.strptime(str_image_date, "%Y:%m:%d %H:%M:%S")
    image_date = pytz.timezone(settings.timezone).localize(image_date)

    sun = settings.location.sun(date=datetime.date(image_date.year, image_date.month, image_date.day))

    offset = datetime.timedelta(minutes=int(settings.dawn_dusk_offset))

    if settings.skip_images_without_natural_light and \
            (image_date < sun['dawn'] + offset or image_date > sun['dusk'] - offset):
        return False

    max_color_count = 0
    max_color_name = ''

    if settings.skip_dark_images or settings.skip_over_exposed_images:
        w, h = img.size
        for idx, c in enumerate(img.getcolors(w * h)):
            if c[0] > max_color_count:
                max_color_count = c[0]
                max_color_name = hex_code(c[1])

        if settings.skip_dark_images and max_color_name == "#000000":
            return False

        if settings.skip_over_exposed_images and max_color_name == "#ffffff" and \
                max_color_count > w * h / 100 * settings.white_overexposed_threshold_percentage:
            return False

    return True


def get_file_name_and_id(file):
    filename, extension = filename_and_extension(file)
    name = None
    number = None

    reg_res = _FILENAME_REGEX.match(filename)
    if reg_res:
        name = reg_res.group(1).strip()
        number = reg_res.group(2).strip()

    return name, number


def get_new_filename(file, number_of_digits, override_id=None):
    _, extension = filename_and_extension(file)
    name, number = get_file_name_and_id(file)

    if not name:
        name = ''

    if override_id:
        number = str(override_id)
    elif not number:
            return None

    sufficient_number_of_digits = len(number) >= number_of_digits
    return file if sufficient_number_of_digits else f'{name}{number.zfill(number_of_digits)}{extension}'
