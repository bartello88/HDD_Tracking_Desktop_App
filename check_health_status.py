def heatlh_status(hdd_health_status, status):
    if status == 'Good':
        hdd_health_status.setText('Good')
        hdd_health_status.setStyleSheet('color:Green')
    elif status == 'Caution':
        hdd_health_status.setText('Caution')
        hdd_health_status.setStyleSheet('color:rgb(204, 204, 0)')
    elif status == 'Bad':
        hdd_health_status.setText('Bad')
        hdd_health_status.setStyleSheet('color:Red')
    else:
        hdd_health_status.setText('Unknow')
        hdd_health_status.setStyleSheet('color:black')