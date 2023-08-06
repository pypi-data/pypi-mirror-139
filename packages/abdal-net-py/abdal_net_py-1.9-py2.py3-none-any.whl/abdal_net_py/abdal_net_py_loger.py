import os
from datetime import datetime


def error_writer(error_content, file_name):
    """
    log writer
    :param error_content:
    :param file_name:
    :return:
    """
    try:
        get_current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__()
        log_file_name = file_name
        if os.path.exists(log_file_name):
            mode_write = 'a'  # append if already exists
        else:
            mode_write = 'w'  # make a new file if not

        error_log_writer = open(log_file_name, mode_write)
        error_log_writer.write(get_current_date_time + " - " + error_content.__str__() + " \n")
        error_log_writer.close()
    except Exception as e:
        print(e.__str__())
        pass
