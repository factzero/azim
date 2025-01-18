import os
import datetime


def get_file_modify_time(path: str):
    modify_time = os.path.getmtime(path)
    modify_datetime = datetime.datetime.fromtimestamp(modify_time)
    return modify_datetime
