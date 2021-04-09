import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
def save_last_ship_to_file(car_name,date, code):
    with open('lastship.txt',  'a') as f:
        file = f.write(f'\nCar name: {car_name}\nDate: {date}\nCode: {code}\n\n')
