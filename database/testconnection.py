import mysql.connector
from db_config import DB_CONFIG

try:
    con = mysql.connector.connect(**DB_CONFIG)
    if con.is_connected():
        print("Verbindung erfolgreich!")
        con.close()
        print("Verbindung geschlossen.")
except mysql.connector.Error as e:
    print(f"Fehler aufgetreten: {e}")