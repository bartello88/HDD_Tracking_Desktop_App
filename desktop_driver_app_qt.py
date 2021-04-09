from pprint import pprint
from colorama import *
from PyQt5.QtWidgets import QWidget, QListWidget, QLineEdit, QGridLayout, QTextEdit, QLabel, QApplication, QPushButton, \
    QHBoxLayout, QGroupBox, QMessageBox, QCheckBox, QPlainTextEdit, QComboBox
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5 import QtGui, QtCore
from get_hdd import get_user_name, get_hdd_serial_number, get_MDI_files_name, get_hdd_info, get_date, \
    get_sessions_data_range, find_disks
from hdd import Hdd
from send_data import send_to_heimdall
from code_generator import code_generator, get_last_file_modified_data
from datetime import datetime
from save_ship_to_file import save_last_ship_to_file
from parse_crystaldiskinfo_txt import *
from check_vpn_connection import check_vpn
from check_health_status import heatlh_status
import logging
import yaml
import time
import os


# -----------------------------------------------------------------------------------------------------
def checking_files():
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


# colorama
init(autoreset=True)

# loggin config
logging.basicConfig(filename='log.log', level=logging.DEBUG)

current_date_for_gc = datetime.now().strftime("%Y-%m-%d")
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

logging.info(f'//////////////////////////////////////////////////////////////////\nApp starts {current_date}\n')
checking_files()
logging.info("Opening yaml file")



with open('config.yaml') as yaml_file:
    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    version = data['version']

logging.info(f"{current_date}\nFile has been opened properly\n")

print(Fore.GREEN + "Hello driver")
print(Fore.BLUE + f"Vrsion:{version}")

my_hdd = create_hdd_object()
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class DriverWindow(QWidget):
    def __init__(self):
        super().__init__()

        # driver name
        self.driver_name_label = QLabel('Driver name')
        self.driver_name_text = QLineEdit()
        self.driver_name_text.setPlaceholderText('enter your name')

        # car name
        self.car_name_label = QLabel('Car name')
        self.car_name_text = QLineEdit()
        self.car_name_text.setText(my_hdd.car_name)
        self.car_name_text.setReadOnly(True)

        # HDD id
        self.hdd_id_label = QLabel('HDD Serial Number')
        self.hdd_id_text = QLineEdit()
        self.hdd_id_text.setText(my_hdd.hdd_serial_number)
        self.hdd_id_text.setReadOnly(True)

        # number of sessions
        self.count_sessions_label = QLabel('Number of sessions')
        self.count_sessions_text = QLineEdit()
        self.count_sessions_text.setText(str(my_hdd.number_of_session))
        self.count_sessions_text.setReadOnly(True)

        # sessions range
        ##start_date
        self.start_date_label = QLabel('First & Last Session')
        self.start_date_text = QLineEdit()
        self.start_date_text.setText(my_hdd.start_date)
        self.start_date_text.setReadOnly(True)

        ##end date
        self.end_date_label = QLabel('Last Session')
        self.end_date_text = QLineEdit()
        self.end_date_text.setText(my_hdd.end_date)
        self.end_date_text.setReadOnly(True)

        # list of sessions
        self.sessions_list_label = QLabel('sessions')
        self.sessions_list_text = QListWidget()
        self.sessions_list_text.addItems([x for x in my_hdd.session_list])
        # sessions_list_text.setReadOnly(True)

        # AWB number
        self.airwaybill_label = QLabel('AWB name')
        self.airwaybill_text = QLineEdit()
        self.airwaybill_text.setPlaceholderText('enter AWB number if you have it')

        # code
        self.generated_code_label = QLabel('Generated code')
        self.generated_code_text = QLineEdit()
        self.generated_code = code_generator(my_hdd.car_name, current_date_for_gc.replace('_', '-'), 3)
        self.generated_code_text.setText(self.generated_code)
        self.generated_code_text.setReadOnly(True)

        # vpn
        self.vpn_label = QLabel('VPN')
        self.vpn_connection_label = QLabel('checking...')

        # hdd status health

        self.hdd_health_status_label = QLabel('HDD Health status')
        self.check_hdd_health_status_label = QLabel('Add hdd to check')


        # hdds

        # 1
        self.hdd_1_label = QLabel()
        self.hdd_1_hddid_label = QLabel()
        self.hdd_1_start_date_label = QLabel()
        self.hdd_1_end_date_label = QLabel()
        self.hdd_1_num_sessions_label = QLabel()
        self.hdd_1_icon_label = QLabel()

        # 2
        self.hdd_2_label = QLabel()
        self.hdd_2_hddid_label = QLabel()
        self.hdd_2_start_date_label = QLabel()
        self.hdd_2_end_date_label = QLabel()
        self.hdd_2_num_sessions_label = QLabel()
        self.hdd_2_icon_label = QLabel()

        # 3
        self.hdd_3_label = QLabel()
        self.hdd_3_hddid_label = QLabel()
        self.hdd_3_start_date_label = QLabel()
        self.hdd_3_end_date_label = QLabel()
        self.hdd_3_num_sessions_label = QLabel()
        self.hdd_3_icon_label = QLabel()

        # 4
        self.hdd_4_number = QLabel()
        self.hdd_4_label = QLabel()
        self.hdd_4_hddid_label = QLabel()
        self.hdd_4_start_date_label = QLabel()
        self.hdd_4_end_date_label = QLabel()
        self.hdd_4_num_sessions_label = QLabel()
        self.hdd_4_icon_label = QLabel()

        # 5
        self.hdd_5_number = QLabel()
        self.hdd_5_label = QLabel()
        self.hdd_5_hddid_label = QLabel()
        self.hdd_5_start_date_label = QLabel()
        self.hdd_5_end_date_label = QLabel()
        self.hdd_5_num_sessions_label = QLabel()
        self.hdd_5_icon_label = QLabel()

        # version
        self.version = QLabel('Version')
        self.version_label = QLabel(version)

        # add_button
        add_button = QPushButton('Add new HDD to the shipment',  self)
        add_button.setIcon(QtGui.QIcon('images/HDD-512.png'))
        add_button.setIconSize(QtCore.QSize(50, 50))
        add_button.clicked.connect(self.add_new_hdd)
        add_button.setToolTip('Add ndew Hdd to the queue')
        add_button.setStyleSheet('color:blue')
        add_button.setStyleSheet("background-color:#B7D9FF");

        # button
        button = QPushButton('Send HDD information', self)
        button.setIcon(QtGui.QIcon('images/send.png'))
        button.setIconSize(QtCore.QSize(65, 65))
        button.clicked.connect(self.show_popup)
        button.setToolTip('Send information to database')
        button.setStyleSheet('color:green')
        button.setStyleSheet("background-color:#CCFFCC;");

        self.message_window = QMessageBox()
        self.message_window.setWindowTitle('Info')

        self.txt_review = QLineEdit()
        self.txt_review.setPlaceholderText('enter your opinion')

        # GRID

        grid_layout = QGridLayout()
        grid_layout.setSpacing(3)

        # Drivers name
        grid_layout.addWidget(self.driver_name_label, 1, 0)  # column 1, row 0
        grid_layout.addWidget(self.driver_name_text, 1, 1)

        # Car name
        grid_layout.addWidget(self.car_name_label, 2, 0)  # column 1, row 0
        grid_layout.addWidget(self.car_name_text, 2, 1)

        # HDD ID
        grid_layout.addWidget(self.hdd_id_label, 3, 0)
        grid_layout.addWidget(self.hdd_id_text, 3, 1)  # column 2, row 1 to column 5 row 1

        # number of sessions
        grid_layout.addWidget(self.count_sessions_label, 4, 0)
        grid_layout.addWidget(self.count_sessions_text, 4, 1)  # column 2, row 1 to column 5 row 1

        # sessions range
        grid_layout.addWidget(self.start_date_label, 5, 0)
        grid_layout.addWidget(self.start_date_text, 5, 1)
        grid_layout.addWidget(self.end_date_label, 6, 0)
        grid_layout.addWidget(self.end_date_text, 6, 1)

        # awb number
        grid_layout.addWidget(self.airwaybill_label, 7, 0)
        grid_layout.addWidget(self.airwaybill_text, 7, 1)

        # generated code
        grid_layout.addWidget(self.generated_code_label, 8, 0)
        grid_layout.addWidget(self.generated_code_text, 8, 1)

        # list of sessions
        grid_layout.addWidget(self.sessions_list_text, 1, 3,
                              8, 3)

        # vpn
        grid_layout.addWidget(self.vpn_label, 9, 0)
        grid_layout.addWidget(self.vpn_connection_label, 9, 1)

        # hdd health status
        grid_layout.addWidget(self.hdd_health_status_label, 10, 0)
        grid_layout.addWidget(self.check_hdd_health_status_label, 10, 1)

        # hdds
        grid_layout.addWidget(self.hdd_1_label, 15, 0)
        grid_layout.addWidget(self.hdd_1_hddid_label, 15, 1)
        grid_layout.addWidget(self.hdd_1_start_date_label, 15, 3)
        grid_layout.addWidget(self.hdd_1_end_date_label, 15, 4)
        grid_layout.addWidget(self.hdd_1_num_sessions_label, 15, 5)
        grid_layout.addWidget(self.hdd_1_icon_label, 15, 6)
        grid_layout.addWidget(self.hdd_2_label, 16, 0)
        grid_layout.addWidget(self.hdd_2_hddid_label, 16, 1)
        grid_layout.addWidget(self.hdd_2_start_date_label, 16, 3)
        grid_layout.addWidget(self.hdd_2_end_date_label, 16, 4)
        grid_layout.addWidget(self.hdd_2_num_sessions_label, 16, 5)
        grid_layout.addWidget(self.hdd_2_icon_label, 16, 6)
        grid_layout.addWidget(self.hdd_3_label, 17, 0)
        grid_layout.addWidget(self.hdd_3_hddid_label, 17, 1)
        grid_layout.addWidget(self.hdd_3_start_date_label, 17, 3)
        grid_layout.addWidget(self.hdd_3_end_date_label, 17, 4)
        grid_layout.addWidget(self.hdd_3_num_sessions_label, 17, 5)
        grid_layout.addWidget(self.hdd_3_icon_label, 17, 6)
        grid_layout.addWidget(self.hdd_4_label, 18, 0)
        grid_layout.addWidget(self.hdd_4_hddid_label, 18, 1)
        grid_layout.addWidget(self.hdd_4_start_date_label, 18, 3)
        grid_layout.addWidget(self.hdd_4_end_date_label, 18, 4)
        grid_layout.addWidget(self.hdd_4_num_sessions_label, 18, 5)
        grid_layout.addWidget(self.hdd_4_icon_label, 18, 6)
        grid_layout.addWidget(self.hdd_5_label, 19, 0)
        grid_layout.addWidget(self.hdd_5_hddid_label, 19, 1)
        grid_layout.addWidget(self.hdd_5_start_date_label, 19, 3)
        grid_layout.addWidget(self.hdd_5_end_date_label, 19, 4)
        grid_layout.addWidget(self.hdd_5_num_sessions_label, 19, 5)
        grid_layout.addWidget(self.hdd_5_icon_label, 19, 6)

        # version

        grid_layout.addWidget(self.version,0, 0)
        grid_layout.addWidget(self.version_label,0, 1)

        # button
        grid_layout.addWidget(add_button, 0, 0, 25, 10)
        grid_layout.addWidget(button, 19, 0, 5, 10)

        # creating hdd's labels
        self.hdd_labels = [
            [
                self.hdd_1_label,
                self.hdd_1_hddid_label,
                self.hdd_1_start_date_label,
                self.hdd_1_end_date_label,
                self.hdd_1_num_sessions_label,
                self.hdd_1_icon_label
            ]
            ,
            [
                self.hdd_2_label,
                self.hdd_2_hddid_label,
                self.hdd_2_start_date_label,
                self.hdd_2_end_date_label,
                self.hdd_2_num_sessions_label,
                self.hdd_2_icon_label
            ],
            [
                self.hdd_3_label,
                self.hdd_3_hddid_label,
                self.hdd_3_start_date_label,
                self.hdd_3_end_date_label,
                self.hdd_3_num_sessions_label,
                self.hdd_3_icon_label
            ],
            [
                self.hdd_4_label,
                self.hdd_4_hddid_label,
                self.hdd_4_start_date_label,
                self.hdd_4_end_date_label,
                self.hdd_4_num_sessions_label,
                self.hdd_4_icon_label
            ],
            [
                self.hdd_5_label,
                self.hdd_5_hddid_label,
                self.hdd_5_start_date_label,
                self.hdd_5_end_date_label,
                self.hdd_5_num_sessions_label,
                self.hdd_5_icon_label
            ]
        ]

        # Qtimer
        timer = QTimer(self)
        timer.timeout.connect(self.refresh_hdd)
        timer.start(1200)

        timer2 = QTimer(self)
        timer2.timeout.connect(self.check_vpn_connection)
        timer2.start(10000)

        self.setLayout(grid_layout)
        self.setGeometry(500,  # x
                         400,  # y
                         600,
                         640)
        self.setWindowTitle('HDD tracker')
        self.setWindowIcon(QtGui.QIcon('send.png'))

    hdds = []

    # functions

    def check_vpn_connection(self):
        check_vpn(self.vpn_connection_label)

    def refresh_hdd(self):
        find_disks()
        new_hdd = create_hdd_object()
        if len(new_hdd.session_list) == 0:
            self.sessions_list_text.clear()
            self.car_name_text.setStyleSheet('color:red')
            self.start_date_text.setStyleSheet('color:red')
            self.end_date_text.setStyleSheet('color:red')
            self.hdd_id_text.setStyleSheet('color:red')
            self.count_sessions_text.setStyleSheet('color:red')
            self.count_sessions_text.setText(str(new_hdd.number_of_session))
            self.car_name_text.setText(str(new_hdd.car_name))
            self.hdd_id_text.setText('')
            self.start_date_text.setText(str(new_hdd.start_date))
            self.end_date_text.setText(str(new_hdd.end_date))
            self.sessions_list_text.clear()
            self.sessions_list_text.addItems([x for x in new_hdd.session_list])
            self.generated_code_text.setText(self.generated_code)
        else:
            try:
                obj = parase_crystaldisk()
            except FileNotFoundError:
                logging.info(f'{current_date}No DiskInfo.txt of file is empty')
            self.car_name_text.setStyleSheet('color:darkgreen')
            self.start_date_text.setStyleSheet('color:darkgreen')
            self.end_date_text.setStyleSheet('color:darkgreen')
            self.generated_code_text.setStyleSheet('color:darkgreen')
            self.hdd_id_text.setStyleSheet('color:darkgreen')
            self.count_sessions_text.setStyleSheet('color:darkgreen')
            self.generated_code_text.setStyleSheet('color:blue')
            self.count_sessions_text.setText(str(new_hdd.number_of_session))
            self.car_name_text.setText(str(new_hdd.car_name))
            self.hdd_id_text.setText(
                str(obj['disks'][len(obj['disks']) - 1]['Serial Number']))  # added last element from disk's list
            self.start_date_text.setText(str(new_hdd.start_date))
            self.end_date_text.setText(str(new_hdd.end_date))
            self.sessions_list_text.clear()
            self.sessions_list_text.addItems([x for x in new_hdd.session_list])
            if self.generated_code == 'no hdd':
                self.generated_code = code_generator(new_hdd.car_name, current_date_for_gc.replace('_', '-'), 3)
                self.generated_code_text.setText(self.generated_code)
                print(self.generated_code)

    print(current_date)
    number_of_hdd = 0

    # creating new shipment template
    new_shipment = {
        'id': None,
        'status': 'prepared',
        'create_date': current_date,
        "DHL_data": {
            "awb": "-",
            "event_date": "-",
            "event_desc": "-",
            "event_signatory": "-",
            "event_time": "-",
            "ref_id": "-",
            "ship_date": "-",
            "ship_to": "-",
            "shipper_name": "-",
            "status_code": "-"
        },
        "self_delivery_data": {
            "location": "-",
            "comment": "-"
        },
        'driver': '-',
        'disks': [],
        "previous_status": "-",
        "status_history": {
            "prepared": current_date,
            "sent": "-",
            "self_delivered": "-",
            "delivered": "-",
            "received": "-"},
        "_rid": "FNx-AOmVdYQjAAAAAAAAAA==",
        "_self": "dbs/FNx-AA==/colls/FNx-AOmVdYQ=/docs/FNx-AOmVdYQjAAAAAAAAAA==/",
        "_etag": "\"85005be0-0000-0d00-0000-5fa95b4a0000\"",
        "_attachments": "attachments/",
        "_ts": 1604934474
    }

    # buttons function
    @pyqtSlot()
    def add_new_hdd(self):
        filePath = f'{__location__}\DiskInfo.txt'
        modificationTime = get_last_file_modified_data(filePath)

        # executing CrystalDiskInfo

        logging.info(f'\n{current_date}\nExecuting Cristal Disk info')
        subprocess.run(
            ["powershell", "start", f"'{__location__}\DiskInfo64.exe'", "-ArgumentList",
             "/CopyExit ", "-Verb", "Runas"])
        logging.info(f'\n{current_date}\nExecuting Cristal Disk Info done')
        modificationTimeNew = get_last_file_modified_data(filePath)

        # comparing last modification date to make sure that file is already updated
        while modificationTime == modificationTimeNew:
            modificationTimeNew = get_last_file_modified_data(filePath)
            print(Fore.YELLOW + "Waiting for DiskInfo.txt update")
            time.sleep(0.5)
        print('')
        print(Fore.GREEN + 'Success')
        time.sleep(0.5)
        print(Fore.GREEN + "DiskInfo.txt has been updated")
        obj = parase_crystaldisk()
        logging.info(f'\n{current_date}\nDiskInfo.txt has been updated\nObject: {obj}')
        new_hdd = create_hdd_object()
        self.new_shipment['id'] = self.generated_code
        self.new_shipment['driver'] = self.driver_name_text.text()

        new_disk = {
            'carname': new_hdd.car_name,
            'hdd_serial_number': obj['disks'][len(obj['disks']) - 1]['Serial Number'],
            'health_status': '-',
            'sessions_from': new_hdd.start_date,
            'sessions_to': new_hdd.end_date,
            'sessions': new_hdd.session_list
        }
        try:
            new_disk['health_status'] = obj['disks'][len(obj['disks'])-1]['Health Status']
            heatlh_status(self.check_hdd_health_status_label, obj['disks'][len(obj['disks'])-1]['Health Status'])
        except:
            pass

        if new_disk not in self.new_shipment['disks'] and new_disk['carname'] != 'no hdd':
            print(Fore.GREEN + 'HDD has been just added to the shipment\n')
            self.new_shipment['disks'].append(new_disk)

            self.hdd_labels[self.number_of_hdd][0].setText(new_hdd.car_name)
            self.hdd_labels[self.number_of_hdd][0].setStyleSheet('background-color: #00ff00')
            self.hdd_labels[self.number_of_hdd][1].setText(new_disk['hdd_serial_number'])
            self.hdd_labels[self.number_of_hdd][1].setStyleSheet('background-color: #00ff00')
            self.hdd_labels[self.number_of_hdd][2].setText(new_hdd.start_date)
            self.hdd_labels[self.number_of_hdd][2].setStyleSheet('background-color: #00ff00')
            self.hdd_labels[self.number_of_hdd][3].setText(new_hdd.end_date)
            self.hdd_labels[self.number_of_hdd][3].setStyleSheet('background-color: #00ff00')
            self.hdd_labels[self.number_of_hdd][4].setText(str(new_hdd.number_of_session))
            self.hdd_labels[self.number_of_hdd][4].setStyleSheet('background-color: #00ff00')
            self.hdd_labels[self.number_of_hdd][4].setAlignment(QtCore.Qt.AlignCenter)
            self.hdd_labels[self.number_of_hdd][5].setPixmap((QtGui.QPixmap('images/hdd.png')))
            self.number_of_hdd += 1

            print(f"Reading data from: {obj['disks'][1]['Drive Letter']}")
            logging.info(f'\n{current_date}\nAdded new disk to the shipment\nNew disk: {new_disk}\n')
        else:
            print(Fore.RED + 'Wrong')
            print(Fore.RED + "Error you cannot add HDD")
            logging.info(f'\n{current_date}\nCannot add HDD')
            self.message_window.setText('HDD already exists in the shipment or no HDD')
            x = self.message_window.exec()

    @pyqtSlot()
    def show_popup(self):
        res = QMessageBox.question(self, 'MessageBox', 'Are you sure?', QMessageBox.Yes | QMessageBox.Cancel,
                                   QMessageBox.Cancel)
        if res == QMessageBox.Yes:
            self.on_click()
        else:
            print('No')

    @pyqtSlot()
    def on_click(self):
        if len(self.driver_name_text.text()) == 0:
            self.message_window.setText('Add driver name')
            x = self.message_window.exec()
        else:
            try:
                print(Fore.GREEN + 'Sending')
                self.new_shipment['driver'] = self.driver_name_text.text()
                _, scode = send_to_heimdall(self.new_shipment)
                logging.info(f'\n{current_date}\nShipement has been saved to db\nShipement: {self.new_shipment}\n')
                self.message_window.setText(f'Success! Your code: {self.generated_code}')
                x = self.message_window.exec()
                save_last_ship_to_file(self.new_shipment['disks'][0]['carname'], current_date, self.generated_code)
                print(Fore.GREEN + "Success")
                print(Fore.GREEN + "Shipment has been added to DB")
                print(Fore.GREEN + "Ship's info has been added to lastship.txt as well")
                print(Fore.WHITE + "DONT FORGET YOUR CODE!")
            except:
                scode = '400'
                logging.info(f'\n{current_date}\nCan send data to db')
                self.message_window.setText('No connection or shipement exists in database')
                x = self.message_window.exec()


stylesheet = """

    
    QListWidget{
        border: 1px solid black;
    }
    QLineEdit{
        border: 1px solid black;
        margin-bottom:1px;
    }
    QLabel{
        margin-bottom:1px;
        font-size:14px;
        font-weight: bold;
    }
    QComboBox{
        margin-bottom:1px;
        font-size:14px;
        font-weight: bold;
    }
    QCheckBox{
        margin-bottom:1px;
        font-size:14px;
        font-weight: bold;

"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    pprint('input parameters = ' + str(sys.argv))
    tutorial_window = DriverWindow()
    tutorial_window.setWindowIcon(QtGui.QIcon('images/postman.png'))
    tutorial_window.show()
    sys.exit(app.exec())
