import mysql.connector
from db_config import DB_CONFIG

def test():
    try:
        con = mysql.connector.connect(**DB_CONFIG)
        if con.is_connected():
            print("Verbindung erfolgreich!")
            con.close()
            print("Verbindung geschlossen.")
        return True
    except mysql.connector.Error as e:
        print(f"Fehler aufgetreten: {e}")
        print("""
            Wenn du mit einem Remote Server verbunden bist, teste ob er läuft.
            Trage dann die richtige IP-Adresse in die .env ein.
            Überprüfe ob du die richtigen Zugangsdaten für die Datenbank hast.
            """)

if __name__ == '__main__':
    test()