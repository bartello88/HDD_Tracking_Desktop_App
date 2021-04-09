import wmi
import psutil
import os
import getpass
import datetime
import pythoncom
import win32api
import re
import logging
from hdd import Hdd
def create_hdd_object():
    try:
        disk = find_disks()
        driver = get_user_name()
        serial_number = get_hdd_serial_number()
        number_of_sessions, session_list, car_name = get_MDI_files_name(
            disk + r':')  # test path - to be changed to select folder on cilent's side

        hdd_total, hdd_used = get_hdd_info()
        date = get_date()
        start_date, end_date = get_sessions_data_range(session_list)

        hdd = Hdd(serial_number, car_name, session_list, number_of_sessions, driver, hdd_total, hdd_used, date,
                  start_date,
                  end_date)
        return hdd
    except:
        no_hdd = Hdd(serial_number='no hdd', car_name='n0 hdd', session_list=[], number_of_sessions=0, driver='no hdd',
                     hdd_total=0, hdd_used=0, date=0,
                     start_date='no hdd',
                     end_date='no hdd')
        return no_hdd

def checking_necessary_files():
    logging.info(f"File DiskInfo.txt exists: {os.path.isfile('DiskInfo.txt')}")
    logging.info(f"File DiskInfo64.rxr exists: {os.path.isfile('DiskInfo64.exe')}")
    logging.info(f"File config.yaml exists: {os.path.isfile('config.yaml')}")
    logging.info(f"File lastship.txt exists: {os.path.isfile('lastship.txt')}")
    logging.info(f"File log.log exists: {os.path.isfile('log.log')}")
    logging.info(f"File DiskInfoParase.json exists: {os.path.isfile('DiskInfoParser.json')}")
    logging.info(f"Folder CdiResources exists: {os.path.isdir('CdiResource')}\n")
    with open('DiskInfo.txt') as disk_info_file:
        logging.info(f'Reading DiskInfo.txt...\n{disk_info_file.read()}')
    with open('DiskInfoParser.json') as disk_info_parser_json_file:
        logging.info(f'Reading DiskInfoParser.json...\n{disk_info_parser_json_file.read()}')

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



