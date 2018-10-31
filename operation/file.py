import os
import multiprocessing

from operation.utils import is_file_processable, get_new_filename, get_file_name_and_id

from util.utils import eprint, file_in_dir, natural_sorted, print_progress_bar

process_config = None


def init(args):
    global process_config
    process_config = args


class ProcessConfig:
    def __init__(self, files_count, settings):
        self.files_count = files_count
        self.settings = settings
        self.files_processed = multiprocessing.Value('i', 0)

    def next_file(self):
        with self.files_processed.get_lock():
            self.files_processed.value += 1
            print_progress_bar(self.files_processed.value, self.files_count, prefix='Processing input files:',
                               suffix='Complete', length=50)


def repeat_last_frame(settings):
    linked_files = natural_sorted(os.listdir(settings.link_dir))
    if len(linked_files) == 0:
        return

    last_file = linked_files[-1]
    last_file_full_path = file_in_dir(settings.link_dir, last_file)
    _, last_file_id = get_file_name_and_id(last_file)

    number_of_digits = len(last_file_id)
    last_file_id = int(last_file_id)

    for i in range(1, int(settings.framerate * settings.last_frame_freeze) + 1):
        new_filename = get_new_filename(last_file, number_of_digits, override_id=last_file_id + i)  # 7 just to be sure
        linked_file = file_in_dir(settings.link_dir, new_filename)
        os.symlink(last_file_full_path, linked_file)


def process_input_files(settings):
    # sorting doesn't do much, but there is a bigger chance log will be consecutive
    files = natural_sorted(os.listdir(settings.input_dir))
    files_count = len(files)
    print_progress_bar(0, files_count, prefix='Processing input files:', suffix='Complete', length=50)

    pool = multiprocessing.Pool(settings.threads, initializer=init, initargs=(ProcessConfig(files_count, settings),))

    pool.map(_process_input_file, files)


def _process_input_file(file):
    settings = process_config.settings

    if file.endswith(settings.image_extension):
        # filename is used for ffmpeg glob option
        new_filename = get_new_filename(file, len(str(process_config.files_count)) + 7)  # 7 just to be sure

        if not new_filename:
            eprint(f'skipping {file}: invalid filename! Not numbered in format "abc123.jpg"')
            return

        file_full_path = file_in_dir(settings.input_dir, file)
        if is_file_processable(file_full_path, settings):
            linked_file = file_in_dir(settings.link_dir, new_filename)
            os.symlink(file_full_path, linked_file)

    process_config.next_file()
