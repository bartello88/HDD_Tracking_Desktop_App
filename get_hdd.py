import wmi
import psutil
import os
import getpass
import datetime
import pythoncom
import win32api
import re


def get_user_name():
    try:
        driver_name = getpass.getuser()
        return driver_name
    except:
        return 'no_hdd'


def get_hdd_serial_number():
    try:
        pythoncom.CoInitialize()
        hdd = wmi.WMI()
        for s_number in hdd.Win32_PhysicalMedia():
            serial_number = s_number.SerialNumber
            return serial_number
    except:
        return ''


def get_MDI_files_name(directory):
    try:
        sessions_list = []
        for r, d, f in os.walk(directory):
            for file in f:
                pattern =re.compile( r'._\d{4}_\d{2}_\d{2}__\d{2}_\d{2}_\d{2}')
                if ".mdi" in file:
                    if pattern.search(file):
                        sessions_list.append(file.split('.')[0])
                        car_name = file.split('_')[0]
        number_of_sesions = len(sessions_list)
        return number_of_sesions, sessions_list, car_name
    except:
        return 0, [], 'no hdd'


def get_hdd_info():
    try:
        hdd = psutil.disk_usage('/')
        hdd_total = round(hdd.total / (2 ** 30), 1)
        hdd_used = round(hdd.used / (2 ** 30), 1)
        return hdd_total, hdd_used
    except:
        return 0, 0

def find_disks():

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    disks = [x[0] for x in drives if x != 'Z:\\' ]
    return disks[len(disks)-1]


def get_date():
    try:
        date = datetime.datetime.now()
        date = date.strftime("%b %d %Y %H:%M:%S")
        return date
    except:
        'no data'


def get_sessions_data_range(session_list):
    try:
        session_list.sort()
        start_date = session_list[0].split('_')[1:4]
        start_date = '-'.join(start_date)
        end_date = session_list[len(session_list) - 1].split('_')[1:4]
        end_date = '_'.join(end_date)
        return start_date, end_date
    except:
        return 'no data', 'no data'



