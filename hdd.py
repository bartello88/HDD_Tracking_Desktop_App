class Hdd():
    def __init__(self, hdd_serial_number, car_name, session_list, number_of_session, driver, hdd_size, hdd_used, date,
                 start_date, end_date, abw=''):
        self.hdd_serial_number = hdd_serial_number
        self.car_name = car_name
        self.session_list = session_list
        self.number_of_session = number_of_session
        self.driver = driver
        self.hdd_size = hdd_size
        self.hdd_used = hdd_used
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.abw = abw

    def __repr__(self):
        return f'Serial number: {self.hdd_serial_number}\nCar name: {self.car_name}\nNumber of sessions: {self.number_of_session}\nSessions: {self.session_list}\nDriver: {self.driver}\nHdd size: {self.hdd_size} GBs\nHdd used space: {self.hdd_used} GBs\nStart date: {self.start_date}\nEnd date : {self.end_date}\nABW: {self.abw}'
