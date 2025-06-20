from dotenv import load_dotenv, set_key, dotenv_values
import os
from subprocess import check_output
import sys

load_dotenv(override=False)
MULTIPASS = os.getenv('MULTIPASS', '')
DB_RUNNING = os.getenv('DB_RUNNING', '')
DB_SERVER = os.getenv('DB_SERVER', '')
# ---
DB_IPADDRESS = os.getenv('DB_IPADDRESS', 'localhost')
DB_DATABASE=os.getenv('DB_DATABASE')
DB_USERNAME=os.getenv('DB_USERNAME')
DB_PASSWORD=os.getenv('DB_PASSWORD')

# MULTIPASS = True

if MULTIPASS and not DB_RUNNING:
    def get_ip():
        print(f'Suche nach IP von Multipass Server "{DB_SERVER}"...')
        info: str
        names: list[str]
        i: int
        try:
            info = check_output('multipass info', shell=True).decode('utf-8').split('\r\n')
            names = info[::12]
            if names[0].split()[0] != 'Name:':
                raise Exception
            names = [n.split()[1] for n in names]
        except:
            print('Es schien einen Fehler mit "multipass info" zu geben. Output:')
            print(info)
            sys.exit()
        try:
            i = names.index(DB_SERVER)
        except ValueError:
            print(f'Der Multipassserver "{DB_SERVER}" wurde nicht gefunden.')
            sys.exit()
        ip = info[3::12][i].split()[1]
        return ip if len(ip.split('.')) == 4 else None
    
    while not (ip:=get_ip()):
        print(f'Starte Multipass Server "{DB_SERVER}"...')
        os.system(f'multipass start {DB_SERVER}')
        
    print(f'IP von "{DB_SERVER}" gefunden: {ip}')
    DB_IPADDRESS = ip
    set_key('.env', 'DB_IPADDRESS', DB_IPADDRESS)
    set_key('.env', 'DB_RUNNING', 'True')

DB_CONFIG = dict(
    host = DB_IPADDRESS,
    database = DB_DATABASE,
    user = DB_USERNAME,
    password = DB_PASSWORD,
    connection_timeout = 10
)
# print(DB_CONFIG)