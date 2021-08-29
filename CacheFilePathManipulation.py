import os
import errno

from constants import CACHE_FILE_PATH


def get_cache_path(file_name, user_id=None):
    __make_sure_path_exists(CACHE_FILE_PATH)

    path, extension = os.path.splitext(file_name)

    user_id = "" if user_id is None else user_id

    combined_path = f"{CACHE_FILE_PATH}{path}{user_id}{extension}"  # Combine paths

    return combined_path


def remove_file_path(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        raise RuntimeError(f"File path \"{path}\" does not exist!")


def clear_cache():
    remove_file_path(CACHE_FILE_PATH)


def __make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
