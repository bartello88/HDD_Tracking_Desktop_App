from pythonping import ping
from colorama import *
import requests

def check_vpn(vpn_connection_label):
    try:
        ping('PL1WXD-105103', timeout=0.1)
        print(Fore.GREEN + 'You are connected to VPN')
        vpn_connection_label.setText('connected')
        vpn_connection_label.setStyleSheet('color:green')
    except:
        print(Fore.RED + 'No connection')
        vpn_connection_label.setText('no connection')
        vpn_connection_label.setStyleSheet('color:red')
