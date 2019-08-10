import datetime
import os
import random
import uuid
from unidecode import unidecode
from Ads_Project.functions import jalali_to_gregorian
from django.shortcuts import redirect


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

def change_date_to_english(value, mode=1):
    if mode == 3:
        y, m, d = value
        pdate = jalali_to_gregorian(int(y), int(m), int(d))
        date_time = datetime.datetime(pdate[0], pdate[1], pdate[2])
        return date_time
    if mode == 2:
        y, m, d = unidecode(value).split('/')
        pdate = jalali_to_gregorian(int(y), int(m), int(d))
        date_time = datetime.datetime(pdate[0], pdate[1], pdate[2])
        return date_time
    value = unidecode(value)
    stime, date = value.split(' ')
    stime = unidecode(stime)
    year, month, day = date.split('/')
    date = jalali_to_gregorian(int(year), int(month), int(day))
    string_date = "{y} {m} {d} ".format(y=date[0], m=date[1], d=date[2])
    string_date_time = string_date + stime
    date_time = datetime.datetime.strptime(string_date_time, "%Y %m %d %H:%M:%S")
    return date_time


def check_role_user(*roles):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                user_roles = request.user.roles.all()
            except:
                return redirect('/users/logout/')

            for user_role in user_roles:
                for role in roles:
                    if role == str(user_role.name):
                        return func(request, *args, **kwargs)
            return redirect('/')

        return wrapper
    return decorator