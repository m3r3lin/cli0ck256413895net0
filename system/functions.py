import datetime
import os
import random
import uuid


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_avatar_path(instance, filename):
    name, ext = get_filename_ext(filename)
    rand_int_filename = str(random.randint(1, 3910209312))
    random_filename = str(datetime.datetime.now().strftime('%Y%m%d')) + uuid.uuid4().hex[:15] + str(
        random.randint(1, 3910209312))
    final_filename = '{new_filename}{ext}'.format(new_filename=random_filename, ext=ext)
    return "avatar/{final_filename}".format(final_filename=final_filename)


def upload_cart_melli_path(instance, filename):
    name, ext = get_filename_ext(filename)
    rand_int_filename = str(random.randint(1, 3910209312))
    random_filename = str(datetime.datetime.now().strftime('%Y%m%d')) + uuid.uuid4().hex[:15] + str(
        random.randint(1, 3910209312))
    final_filename = '{new_filename}{ext}'.format(new_filename=random_filename, ext=ext)
    return "cart_melli/{final_filename}".format(final_filename=final_filename)
